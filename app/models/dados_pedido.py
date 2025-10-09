from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class DadosPedido(Base):
    __tablename__ = "dados_pedido"

    id_pedido = Column(Integer, primary_key=True, autoincrement=True)
    funcionario_pedido = Column(Integer, ForeignKey("funcionarios.idfuncionarios"), nullable=False)
    datetime_pedido = Column(DateTime, default=datetime.utcnow)
    nome_projeto = Column(String(45), nullable=False)
    nome_lista = Column(String(45), nullable=False)

    # Relacionamentos
    funcionario = relationship("Funcionario", back_populates="pedidos_criados")
    pedidos = relationship(
        "Pedido",
        back_populates="dados_pedido",
        cascade="all, delete-orphan"
    )
