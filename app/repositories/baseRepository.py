class BaseRepository:
    """Classe base para repositórios (sem query real ainda)."""

    def __init__(self, session):
        self.session = session
