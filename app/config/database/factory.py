import os
import logging
from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, OperationalError

from app.config.exceptions import DatabaseConfigurationError, DatabaseConnectionError
from app.config.database.validators import DatabaseConfigValidator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class SessionFactory:
    """Factory Singleton para Engine + Session SQLAlchemy."""

    _instance = None
    _engine = None
    _Session = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionFactory, cls).__new__(cls)
            cls._instance._configure()
        return cls._instance

    def _configure(self):
        DatabaseConfigValidator.validate()

        db_type = os.getenv("DB_TYPE").lower()
        db_user = os.getenv("DB_USER")
        db_pass = os.getenv("DB_PASS")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_name = os.getenv("DB_NAME")

        if db_type == "postgres":
            url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        elif db_type == "mysql":
            url = f"mysql+mysqlconnector://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        else:
            raise DatabaseConfigurationError(f"Tipo de banco não suportado: {db_type}")

        try:
            self._engine = create_engine(url, echo=False, future=True)
            self._Session = sessionmaker(bind=self._engine, autoflush=False, autocommit=False, future=True)
            logger.info(f"Engine criada com sucesso para {db_type} em {db_host}:{db_port}/{db_name}")
        except SQLAlchemyError as e:
            raise DatabaseConnectionError(f"Erro ao configurar engine: {e}") from e

    @contextmanager
    def get_session(self):
        """Gerencia sessão com commit/rollback automático."""
        session = self._Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Erro na sessão: {e}")
            raise
        finally:
            session.close()

    def check_connection(self):
        """Health-check simples da conexão."""
        try:
            with self._engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Conexão validada com sucesso.")
            return True
        except OperationalError as e:
            raise DatabaseConnectionError(f"Falha na conexão: {e}") from e
