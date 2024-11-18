import pytest
from fastapi.testeclient import TesteClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.models import table_registry


@pytest.fixture
def client():
    return TesteClient(app)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    # Gerenciamento de contexto
    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
