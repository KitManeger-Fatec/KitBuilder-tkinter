# app/models/__init__.py

from app.database import Base

# Modelos simples (sem dependências cruzadas)
from .grupo import Grupo
from .categoria import Categoria
from .subcategoria import Subcategoria
from .renomear import Renomear
from .authModel import AuthModel
from .funcionarios import Funcionario
from .chefia_direta import ChefiaDireta

# Modelos com dependências entre si
# IMPORTANTE: importar ambos, Pedido e DadosPedido, na sequência
from .pedido import Pedido
from .dados_pedido import DadosPedido

# Outros modelos dependentes
from .pedido_aprova import PedidoAprova

__all__ = [
    "Base",
    "Grupo",
    "Categoria",
    "Subcategoria",
    "Renomear",
    "AuthModel",
    "Funcionario",
    "ChefiaDireta",
    "Pedido",
    "DadosPedido",
    "PedidoAprova",
]
