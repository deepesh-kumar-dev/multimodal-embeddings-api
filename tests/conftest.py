"""Shared pytest fixtures, available to every test file without importing.

Test files mirror the routes: tests/test_<feature>.py tests app/api/routes/<feature>.py.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client():
    # Entering the context runs the lifespan, which loads the model once for all tests.
    with TestClient(app) as c:
        yield c
