# controllers/authController.py
from models.authModel import AuthModel
from views.loginView import LoginView
from views.mainView import MainView

class AuthController:
    """
    Controller responsável por autenticação e criação de views dentro do root.
    Não executa mainloop; delega ao App.
    """
    def __init__(self, root=None, router=None):
        self.root = root
        self.router = router
        self.model = AuthModel()
        self.view = None
        self.main_view = None

    def criar_view_login(self):
        # cria LoginView embutida
        self.destruir_view_login()
        self.view = LoginView(parent=self.root, controller=self)

    def fazer_login(self):
        if not self.view:
            return False
        usuario, senha = self.view.get_credenciais()
        if self.model.verificar_credenciais(usuario, senha):
            # navega para main view
            if self.router and hasattr(self.router, "show_main"):
                self.router.show_main()
            return True
        else:
            self.view.mostrar_erro("Usuário ou senha incorretos")
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
