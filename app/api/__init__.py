"""API layer: everything HTTP-specific.

- router.py        Combines all route modules into one router
- dependencies.py  Shared objects injected into routes (e.g. EmbeddingService)
- routes/          One module per feature, each defining its own APIRouter

Routes should stay thin: validate input via schemas, call a service, and
build the response. Put real logic in services/.
"""
