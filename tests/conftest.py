import pytest
from fastapi.testeclient import TesteClient

from fast_zero.app import app


@pytest.fixture
def client():
    return TesteClient(app)
