from app.repositories.userRepository import UserRepository
from app.repositories.authRepository import AuthRepository

def test_user_repository_stub():
    repo = UserRepository(session=None)
    user = repo.get_by_id(1)
    assert user["id"] == 1
    assert user["username"] == "stub_user"

def test_auth_repository_stub():
    repo = AuthRepository(session=None)
    assert repo.verify_credentials("admin", "admin") is True
    assert repo.verify_credentials("user", "wrong") is False
