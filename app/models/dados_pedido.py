from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Boolean
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class DadosPedido(Base):
    __tablename__ = "dados_pedido"

    id_pedido = Column(Integer, primary_key=True, autoincrement=True)
    funcionario_pedido = Column(Integer, ForeignKey("funcionarios.idfuncionarios"), nullable=False)
    datetime_pedido = Column(String(45), nullable=False)  # ou DateTime se preferir
    nome_projeto = Column(String(45), nullable=False)
    nome_lista = Column(String(45), nullable=False)

    # relacionamento 1:N com itens de pedido
    itens = relationship("Pedido", back_populates="dados_pedido", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<DadosPedido(id={self.id_pedido}, projeto='{self.nome_projeto}')>"