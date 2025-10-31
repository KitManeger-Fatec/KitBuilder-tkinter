# app/utils/session_manager.py
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class SessionManager:
    """
    Armazena e gerencia o ID do usuário logado.
    Acesso global (Singleton-like).
    """
    _usuario_id: Optional[int] = None

    @classmethod
    def set_usuario_id(cls, user_id: int):
        cls._usuario_id = user_id
        logger.info(f"Usuário logado com ID: {user_id}")

    @classmethod
    def get_usuario_id(cls) -> Optional[int]:
        return cls._usuario_id

    @classmethod
    def limpar_sessao(cls):
        logger.info("Sessão do usuário encerrada")
        cls._usuario_id = None
