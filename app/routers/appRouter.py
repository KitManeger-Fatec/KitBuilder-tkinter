# routers/appRouter.py
class AppRouter:
    """
    routers simples que centraliza a navegação entre views na aplicação.
    - É criado com uma referência ao root (janela).
    - Depois deve receber o controller via set_controller(controller).
    - Métodos publicos: show_login(), show_main().
    """

    def __init__(self, root):
        self.root = root
        self.controller = None
        self.current_view = None

    def set_controller(self, controller):
        """Vincula o controller que o routers vai usar para criar as views."""
        self.controller = controller

    def clear_root(self):
        """Dá um destroy em todos os filhos diretos do root (limpa a tela)."""
        for child in list(self.root.winfo_children()):
            try:
                child.destroy()
            except Exception:
                pass

    def show_login(self):
        """
        Limpa a root e cria a view de login via controller.
        Mantém referência em current_view.
        """
        self.clear_root()
        if not self.controller:
            return None
        # garante que não exista view antiga
        try:
            self.controller.destruir_view_login()
        except Exception:
            pass
        try:
            self.controller.criar_view_login()
            self.current_view = self.controller.view
            return self.current_view
        except Exception:
            return None

    def show_main(self):
        """
        Limpa a root e cria a main view via controller.
        Mantém referência em current_view.
        """
        self.clear_root()
        if not self.controller:
            return None
        try:
            self.controller.criar_main_view()
            self.current_view = self.controller.main_view
            return self.current_view
        except Exception:
            return None
