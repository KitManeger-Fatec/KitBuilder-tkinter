from app.repositories.baseRepository import BaseRepository

class UserRepository(BaseRepository):
    """Stub de repositório de usuário (sem consultas reais ainda)."""

    def get_by_id(self, user_id):
        # Placeholder: retorna stub
        return {"id": user_id, "username": "stub_user"}
