from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Pedido(Base):
    __tablename__ = "pedido"

    idpedido = Column(Integer, primary_key=True, autoincrement=True)
    quantidade = Column(Integer, nullable=False)
    codigo = Column(String(20), nullable=False)
    produto = Column(String(200), nullable=False)
    aceito = Column(Boolean)
