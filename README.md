# Multimodal Embeddings API

FastAPI service that generates embeddings with CLIP. Text and image vectors share one
vector space, so they can be compared directly. Text embeddings are available now;
image embeddings are planned.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate

# CPU-only PyTorch (much smaller download). Skip this line if you have an NVIDIA GPU.
pip install torch --index-url https://download.pytorch.org/whl/cpu

pip install -e ".[dev]"
```

## Run

```bash
uvicorn app.main:app --reload
```

The model downloads on first start (~600 MB). Interactive docs: http://127.0.0.1:8000/docs

## Usage

```bash
curl -X POST http://127.0.0.1:8000/embed/text \
  -H "Content-Type: application/json" \
  -d '{"texts": ["a photo of a cat", "a red sports car"]}'
```

```json
{
  "model": "clip-ViT-B-32",
  "dimensions": 512,
  "embeddings": [[0.012, -0.034, ...], [...]]
}
```

Vectors are L2-normalized by default, so the dot product of two vectors is their cosine
similarity. Send `"normalize": false` to get raw vectors.

## Configuration

Set environment variables or add them to a `.env` file (start from the template with
`cp .env.example .env`):

| Variable | Default | Description |
|---|---|---|
| `EMBED_MODEL_NAME` | `clip-ViT-B-32` | Any sentence-transformers model |
| `EMBED_DEVICE` | auto | `cpu` or `cuda` |
| `EMBED_MAX_BATCH_SIZE` | `64` | Max texts per request |
| `EMBED_LOG_LEVEL` | `info` | `debug` shows per-request timings |

Note: CLIP truncates text to 77 tokens. For long documents, use a text-only model such as
`all-MiniLM-L6-v2`. Its vectors won't be comparable with CLIP image embeddings.

## Project structure

```
app/
├── main.py                 # Entry point: builds the app, loads the model, mounts routes
├── core/                   # App-wide setup
│   ├── config.py           #   Settings (EMBED_* env vars / .env)
│   └── logging.py          #   Log format and level
├── api/                    # HTTP layer
│   ├── router.py           #   Registers all route modules
│   ├── dependencies.py     #   Shares the EmbeddingService with routes
│   └── routes/
│       ├── health.py       #   GET  /health
│       └── embeddings.py   #   POST /embed/text
├── schemas/                # Request/response models and validation
│   ├── embeddings.py
│   └── health.py
└── services/               # Business logic, no FastAPI
    └── embedding.py        #   EmbeddingService: the only code that touches the model
tests/
├── conftest.py             # Shared test client (loads model once)
├── test_health.py
└── test_text_embeddings.py
docs/
└── ARCHITECTURE.md         # Layers, request flow, debugging, extending
.env.example                # Every setting with its default
```

Every module starts with a docstring explaining what it does and where related code
lives. See **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** for the request flow, a
debugging guide, and step-by-step instructions for adding features.

## Tests

```bash
pytest
```
