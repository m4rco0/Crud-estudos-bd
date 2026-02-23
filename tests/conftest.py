import os
from contextlib import contextmanager
from datetime import datetime

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from loja_db.app import app
from loja_db.database import get_session
from loja_db.models import table_registry

"""Cliente usado para testes"""
load_dotenv()


@pytest.fixture
def client():
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client
    app.dependency_overrides.clear()


""" Testando conexão com o banco de dados"""


@pytest.fixture
def session():
    url = os.getenv('DATABASE_URL')
    engine = create_engine(url)
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


""" Criando uma DateTime falso para testes em uma Tabela"""


@contextmanager
def _mock_db_time(model, time=datetime(2025, 5, 20)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time

    event.listen(model, 'before_insert', fake_time_hook)

    yield time
    event.listen(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time
