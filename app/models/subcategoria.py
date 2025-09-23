from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Subcategoria(Base):
    __tablename__ = "subcategoria"

    idsubcategoria = Column(Integer, primary_key=True)
    nome_subcategoria = Column(String(45), nullable=False)
    db_subcategoria = Column(String(45), nullable=False)
    descricao_subcategoria = Column(String(100), nullable=False)
    unidade_medida = Column(String(20), nullable=False)
    categorias_id_categoria = Column(Integer, ForeignKey("categorias.id_categoria"))

    categoria = relationship("Categoria", back_populates="subcategorias")
