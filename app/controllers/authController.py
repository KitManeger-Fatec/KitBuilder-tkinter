# controllers/authController.py
from app.models.authModel import AuthModel
from app.views.loginView import LoginView
from app.views.mainView import MainView

class AuthController:
    """
    Controller responsável por autenticação e criação de views dentro do root.
    Agora exige um routers externo (injeção). Isso mantém a responsabilidade de
    navegação fora do controller e facilita integração com um AppRouter.
    """
    def __init__(self, root=None, router=None):
        if router is None:
            raise ValueError("AuthController requires a routers instance. Pass routers=<your_router>.")
        self.root = root
        self.router = router
        self.model = AuthModel()
        self.view = None
        self.main_view = None

    def criar_view_login(self):
        # cria LoginView embutida (destrói a anterior se houver)
        self.destruir_view_login()
        self.view = LoginView(parent=self.root, controller=self)

    def fazer_login(self):
        if not self.view:
            return False
        usuario, senha = self.view.get_credenciais()
        if self.model.verificar_credenciais(usuario, senha):
            # navega para main view via routers injetado
            if self.router and hasattr(self.router, "show_main"):
                try:
                    self.router.show_main()
                except Exception:
                    # não propaga para manter teste/robustez
                    pass
            return True
        else:
            # exibe erro na view (se houver)
            try:
                self.view.mostrar_erro("Usuário ou senha incorretos")
            except Exception:
                pass
            return False

    def destruir_view_login(self):
        if self.view:
            try:
                self.view.destruir()
            except Exception:
                pass
            self.view = None

    def criar_main_view(self):
        # destrói main_view antiga se houver
        if self.main_view:
            try:
                self.main_view.destroy()
            except Exception:
                pass
            self.main_view = None
        self.main_view = MainView(parent=self.root, router=self.router)
        return self.main_view
