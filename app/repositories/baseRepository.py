import logging

logger = logging.getLogger(__name__)

class BaseRepository:
    """Classe base para repositórios (sem query real ainda)."""

    def __init__(self, session):
        logger.debug(f"Inicializando BaseRepository com sessão: {session}")
        self.session = session