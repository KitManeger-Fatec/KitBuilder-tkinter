# config/database/validators.py
import os
from app.config.exceptions import DatabaseConfigurationError

class DatabaseConfigValidator:
    """Valida se variáveis obrigatórias estão presentes antes de iniciar."""

    REQUIRED_VARS = ["DB_TYPE", "DB_USER", "DB_PASS", "DB_HOST", "DB_PORT", "DB_NAME"]

    @classmethod
    def validate(cls):
        missing = [var for var in cls.REQUIRED_VARS if not os.getenv(var)]
        if missing:
            raise DatabaseConfigurationError(
                f"Variáveis de ambiente ausentes: {', '.join(missing)}"
            )
