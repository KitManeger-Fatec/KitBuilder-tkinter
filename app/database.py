from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus

# --- CONFIGURAÇÕES DO BANCO ---
USER = "root"
PASSWORD = quote_plus("Supernatur@l1985")  # Protege caracteres especiais
HOST = "localhost"
DB = "db_listaCompras"

# --- ENGINE PARA O BANCO ---
DATABASE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DB}"
engine = create_engine(DATABASE_URL, echo=True)  # echo=True mostra queries no console

# --- BASE ORM ---
Base = declarative_base()

# --- SESSION FACTORY ---
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
