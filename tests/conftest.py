"""Shared pytest fixtures, available to every test file without importing.

Test files mirror the routes: ``tests/test_<feature>.py`` tests
``app/api/routes/<feature>.py``.
"""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client() -> Iterator[TestClient]:
    """Provide a test client shared by the whole test session.

    Entering the client's context runs the app's lifespan, so the model is loaded
    once for all tests instead of once per test.

    Yields:
        A client for sending requests to the app.
    """
    with TestClient(app) as test_client:
        yield test_client
