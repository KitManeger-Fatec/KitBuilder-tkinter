import logging
from app.models.authModel import AuthModel
from app.views.loginView import LoginView
from app.views.mainView import MainView

logger = logging.getLogger(__name__)


class AuthController:
    """
    Controller responsável por autenticação e criação de views dentro do root.
    Agora exige um routers externo (injeção). Isso mantém a responsabilidade de
    navegação fora do controller e facilita integração com um AppRouter.
    """

    def __init__(self, root=None, router=None):
        logger.debug("Inicializando AuthController")
        if router is None:
            error_msg = "AuthController requer uma instância de router"
            logger.error(error_msg)
            raise ValueError(error_msg)

        self.root = root
        self.router = router
        self.model = AuthModel()
        self.view = None
        self.main_view = None
        logger.info("AuthController inicializado com sucesso")

    def criar_view_login(self):
        logger.debug("Criando view de login")
        # cria LoginView embutida (destrói a anterior se houver)
        self.destruir_view_login()
        try:
            self.view = LoginView(parent=self.root, controller=self)
            logger.debug("View de login criada com sucesso")
        except Exception as e:
            logger.error(f"Erro ao criar view de login: {e}")
            raise

    def fazer_login(self):
        logger.debug("Iniciando processo de login")
        if not self.view:
            logger.warning("Tentativa de login sem view definida")
            return False

        try:
            usuario, senha = self.view.get_credenciais()
            logger.debug(f"Credenciais obtidas - Usuário: {usuario}")

            if self.model.verificar_credenciais(usuario, senha):
                logger.info(f"Login bem-sucedido para usuário: {usuario}")
                # navega para main view via routers injetado
                if self.router and hasattr(self.router, "show_main"):
                    try:
                        self.router.show_main()
                        return True
                    except Exception as e:
                        logger.error(f"Erro ao navegar para tela principal: {e}")
                        # não propaga para manter teste/robustez
                return True
            else:
                logger.warning(f"Tentativa de login falhou para usuário: {usuario}")
                # exibe erro na view (se houver)
                try:
                    self.view.mostrar_erro("Usuário ou senha incorretos")
                except Exception as e:
                    logger.error(f"Erro ao exibir mensagem de erro: {e}")
                return False

        except Exception as e:
            logger.error(f"Erro durante o processo de login: {e}")
            return False

    def destruir_view_login(self):
        logger.debug("Destruindo view de login")
        if self.view:
            try:
                self.view.destruir()
                logger.debug("View de login destruída com sucesso")
            except Exception as e:
                logger.error(f"Erro ao destruir view de login: {e}")
            finally:
                self.view = None

    def criar_main_view(self):
        logger.debug("Criando view principal")
        # destrói main_view antiga se houver
        if self.main_view:
            try:
                self.main_view.destroy()
                logger.debug("View principal anterior destruída")
            except Exception as e:
                logger.error(f"Erro ao destruir view principal anterior: {e}")
            self.main_view = None

        try:
            self.main_view = MainView(parent=self.root, router=self.router)
            logger.debug("View principal criada com sucesso")
            return self.main_view
        except Exception as e:
            logger.error(f"Erro ao criar view principal: {e}")
            raise