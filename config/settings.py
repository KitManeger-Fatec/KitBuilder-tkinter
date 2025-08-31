# config/settings.py
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

USUARIO_PADRAO = os.getenv("USER", "admin")
SENHA_PADRAO = os.getenv("PASSWORD", "admin")

# Variável global acessível
VAR_GLOBAL = 10

# Configurações gerais
APP_TITLE = "Meu Sistema CustomTkinter"
FULLSCREEN = True
