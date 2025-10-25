
import logging
from sqlalchemy import Table, MetaData, select
from app.database import engine
from collections import defaultdict
from app.database import SessionLocal
from app.models.funcionarios import Funcionario

logger = logging.getLogger(__name__)

class CadastroViewController:
    def __init__(self):
        self.usuario_logado = None
        self.cadastro_view = None


    def set_usuario_logado(self, usuario_id: int):
        # Aqui você pega o usuário do banco ou de algum estado global
        self.usuario_logado = self.obter_usuario_por_id(usuario_id)

    def get_usuario_logado(self):
        return self.usuario_logado

    def obter_usuario_por_id(self, usuario_id: int):
        """Busca usuário no banco pelo ID"""
        with SessionLocal() as session:
            usuario = session.query(Funcionario).filter_by(idfuncionarios=usuario_id).first()
            if not usuario:
                logger.warning(f"Usuário ID {usuario_id} não encontrado.")
            return usuario

    @staticmethod
    def validar_dados_cadastro(dados):
        """Valida os dados fornecidos para cadastro de funcionário."""
        erros = []
        if not dados.get("nome") or len(dados["nome"]) < 3:
            erros.append("Nome deve ter pelo menos 3 caracteres.")
        if not dados.get("email") or "@" not in dados["email"]:
            erros.append("Email inválido.")
        if not dados.get("senha") or len(dados["senha"]) < 6:
            erros.append("Senha deve ter pelo menos 6 caracteres.")
        # Adicione mais validações conforme necessário
        if erros:
            logger.warning(f"Validação de cadastro falhou: {erros}")
        else:
            logger.debug("Dados de cadastro validados com sucesso")
        return erros
    
    @staticmethod
    def obter_cargos_unicos():
        MetaData_obj = MetaData()
        funcionarios = Table("funcionarios", MetaData_obj, autoload_with=engine)  
        stmt = select(funcionarios.c.cargo_funcionario).distinct()  
        try:
            with engine.connect() as conn:
                result = conn.execute(stmt).fetchall()
            cargos = [row.cargo_funcionario for row in result]
            logger.debug(f"Cargos únicos obtidos: {cargos}")
            return cargos
        except Exception as e:
            logger.error(f"Erro ao buscar cargos únicos: {e}")
            return []
        
    @staticmethod
    def exibir_dados_cadastro(dados: dict):
        """Exibe os dados do formulário enviados pela View."""
        print("\n=== DADOS DO FORMULÁRIO ===")
        for campo, valor in dados.items():
            print(f"{campo.capitalize()}: {valor}")
        print("===========================\n")

        logger.info(f"Dados exibidos: {dados}")








