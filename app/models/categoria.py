from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from .subcategoria import Subcategoria  # se precisar do relacionamento
from .grupo import Grupo  # novo relacionamento com grupos

class Categoria(Base):
    __tablename__ = "categorias"

    id_categoria = Column(Integer, primary_key=True, autoincrement=True)
    Classes_idClasses = Column(
        Integer,
        ForeignKey("grupos.idClasses"),
        nullable=False
    )
    nome_categoria = Column(String(45), nullable=False, unique=True)
    imagem_categoria = Column(String(45), nullable=True)

    # Relacionamentos
    subcategorias = relationship("Subcategoria", back_populates="categoria")
    grupo = relationship("Grupo", back_populates="categorias")