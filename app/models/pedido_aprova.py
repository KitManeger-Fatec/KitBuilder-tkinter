from sqlalchemy import (
    Column, Integer, String, Boolean, Date, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class PedidoAprova(Base):
    __tablename__ = "pedido_aprova"

    idpedido_aprova = Column(Integer, primary_key=True, autoincrement=True)
    pedido_idpedido = Column(Integer, ForeignKey("pedido.linha_pedido"), nullable=False)
    id_chefia_aprova = Column(Integer, ForeignKey("chefia_direta.id_funcionario"), nullable=False)
    pedido_aprovado = Column(Boolean)

    pedido = relationship("Pedido", back_populates="aprovacoes")

    def __repr__(self):
        return f"<PedidoAprova(id={self.idpedido_aprova}, aprovado={self.pedido_aprovado})>"