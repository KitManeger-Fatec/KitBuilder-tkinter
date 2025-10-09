from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ChefiaDireta(Base):
    __tablename__ = "chefia_direta"

    id_confere = Column(Integer, primary_key=True, autoincrement=True)
    id_funcionario = Column(Integer, ForeignKey("funcionarios.idfuncionarios"), nullable=False)
    id_chefia = Column(Integer, ForeignKey("funcionarios.idfuncionarios"), nullable=False)

    funcionario = relationship("Funcionario", foreign_keys=[id_funcionario], back_populates="chefia_direta")
    chefe = relationship("Funcionario", foreign_keys=[id_chefia], back_populates="subordinacoes")
