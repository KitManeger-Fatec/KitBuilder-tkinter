from sqlalchemy import Column, Integer, String, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from app.database import Base

class Pedido(Base):
    __tablename__ = "pedido"

    linha_pedido = Column(Integer, primary_key=True, autoincrement=True)
    id_dados_pedido = Column(Integer, ForeignKey("dados_pedido.id_pedido"), nullable=False)
    aceito = Column(SmallInteger, nullable=True)
    quantidade = Column(Integer, nullable=False)
    medida = Column(String(20), nullable=False)
    codigo = Column(String(20), nullable=False)
    produto = Column(String(200), nullable=False)
    fabricante = Column(String(45), nullable=True)
    cod_fabricante = Column(String(45), nullable=True)

    dados_pedido = relationship("DadosPedido", back_populates="pedidos")

    def to_dict(self):
        return {
            "aceito": self.aceito,
            "linha_pedido": self.linha_pedido,
            "quantidade": self.quantidade,
            "medida": self.medida,
            "codigo": self.codigo,
            "produto": self.produto,
            "fabricante": self.fabricante,
            "cod_fabricante": self.cod_fabricante,
        }
