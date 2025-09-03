class DatabaseConfigurationError(Exception):
    """Erro de configuração do banco (ex: variáveis de ambiente faltando)."""
    pass


class DatabaseConnectionError(Exception):
    """Erro ao conectar ao banco de dados."""
    pass
