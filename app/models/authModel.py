import os
import logging
from app.config.settings import USUARIO_PADRAO, SENHA_PADRAO

logger = logging.getLogger(__name__)


class AuthModel:
    @staticmethod
    def verificar_credenciais(usuario, senha):
        logger.debug(f"Verificando credenciais para usuário: {usuario}")
        expected_user = os.getenv("USERNAME", USUARIO_PADRAO)
        expected_pass = os.getenv("PASSWORD", SENHA_PADRAO)

        # Por segurança, não logamos a senha esperada
        resultado = usuario == expected_user and senha == expected_pass

        if resultado:
            logger.info(f"Credenciais válidas para usuário: {usuario}")
        else:
            logger.warning(f"Credenciais inválidas para usuário: {usuario},{expected_user},{expected_pass},{senha}")
            print(f"username atual: {os.getenv("USERNAME")}")
        return resultado