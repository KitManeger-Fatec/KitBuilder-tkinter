import logging

logger = logging.getLogger(__name__)


class AppRouter:
    """
    Router simples que centraliza a navegação entre views na aplicação.
    """

    def __init__(self, root):
        logger.debug("Inicializando AppRouter")
        self.root = root
        self.controller = None
        self.current_view = None

    def set_controller(self, controller):
        """Vincula o controller que o router vai usar para criar as views."""
        logger.debug("Definindo controller no router")
        self.controller = controller

    def clear_root(self):
        """Dá um destroy em todos os filhos diretos do root (limpa a tela)."""
        logger.debug("Limpando janela principal")
        for child in list(self.root.winfo_children()):
            try:
                child.destroy()
            except Exception as e:
                logger.error(f"Erro ao destruir widget: {e}")

    def show_login(self):
        """
        Limpa a root e cria a view de login via controller.
        Mantém referência em current_view.
        """
        logger.info("Navegando para tela de login")
        self.clear_root()
        if not self.controller:
            logger.error("Controller não definido no router")
            return None

        try:
            self.controller.destruir_view_login()
        except Exception as e:
            logger.warning(f"Erro ao destruir view de login anterior: {e}")

        try:
            self.controller.criar_view_login()
            self.current_view = self.controller.view
            logger.debug("View de login criada com sucesso")
            return self.current_view
        except Exception as e:
            logger.error(f"Erro ao criar view de login: {e}")
            return None

    def show_main(self):
        """
        Limpa a root e cria a main view via controller.
        Mantém referência em current_view.
        """
        logger.info("Navegando para tela principal")
        self.clear_root()
        if not self.controller:
            logger.error("Controller não definido no router")
            return None

        try:
            self.controller.criar_main_view()
            self.current_view = self.controller.main_view
            logger.debug("View principal criada com sucesso")
            return self.current_view
        except Exception as e:
            logger.error(f"Erro ao criar view principal: {e}")
            return None
        
    def show_pedido(self):
        self.clear_root()
        try:
            from app.views.pedidoView import PedidoView
            self.current_view = PedidoView(self.root, router=self)
            self.current_view.atualizar_itens()
            self.current_view.pack(fill="both", expand=True)
        except Exception as e:
            logger.error(f"Erro ao criar view de pedidos: {e}")

            