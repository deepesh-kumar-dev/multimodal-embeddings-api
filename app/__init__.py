"""Multimodal Embeddings API.

Package layout (each layer only imports from the layers below it):

    api/       HTTP layer: routes, request handling, dependencies
    schemas/   Pydantic models describing request and response bodies
    services/  Business logic: loading the model and computing embeddings
    core/      Cross-cutting setup: settings and logging

Entry point: app/main.py. See docs/ARCHITECTURE.md for the full guide.
"""
