import logging
import requests
from app.models.authModel import AuthModel
from app.views.loginView import LoginView
from app.views.mainView import MainView
from app.views.cadastroView import CadastroView
from app.controllers.cadastroView_controller import CadastroViewController
from app.utils.logger_config import get_logger


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
        self.main_view = None
        self.cadastro_view = None
        logger.info("AuthController inicializado com sucesso")

    def criar_view_cadastro(self):
            """Cria e exibe a tela de cadastro de funcionário."""
            logger.debug("Criando view de cadastro")
            self.destruir_view_cadastro() # Garante que a view anterior seja destruída
            try:
                # 1. Instancia o controlador de lógica de cadastro
                cadastro_controller = CadastroViewController()
                
                # 2. Instancia a view, passando a si próprio (self) como roteador e o novo controller
                self.cadastro_view = CadastroView(
                    parent=self.root, 
                    router=self.router, 
                    controller=cadastro_controller # Passando o ControllerCadastro
                )
                logger.debug("View de cadastro criada com sucesso")
                return self.cadastro_view
            except Exception as e:
                logger.error(f"Erro ao criar view de cadastro: {e}")
                return None

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
            logger.debug("Iniciando processo de login via API")
            if not self.view:
                logger.warning("Tentativa de login sem view definida")
                return False

            try:
                usuario, senha = self.view.get_credenciais()
                logger.debug(f"Credenciais obtidas - Usuário: {usuario}")

                url = "http://127.0.0.1:8000/auth/login"  # ou IP do seu servidor
                payload = {"username": usuario, "password": senha}

                try:
                    response = requests.post(url, json=payload)
                except Exception as e:
                    logger.error(f"Erro ao conectar com API: {e}")
                    self.view.mostrar_erro("Erro de conexão com o servidor")
                    return False

                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"Login bem-sucedido para usuário: {usuario}")
                    if self.router and hasattr(self.router, "show_main"):
                        self.router.show_main()
                    return True
                else:
                    # detalhar mensagem de erro retornada pelo FastAPI
                    detalhe = response.json().get("detail", "Usuário ou senha incorretos")
                    logger.warning(f"Tentativa de login falhou: {detalhe}")
                    self.view.mostrar_erro(detalhe)
                    return False

            except Exception as e:
                logger.error(f"Erro durante o processo de login: {e}")
                self.view.mostrar_erro("Erro inesperado")
                return False
            
    def fazer_login_para_cadastro(self):
        logger.debug("Iniciando processo de login via API")
        if not self.view:
            logger.warning("Tentativa de login sem view definida")
            return False

        try:
            usuario, senha = self.view.get_credenciais()
            logger.debug(f"Credenciais obtidas - Usuário: {usuario}")

            url = "http://127.0.0.1:8000/auth/login"  # ou IP do seu servidor
            payload = {"username": usuario, "password": senha}

            try:
                response = requests.post(url, json=payload)
            except Exception as e:
                logger.error(f"Erro ao conectar com API: {e}")
                self.view.mostrar_erro("Erro de conexão com o servidor")
                return False

            if response.status_code == 200:
                data = response.json()
                logger.info(f"Login bem-sucedido para usuário: {usuario}")
                if self.router and hasattr(self.router, "show_cadastro"):
                    self.router.show_cadastro()
                return True
            else:
                # detalhar mensagem de erro retornada pelo FastAPI
                detalhe = response.json().get("detail", "Usuário ou senha incorretos")
                logger.warning(f"Tentativa de cadastro falhou: {detalhe}")
                self.view.mostrar_erro(detalhe)
                return False

        except Exception as e:
            logger.error(f"Erro durante o processo de login: {e}")
            self.view.mostrar_erro("Erro inesperado")
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

    def destruir_view_cadastro(self):
        """Destrói a tela de cadastro, se existir."""
        logger.debug("Destruindo view de cadastro")
        if self.cadastro_view:
            try:
                self.cadastro_view.destruir()
                logger.debug("View de cadastro destruída com sucesso")
            except Exception as e:
                logger.error(f"Erro ao destruir view de cadastro: {e}")
            finally:
                self.cadastro_view = None

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


