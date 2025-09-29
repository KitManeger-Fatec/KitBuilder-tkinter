from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Funcionario(Base):
    __tablename__ = "funcionarios"
    __table_args__ = {"schema": "db_listaCompras"}

    idfuncionarios = Column(Integer, primary_key=True, autoincrement=True)
    nome_funcionario = Column(String(60), nullable=False)
    cargo_funcionario = Column(String(45), nullable=False)
    nivel_funcionario = Column(Integer, nullable=False)
    usuario_funcionario = Column(String(45), nullable=False)
    senha_funcionario = Column(String(128), nullable=False)
    email_funcionario = Column(String(100), nullable=False)
    foi_criado_em = Column(Date, nullable=False)
    ultimo_acesso_em = Column(DateTime, nullable=False)

    # relacionamento reverso com ChefiaDireta
    chefias = relationship(
        "ChefiaDireta",
        foreign_keys="ChefiaDireta.id_funcionario",
        back_populates="funcionario"
    )
    chefias_como_chefia = relationship(
        "ChefiaDireta",
        foreign_keys="ChefiaDireta.id_chefia",
        back_populates="chefia"
    )
