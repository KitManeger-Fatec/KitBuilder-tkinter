from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Pedido(Base):
    __tablename__ = "pedido"

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Pedido(Base):
    __tablename__ = "pedido"


    idpedido = Column(Integer, primary_key=True, autoincrement=True)
    funcionario_pedido = Column(
        "Funcionario_pedido",        # nome exato da coluna no MySQL
        Integer,
        ForeignKey("db_listaCompras.funcionarios.idfuncionarios"),
        nullable=False
    )
    quantidade = Column(Integer, nullable=False)
    codigo = Column(String(20), nullable=False)
    produto = Column(String(200), nullable=False)
    aceito = Column(Boolean)  # TINYINT → Boolean

    # --- Relação (opcional) ---
    funcionario = relationship("Funcionario", back_populates="pedidos")