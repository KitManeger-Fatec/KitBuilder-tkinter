
import logging
import bcrypt
from sqlalchemy import Table, MetaData, select
from app.database import engine
from collections import defaultdict
from app.database import SessionLocal
from app.models.funcionarios import Funcionario
from app.models.chefia_direta import ChefiaDireta
from sqlalchemy.exc import SQLAlchemyError

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
    def obter_nivel(id_funcionario: int):
        """
        Busca o nível atual de um funcionário e gera uma lista crescente
        até o nível anterior ao atual, com 'Escolher Nível' no início.
        """
        try:
            if id_funcionario is None:
                raise ValueError("id_funcionario não informado")

            meta = MetaData()
            funcionarios = Table("funcionarios", meta, autoload_with=engine)

            stmt = select(funcionarios.c.nivel_funcionario).where(
                funcionarios.c.idfuncionarios == id_funcionario
            )

            with engine.connect() as conn:
                result = conn.execute(stmt).first()

            if not result:
                logger.warning(f"Nenhum funcionário encontrado com ID {id_funcionario}")
                return ["Escolher Nível", "1"]

            nivel_atual = result[0]

            # gera níveis de 1 até (nivel_atual - 1)
            if nivel_atual > 1:
                niveis = [str(n) for n in range(1, nivel_atual)]
            else:
                niveis = ["1"]  # se for nível 1, não há níveis abaixo

            # adiciona a opção inicial
            niveis.insert(0, "Escolher Nível")

            logger.debug(f"Nível atual: {nivel_atual}, níveis disponíveis: {niveis}")
            return niveis

        except Exception as e:
            logger.error(f"Erro ao buscar nível do funcionário: {e}")
            return ["Escolher Nível", "1"]

    
    @staticmethod
    def exibir_dados_cadastro(dados: dict):
        """Exibe os dados do formulário enviados pela View."""
        print("\n=== DADOS DO FORMULÁRIO ===")
        for campo, valor in dados.items():
            print(f"{campo.capitalize()}: {valor}")
        print("===========================\n")

        logger.info(f"Dados exibidos: {dados}")

    @staticmethod
    def usuario_existe(usuario: str) -> bool:
        """Verifica se já existe um usuário com o mesmo login no banco."""
        if not usuario.strip():
            return False  # campo vazio não considera existente

        try:
            with SessionLocal() as session:
                stmt = select(Funcionario).where(Funcionario.usuario_funcionario == usuario)
                existe = session.scalar(stmt) is not None
                return existe
        except Exception as e:
            logger.error(f"Erro ao verificar usuário no banco: {e}")
            return False


    @staticmethod
    def salvar_funcionario(dados: dict, chefes_selecionados: list[str]) -> bool:
        """
        Salva um novo funcionário e associa chefes selecionados.
        chefes_selecionados = ["Nome Chefe - Cargo", ...]
        """
        try:
            senha_bytes = dados["senha"].encode("utf-8")
            hashed = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())

            with SessionLocal() as session:
                # --- cria funcionário ---
                novo_funcionario = Funcionario(
                    nome_funcionario=dados["nome"].strip(),
                    cargo_funcionario=dados["cargo"].strip(),
                    nivel_funcionario=int(dados["nivel"]),
                    usuario_funcionario=dados["usuario"].strip(),
                    senha_funcionario=hashed.decode("utf-8"),
                    email_funcionario=dados["email"].strip()
                )
                session.add(novo_funcionario)
                session.flush()  # garante que novo_funcionario.idfuncionarios está disponível

                # --- associa chefes ---
                for chefe_texto in chefes_selecionados:
                    nome = chefe_texto.split(" - ")[0].strip()
                    stmt = select(Funcionario).where(Funcionario.nome_funcionario == nome)
                    chefe_obj = session.scalar(stmt)
                    if chefe_obj and chefe_obj.idfuncionarios != novo_funcionario.idfuncionarios:
                        rel = ChefiaDireta(
                            id_funcionario=novo_funcionario.idfuncionarios,
                            id_chefia=chefe_obj.idfuncionarios
                        )
                        session.add(rel)

                session.commit()
                logger.info(f"Funcionário '{novo_funcionario.nome_funcionario}' cadastrado com sucesso com {len(chefes_selecionados)} chefes.")
                return True

        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao salvar funcionário com chefes: {e}")
            return False
        
    @staticmethod
    def limpar_formulario(view):
        """Limpa os campos do formulário recebendo a View como parâmetro."""
        try:
            view.nome_entry.delete(0, "end")
            view.cpf_entry.delete(0, "end")
            view.usuario_entry.delete(0, "end")
            view.email_entry.delete(0, "end")
            view.senha_entry.delete(0, "end")
            view.confirmar_senha_entry.delete(0, "end")
            view.novo_cargo_entry.delete(0, "end")
            view.cargo_combobox.set(view.cargo_combobox.values[0])
            view.nivel_combobox.set(view.nivel_combobox.values[0])
            view.textbox_selecionados.delete("0.0", "end")
            view.chefes_selecionados.clear()
        except Exception as e:
            logger.error(f"Erro ao limpar formulário: {e}")

# def verificar_senha(senha_digitada, senha_armazenada):
#     return bcrypt.checkpw(senha_digitada.encode('utf-8'), senha_armazenada.encode('utf-8'))