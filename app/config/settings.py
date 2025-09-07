# config/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis do .env com caminho absoluto
env_path = Path('') / '.env'
load_dotenv(dotenv_path=env_path)

USUARIO_PADRAO = os.getenv("USERNAME", "admin")
SENHA_PADRAO = os.getenv("PASSWORD", "admin")
# Variável global acessível
VAR_GLOBAL = 10

# Configs do app
APP_TITLE = os.getenv("APP_TITLE", "S.A.G.A - Kit Manager")
FULLSCREEN = os.getenv("FULLSCREEN", "True").lower() in ("1", "true", "yes")

# Exemplo: nome da marca para whitelabel
BRAND_NAME = os.getenv("BRAND_NAME", "Minha Empresa")

# Configuração de logging (apenas define a variável, não executa)
SETUP_LOGGING = os.getenv("SETUP_LOGGING", "True").lower() in ("1", "true", "yes")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()