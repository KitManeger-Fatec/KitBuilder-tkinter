from sqlalchemy import (
    Column, Integer, String, Boolean, Date, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Pedido(Base):
    __tablename__ = "pedido"

    linha_pedido = Column(Integer, primary_key=True, autoincrement=True)
    id_dados_pedido = Column(Integer, ForeignKey("dados_pedido.id_pedido"), nullable=False)
    aceito = Column(Boolean)           # TINYINT -> Boolean
    quantidade = Column(Integer, nullable=False)
    medida = Column(String(20), nullable=False)
    codigo = Column(String(20), nullable=False)
    produto = Column(String(200), nullable=False)
    fabricante = Column(String(45))
    cod_fabricante = Column(String(45))

    dados_pedido = relationship("DadosPedido", back_populates="itens")
    aprovacoes = relationship("PedidoAprova", back_populates="pedido", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Pedido(linha={self.linha_pedido}, produto='{self.produto}')>"