import pytest
from app.config import SessionFactory
from app.config import DatabaseConfigurationError


def setup_env(monkeypatch, db_type="postgres"):
    monkeypatch.setenv("DB_TYPE", db_type)
    monkeypatch.setenv("DB_USER", "user")
    monkeypatch.setenv("DB_PASS", "pass")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_NAME", "testdb")


def reset_factory_singleton():
    SessionFactory._instance = None
    SessionFactory._engine = None
    SessionFactory._Session = None


def test_configuracao_incompleta(monkeypatch):
    reset_factory_singleton()
    monkeypatch.delenv("DB_USER", raising=False)
    with pytest.raises(DatabaseConfigurationError):
        SessionFactory()


def test_tipo_nao_suportado(monkeypatch):
    reset_factory_singleton()
    setup_env(monkeypatch, "sqlite")
    with pytest.raises(DatabaseConfigurationError):
        SessionFactory()


def test_singleton(monkeypatch):
    reset_factory_singleton()
    setup_env(monkeypatch)
    f1 = SessionFactory()
    f2 = SessionFactory()
    assert f1 is f2


def test_context_manager(monkeypatch):
    reset_factory_singleton()
    setup_env(monkeypatch)
    factory = SessionFactory()

    class DummySession:
        def __init__(self): self.closed, self.committed = False, False
        def commit(self): self.committed = True
        def rollback(self): self.committed = False
        def close(self): self.closed = True

    factory._Session = lambda: DummySession()

    with factory.get_session() as session:
        assert isinstance(session, DummySession)


def test_check_connection_falha(monkeypatch):
    reset_factory_singleton()
    setup_env(monkeypatch)
    factory = SessionFactory()
    factory._engine = None  # força erro
    with pytest.raises(Exception):
        factory.check_connection()
