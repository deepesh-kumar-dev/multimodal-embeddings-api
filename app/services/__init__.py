"""Services layer: business logic, independent of HTTP.

- embedding.py  EmbeddingService: loads the model and computes embeddings

Services must not import FastAPI or anything from api/, so they can be
reused from scripts, workers or tests without running a web server.
"""
