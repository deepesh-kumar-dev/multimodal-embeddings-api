# Architecture Guide

How the project is organized, how a request flows through it, how to debug it, and
how to extend it.

## Layers

The app is split into four layers. Each layer may only import from the layers
**below** it, so changes stay contained.

```
┌────────────────────────────────────────────────────────────┐
│ api/        HTTP: routes, dependencies, router             │  knows about FastAPI
├────────────────────────────────────────────────────────────┤
│ schemas/    Request/response shapes and validation         │  Pydantic only
├────────────────────────────────────────────────────────────┤
│ services/   Business logic: model loading, embeddings      │  no FastAPI imports
├────────────────────────────────────────────────────────────┤
│ core/       Settings and logging                           │  used by everyone
└────────────────────────────────────────────────────────────┘
```

| Layer | Responsible for | Must NOT |
|---|---|---|
| `api/` | URLs, HTTP status codes, wiring dependencies | Contain model or business logic |
| `schemas/` | Field types, limits, examples shown in `/docs` | Call services or the model |
| `services/` | Loading the model, computing results | Import FastAPI or know about HTTP |
| `core/` | Settings, logging | Import from any other layer |

## File map

| File | What it does | Change it when you want to... |
|---|---|---|
| `app/main.py` | Creates the app, sets up logging, loads the model at startup, mounts routes | Add startup/shutdown work or middleware |
| `app/core/config.py` | All settings (`EMBED_*` env vars) | Add a new setting |
| `app/core/logging.py` | Log format and level | Change log output |
| `app/api/router.py` | Registers every route module | Add a new route module |
| `app/api/dependencies.py` | Gives routes the shared `EmbeddingService` | Share a new object with routes |
| `app/api/routes/health.py` | `GET /health` | Change the health check |
| `app/api/routes/embeddings.py` | `POST /embed/text` | Add or change embedding endpoints |
| `app/schemas/embeddings.py` | Request/response models and validation for `/embed/*` | Change input limits or response fields |
| `app/schemas/health.py` | Response model for `/health` | Change the health response |
| `app/services/embedding.py` | `EmbeddingService`: the only code that touches the model | Change model library or add input types |
| `tests/conftest.py` | Shared test client (loads model once) | Add shared fixtures |
| `tests/test_<feature>.py` | Tests for `app/api/routes/<feature>.py` | Test a feature |
| `.env.example` | Documents every setting with its default | Add a new setting |

## Request flow

What happens for `POST /embed/text`:

```
Client
  │  POST /embed/text  {"texts": [...]}
  ▼
app/main.py              app built by create_app(); model already loaded by lifespan()
  │
  ▼
app/api/router.py        matches /embed/text → embeddings.router
  │
  ▼
app/schemas/embeddings.py   TextEmbeddingRequest validates the body
  │                         (invalid → 422 returned here, route never runs)
  ▼
app/api/dependencies.py  get_embedding_service() fetches the shared service
  │
  ▼
app/api/routes/embeddings.py   embed_text() calls service.embed_texts()
  │
  ▼
app/services/embedding.py      model.encode() → numpy array
  │
  ▼
Route builds TextEmbeddingResponse → JSON back to the client
```

Startup happens once, before any request: `create_app()` → `setup_logging()` →
`lifespan()` → `EmbeddingService(...)` loads the model and stores it on `app.state`.

## Debugging

**Turn on debug logs** to see model loading and per-request timings:

```bash
EMBED_LOG_LEVEL=debug uvicorn app.main:app --reload
```

```
... INFO     [app.services.embedding] Loading model 'clip-ViT-B-32' (device=auto)...
... INFO     [app.services.embedding] Model loaded in 3.2s on cpu
... DEBUG    [app.services.embedding] Embedded 2 text(s) in 41ms
```

**Try requests interactively** at http://127.0.0.1:8000/docs.

**Run a single test** with output shown:

```bash
pytest tests/test_text_embeddings.py -k similar -s
```

**Use the debugger without the server**: services don't depend on FastAPI, so you
can call them directly in a Python shell:

```python
from app.services.embedding import EmbeddingService
svc = EmbeddingService("clip-ViT-B-32")
svc.embed_texts(["hello"]).shape   # (1, 512)
```

### Common problems

| Symptom | Where to look | Likely cause / fix |
|---|---|---|
| `Application startup failed` | Traceback from `app/services/embedding.py` | Model failed to load: check `EMBED_MODEL_NAME`, internet access for first download, missing package |
| `Missing optional dependencies: ... Pillow` | `pyproject.toml` | Run `pip install -e ".[dev]"` again |
| `422 Unprocessable Entity` | `app/schemas/embeddings.py` | Request body broke a validation rule (empty list, too many texts, wrong field name). The response `detail` says which |
| `500 Internal Server Error` | Server logs | Error inside a route or service; the traceback is printed in the uvicorn terminal |
| Very slow first request or startup | Logs: "Model loaded in ..." | First run downloads the model (~600 MB); later runs use the cache in `~/.cache/huggingface` |
| `CUDA` errors | `EMBED_DEVICE` | Set `EMBED_DEVICE=cpu` or install GPU-enabled PyTorch |

## Extending: adding a new feature

Example: adding `POST /embed/image`. Work from the bottom layer up.

1. **Service** — add a method to `EmbeddingService` in `app/services/embedding.py`:
   ```python
   def embed_images(self, images: list[Image.Image], normalize: bool = True) -> np.ndarray:
       return self._model.encode(images, normalize_embeddings=normalize)
   ```
2. **Schemas** — add `ImageEmbeddingResponse` to `app/schemas/embeddings.py` and
   export it from `app/schemas/__init__.py`.
3. **Route** — add an `@router.post("/image")` function to
   `app/api/routes/embeddings.py`. Keep it thin: read the upload, call the service,
   return the schema.
4. **Settings** (if needed) — add fields to `app/core/config.py` and document them in
   `.env.example` and the README.
5. **Tests** — add tests to `tests/test_image_embeddings.py`.
6. **Docs** — update the README usage section and the file map above.

For a **completely new feature area** (not embeddings), create a new
`app/api/routes/<feature>.py` with its own `router`, register it in
`app/api/router.py`, and add `app/schemas/<feature>.py` and, if it has logic,
`app/services/<feature>.py`.

### Conventions

- Use plain `def` (not `async def`) for routes that run the model, so they run in a
  thread pool and don't block other requests.
- Get a logger per module with `logger = logging.getLogger(__name__)`; never `print`.
- Put validation in schemas, not in route bodies.
- Read settings from `app.core.config.settings`; never hard-code values or read
  `os.environ` directly.
