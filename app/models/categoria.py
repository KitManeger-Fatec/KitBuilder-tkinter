from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base  # importa Base de database.py
from .subcategoria import Subcategoria  # apenas se precisar do relacionamento

class Categoria(Base):
    __tablename__ = "categorias"

    id_categoria = Column(Integer, primary_key=True, autoincrement=True)
    nome_classe = Column(String(45), nullable=False)
    nome_categoria = Column(String(45), nullable=False, unique=True)
    imagem_categoria = Column(String(45), nullable=True)

    # Relacionamento
    subcategorias = relationship("Subcategoria", back_populates="categoria")
