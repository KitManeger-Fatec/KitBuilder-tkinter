# models/authModel.py
from config.settings import USUARIO_PADRAO, SENHA_PADRAO

class AuthModel:
    @staticmethod
    def verificar_credenciais(usuario, senha):
        return usuario == USUARIO_PADRAO and senha == SENHA_PADRAO
