# models/authModel.py
import os
from config.settings import USUARIO_PADRAO, SENHA_PADRAO

class AuthModel:
    @staticmethod
    def verificar_credenciais(usuario, senha):
        expected_user = os.getenv("USERNAME", USUARIO_PADRAO)
        expected_pass = os.getenv("PASSWORD", SENHA_PADRAO)
        return usuario == expected_user and senha == expected_pass
