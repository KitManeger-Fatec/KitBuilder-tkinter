# db/factory.py
from urllib.parse import quote_plus
from typing import Tuple
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class SQLAlchemyFactory:
    """
    Factory para criar engine SQLAlchemy e um Session factory (sessionmaker).
    Suporta 'postgres' (psycopg2) e 'mysql' (mysql-connector).
    Retorna (engine, SessionClass).
    """

    def create_engine_and_session(self,
                                  db_type: str,
                                  user: str | None = None,
                                  password: str | None = None,
                                  host: str = "localhost",
                                  port: int | None = None,
                                  database: str | None = None,
                                  echo: bool = False,
                                  **create_engine_kwargs) -> Tuple:
        db_type = (db_type or "").lower().strip()

        if db_type == "postgres":
            driver = "postgresql+psycopg2"
            default_port = 5432
        elif db_type == "mysql":
            driver = "mysql+mysqlconnector"
            default_port = 3306
        else:
            raise ValueError("Unsupported db_type '{}'. Supported: 'postgres', 'mysql'.".format(db_type))

        port = port or default_port

        # monta parte de auth (com escape)
        auth = ""
        if user:
            auth = quote_plus(str(user))
            if password:
                auth += ":" + quote_plus(str(password))
            auth += "@"

        db_name = database or ""

        # monta URL: driver://user:pass@host:port/dbname
        url = f"{driver}://{auth}{host}:{port}/{db_name}"

        # cria engine passando kwargs extras (pool_size, future, etc)
        engine = create_engine(url, echo=echo, **create_engine_kwargs)

        # cria Session factory atrelada ao engine
        Session = sessionmaker(bind=engine)

        return engine, Session
