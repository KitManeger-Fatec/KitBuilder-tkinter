# tests/test_db_factory.py
import db.factory as db_factory_mod
from db.factory import SQLAlchemyFactory
import pytest

def test_create_postgres_engine_and_session(monkeypatch):
    recorded = {}

    def fake_create_engine(url, echo=False, **kwargs):
        recorded['url'] = str(url)
        recorded['echo'] = echo
        recorded['opts'] = kwargs
        return "ENGINE_PG"

    def fake_sessionmaker(bind=None):
        recorded['session_bind'] = bind
        return "SESSION_PG"

    # patch local names in module db.factory
    monkeypatch.setattr(db_factory_mod, "create_engine", fake_create_engine)
    monkeypatch.setattr(db_factory_mod, "sessionmaker", fake_sessionmaker)

    factory = SQLAlchemyFactory()
    engine, Session = factory.create_engine_and_session(
        "postgres",
        user="pguser",
        password="pgpass",
        host="pg-host",
        port=5432,
        database="pgdb",
        echo=True,
        pool_size=5
    )

    assert engine == "ENGINE_PG"
    assert Session == "SESSION_PG"
    assert "postgresql+psycopg2://" in recorded['url']
    assert "pg-host" in recorded['url']
    assert "5432" in recorded['url']
    assert "/pgdb" in recorded['url']
    assert "pguser" in recorded['url']
    assert "pgpass" in recorded['url']
    assert recorded['echo'] is True
    assert recorded['opts']['pool_size'] == 5
    assert recorded['session_bind'] == "ENGINE_PG"


def test_create_mysql_engine_and_session(monkeypatch):
    recorded = {}

    def fake_create_engine(url, echo=False, **kwargs):
        recorded['url'] = str(url)
        recorded['echo'] = echo
        recorded['opts'] = kwargs
        return "ENGINE_MY"

    def fake_sessionmaker(bind=None):
        recorded['session_bind'] = bind
        return "SESSION_MY"

    monkeypatch.setattr(db_factory_mod, "create_engine", fake_create_engine)
    monkeypatch.setattr(db_factory_mod, "sessionmaker", fake_sessionmaker)

    factory = SQLAlchemyFactory()
    engine, Session = factory.create_engine_and_session(
        "mysql",
        user="myuser",
        password="mypass",
        host="my-host",
        port=3306,
        database="mydb",
        echo=False,
        pool_size=10
    )

    assert engine == "ENGINE_MY"
    assert Session == "SESSION_MY"
    assert "mysql+mysqlconnector://" in recorded['url']
    assert "my-host" in recorded['url']
    assert "3306" in recorded['url']
    assert "/mydb" in recorded['url']
    assert "myuser" in recorded['url']
    assert "mypass" in recorded['url']
    assert recorded['echo'] is False
    assert recorded['opts']['pool_size'] == 10
    assert recorded['session_bind'] == "ENGINE_MY"


def test_unsupported_db_type_raises():
    factory = SQLAlchemyFactory()
    with pytest.raises(ValueError):
        factory.create_engine_and_session("sqlite", database="x")
