from app.repositories.baseRepository import BaseRepository

class AuthRepository(BaseRepository):
    """Stub de repositório de autenticação."""

    def verify_credentials(self, username, password):
        # Placeholder: simula validação
        return username == "admin" and password == "admin"
