import logging
from app.repositories.baseRepository import BaseRepository

logger = logging.getLogger(__name__)

class UserRepository(BaseRepository):
    """Stub de repositório de usuário (sem consultas reais ainda)."""

    def get_by_id(self, user_id):
        logger.debug(f"Buscando usuário por ID: {user_id}")
        # Placeholder: retorna stub
        user = {"id": user_id, "username": "stub_user"}
        logger.debug(f"Usuário encontrado: {user}")
        return user