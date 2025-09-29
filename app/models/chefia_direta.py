from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ChefiaDireta(Base):
    __tablename__ = "chefia_direta"
    __table_args__ = {"schema": "db_listaCompras"}

    id_confere = Column(Integer, primary_key=True, autoincrement=True)
    id_funcionario = Column(
        Integer,
        ForeignKey("db_listaCompras.funcionarios.idfuncionarios"),
        nullable=False
    )
    id_chefia = Column(
        Integer,
        ForeignKey("db_listaCompras.funcionarios.idfuncionarios"),
        nullable=False
    )

    # relacionamentos
    funcionario = relationship(
        "Funcionario",
        foreign_keys=[id_funcionario],
        back_populates="chefias"
    )
    chefia = relationship(
        "Funcionario",
        foreign_keys=[id_chefia],
        back_populates="chefias_como_chefia"
    )
