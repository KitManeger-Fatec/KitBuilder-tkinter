from sqlalchemy import Column, Integer, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from app.database import Base

class PedidoAprova(Base):
    __tablename__ = "pedido_aprova"

    idpedido_aprova = Column(Integer, primary_key=True, autoincrement=True)
    pedido_idpedido = Column(Integer, ForeignKey("pedido.linha_pedido"), nullable=False)
    id_chefia_aprova = Column(Integer, ForeignKey("chefia_direta.id_confere"), nullable=False)
    pedido_aprovado = Column(SmallInteger, nullable=True)

    # Relacionamentos
    pedido = relationship("Pedido", backref="aprovacoes")
    chefia = relationship("ChefiaDireta", backref="aprovacoes")
