import logging
from app.database import SessionLocal
from app.models.funcionarios import Funcionario

logger = logging.getLogger(__name__)

class PedidoViewController:
    usuario_logado = None   # dict com campos: id, nome, cargo, nivel
    nome_projeto = ""
    nome_lista = ""
    itens = []  # lista de dicionários representando itens do pedido

    @classmethod
    def set_usuario_logado(cls, usuario_id: int):
        """Carrega o usuário do banco e guarda no estado global."""
        session = SessionLocal()
        logger.info(f"Carregando usuário com id={usuario_id} do banco de dados")
        try:
            funcionario = session.query(Funcionario).filter_by(idfuncionarios=usuario_id).first()
            if not funcionario:
                logger.error(f"Funcionário com id={usuario_id} não encontrado")
                return

            cls.usuario_logado = {
                "id": funcionario.idfuncionarios,
                "nome": funcionario.nome_funcionario,
                "cargo": funcionario.cargo_funcionario,
                "nivel": funcionario.nivel_funcionario
            }

            logger.info(f"Usuário ID {usuario_id} carregado para o estado do pedido.")
            # 🔧 se existir view associada, atualiza labels dinamicamente
            if hasattr(cls, "view") and cls.view:
                cls.view.usuario.configure(text=cls.state.usuario_logado["nome"])
                cls.view.cargo.configure(text=cls.state.usuario_logado["cargo"])
                cls.view.nivel.configure(text=cls.state.usuario_logado["nivel"])

        except Exception as e:
            logger.error(f"Erro ao carregar usuário para o estado: {e}")
        finally:
            session.close()


    @classmethod
    def add_item(cls, codigo, descricao, quantidade, medida, fabricante, codigo_fabricante):
        cls.itens.append({
            "codigo": codigo,
            "produto": descricao,
            "quantidade": quantidade,
            "medida": medida,
            "fabricante": fabricante,
            "codigo_fabricante": codigo_fabricante
        })
        logger.info(f"Item adicionado: {codigo}, qtd={quantidade}, fab={fabricante}")

    @classmethod
    def remover_item(cls, codigo):
        before = len(cls.itens)
        cls.itens = [i for i in cls.itens if i["codigo"] != codigo]
        after = len(cls.itens)
        logger.info(f"Item removido: {codigo}, {before-after} removido(s)")

    @classmethod
    def atualizar_quantidade(cls, codigo, nova_qtd):
        """Atualiza a quantidade de um item baseado apenas no código."""
        logger.info(f"Atualizando quantidade do item {codigo} para {nova_qtd}")
        found = False
        for item in cls.itens:
            if item["codigo"] == codigo:
                item["quantidade"] = nova_qtd
                found = True
                break
        if not found:
            logger.warning("Item não encontrado para atualização de quantidade.")

        # Atualiza a view se existir
        if cls.view:
            cls.view.atualizar_itens()
    @classmethod
    def atualizar_nome_projeto(cls, nome: str):
        """Atualiza o nome do projeto no AppState."""
        AppState.nome_projeto = nome
        logger.info(f"Nome do projeto atualizado para: {nome}")

    @classmethod
    def atualizar_nome_lista(cls, nome: str):
        """Atualiza o nome da lista no AppState."""
        AppState.nome_lista = nome
        logger.info(f"Nome da lista atualizado para: {nome}")

class AppState:
    """Armazena estado global da aplicação"""
    projeto_nome = ""
    lista_nome = ""
    funcionario_logado_id = None