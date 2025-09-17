# app/models/renomear.py
from sqlalchemy import Column, Integer, String
from app.database import Base  # <-- corrigido

class Renomear(Base):
    __tablename__ = "Renomear"
    idRenomear = Column(Integer, primary_key=True, autoincrement=True)
    renomear_coluna = Column(String(45), unique=True, nullable=False)
    renomear_colunaRenomeada = Column(String(45), nullable=False)
