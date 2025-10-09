from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Funcionario(Base):
    __tablename__ = "funcionarios"

    idfuncionarios = Column(Integer, primary_key=True, autoincrement=True)
    nome_funcionario = Column(String(60), nullable=False)
    cargo_funcionario = Column(String(45), nullable=False)
    nivel_funcionario = Column(Integer, nullable=False)
    usuario_funcionario = Column(String(45), nullable=False)
    senha_funcionario = Column(String(128), nullable=False)
    email_funcionario = Column(String(100), nullable=False)
    foi_criado_em = Column(DateTime, default=datetime.utcnow)
    ultimo_acesso_em = Column(DateTime, default=datetime.utcnow)

    # Relacionamento com DadosPedido
    pedidos_criados = relationship("DadosPedido", back_populates="funcionario")

    # Relacionamento chefia direta
    chefia_direta = relationship(
        "ChefiaDireta",
        foreign_keys="ChefiaDireta.id_funcionario",
        back_populates="funcionario"
    )
    subordinacoes = relationship(
        "ChefiaDireta",
        foreign_keys="ChefiaDireta.id_chefia",
        back_populates="chefe"
    )
