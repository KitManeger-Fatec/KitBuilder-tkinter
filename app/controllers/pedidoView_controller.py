import logging
from datetime import datetime
from app.database import SessionLocal
from app.models.funcionarios import Funcionario
from app.models.dados_pedido import DadosPedido
from app.models.pedido import Pedido    
from app.utils.session_manager import SessionManager
logger = logging.getLogger(__name__)


class PedidoViewController:
    """Controlador de estado e lógica dos pedidos"""
    usuario_logado = None
    nome_projeto = ""
    nome_lista = ""
    itens = []  # lista de dicionários representando itens do pedido
    view = None  # ponteiro opcional para a view

    # ================================
    # MÉTODOS DE ESTADO
    # ================================
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

            # Atualiza labels da view (se existir)
            if cls.view:
                cls.view.usuario.configure(text=cls.usuario_logado["nome"])
                cls.view.cargo.configure(text=cls.usuario_logado["cargo"])
                cls.view.nivel.configure(text=cls.usuario_logado["nivel"])

        except Exception as e:
            logger.error(f"Erro ao carregar usuário para o estado: {e}")
        finally:
            session.close()

    # ================================
    # MÉTODOS DE ITENS
    # ================================
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
        antes = len(cls.itens)
        cls.itens = [i for i in cls.itens if i["codigo"] != codigo]
        depois = len(cls.itens)
        logger.info(f"Item removido: {codigo}, {antes - depois} removido(s)")

    @classmethod
    def atualizar_quantidade(cls, codigo, nova_qtd):
        """Atualiza a quantidade de um item baseado apenas no código."""
        logger.info(f"Atualizando quantidade do item {codigo} para {nova_qtd}")
        for item in cls.itens:
            if item["codigo"] == codigo:
                item["quantidade"] = nova_qtd
                break
        else:
            logger.warning("Item não encontrado para atualização de quantidade.")

        if cls.view:
            cls.view.atualizar_itens()

    # ================================
    # MÉTODOS DE PROJETO/LISTA
    # ================================
    @classmethod
    def atualizar_nome_projeto(cls, nome: str):
        cls.nome_projeto = nome
        logger.info(f"Nome do projeto atualizado para: {nome}")

    @classmethod
    def atualizar_nome_lista(cls, nome: str):
        cls.nome_lista = nome
        logger.info(f"Nome da lista atualizado para: {nome}")

    # ================================
    # FINALIZAR PEDIDO
    # ================================
    @classmethod
    def finalizar_pedido(cls):
        logger.info("Tentando finalizar pedido...")

        if not AppState.projeto_nome or not AppState.lista_nome:
            logger.error("Nome do projeto e nome da lista são obrigatórios.")
            raise ValueError("Nome do projeto e nome da lista são obrigatórios")

        if not cls.usuario_logado:
            logger.error("Usuário não logado.")
            raise ValueError("Usuário não logado")

        session = SessionLocal()
        try:
            # Cria o cabeçalho (DadosPedido)
            dados_pedido = DadosPedido(
                funcionario_pedido=cls.usuario_logado["id"],
                datetime_pedido=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                nome_projeto=AppState.projeto_nome,
                nome_lista=AppState.lista_nome
            )
            session.add(dados_pedido)
            session.commit()
            logger.debug(f"DadosPedido criado com ID: {dados_pedido.id_pedido}")

            # Adiciona os itens vinculados
            for item in cls.itens:
                pedido = Pedido(
                    id_dados_pedido=dados_pedido.id_pedido,
                    aceito = True,
                    quantidade=item["quantidade"],
                    medida=item["medida"],
                    codigo=item["codigo"],
                    produto=item["produto"],
                    fabricante=item.get("fabricante", ""),
                    cod_fabricante=item.get("codigo_fabricante", "")
                )
                session.add(pedido)

            session.commit()
            logger.info(f"Pedido finalizado com sucesso. {len(cls.itens)} itens salvos.")

            # Limpa estado local e global
            cls.itens.clear()
            AppState.projeto_nome = ""
            AppState.lista_nome = ""

            if cls.view:
                cls.view.atualizar_itens()

        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao finalizar pedido e salvar no BD: {e}")
            raise
        finally:
            session.close()



# Estado global opcional
class AppState:
    """Armazena estado global da aplicação"""
    projeto_nome = ""
    lista_nome = ""
    funcionario_logado_id = SessionManager.get_usuario_id()
