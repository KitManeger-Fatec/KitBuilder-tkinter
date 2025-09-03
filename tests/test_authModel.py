# tests/test_authModel.py
from app.models import AuthModel

def test_verificar_credenciais_corretas():
    model = AuthModel()
    assert model.verificar_credenciais("test_user", "test_pass") == True

def test_verificar_credenciais_incorretas():
    model = AuthModel()
    assert model.verificar_credenciais("wrong", "credentials") == False