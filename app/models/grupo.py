from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Grupo(Base):
    __tablename__ = "grupos"

    idClasses = Column(Integer, primary_key=True, autoincrement=True)
    nome_classe = Column(String(45), nullable=False, unique=True)

    # Relacionamento: um grupo tem várias categorias
    categorias = relationship("Categoria", back_populates="grupo")