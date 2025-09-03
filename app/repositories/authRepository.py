import logging
from app.repositories.baseRepository import BaseRepository

logger = logging.getLogger(__name__)


class AuthRepository(BaseRepository):
    """Stub de repositório de autenticação."""

    def verify_credentials(self, username, password):
        logger.debug(f"Verificando credenciais no repositório para usuário: {username}")
        # Placeholder: simula validação
        resultado = username == "admin" and password == "admin"

        if resultado:
            logger.info(f"Credenciais válidas no repositório para usuário: {username}")
        else:
            logger.warning(f"Credenciais inválidas no repositório para usuário: {username}")

        return resultado