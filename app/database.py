from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os   

# --- CONFIGURAÇÕES DO BANCO ---
load_dotenv()
USER = os.getenv("DB_USER")
PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
HOST = os.getenv("DB_HOST")
DB = os.getenv("DB_NAME")

# --- ENGINE PARA O BANCO ---

DATABASE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DB}?charset=utf8mb4"
engine = create_engine(
    DATABASE_URL,
    echo=True)

# --- BASE ORM ---
Base = declarative_base()

# --- SESSION FACTORY ---
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
