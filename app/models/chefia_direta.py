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

    def to_dict(self):
        return {
            "id_confere": self.id_confere,
            "id_funcionario": self.id_funcionario,
            "id_chefia": self.id_chefia,
            "funcionario_nome": self.funcionario.nome_funcionario if self.funcionario else None,
            "chefe_nome": self.chefe.nome_funcionario if self.chefe else None,
        }