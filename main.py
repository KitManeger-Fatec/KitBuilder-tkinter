# main.py
from pathlib import Path
import customtkinter as ctk

from app.controllers.authController import AuthController
from app.config import FULLSCREEN, APP_TITLE
from app.routers.appRouter import AppRouter  # novo import


def criar_env_se_nao_existir():
    env_file = Path('.') / '.env'
    if not env_file.exists():
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write("USERNAME=admin\n")
            f.write("PASSWORD=admin\n")
        print("Arquivo .env criado com credenciais padrão (USERNAME=admin / PASSWORD=admin).")


class App:
    def __init__(self):
        criar_env_se_nao_existir()

        # CustomTkinter settings
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Root (single instance)
        self.root = ctk.CTk()
        self.root.title(APP_TITLE)
        # start fullscreen according to config
        try:
            if FULLSCREEN:
                self.root.attributes("-fullscreen", True)
        except Exception:
            pass

        # routers (responsável por show_login / show_main)
        self.router = AppRouter(self.root)

        # Controller -> agora exige routers externo
        self.controller = AuthController(root=self.root, router=self.router)

        # conecta controller ao routers
        self.router.set_controller(self.controller)

        # current view reference (opcional)
        self.current_view = None

        # Global keybindings: Escape => toggle fullscreen
        self.root.bind("<Escape>", lambda event: self.toggle_fullscreen())

        # Start in login screen (delegado ao routers)
        self.show_login()

    def toggle_fullscreen(self):
        try:
            current = bool(self.root.attributes("-fullscreen"))
            self.root.attributes("-fullscreen", not current)
        except Exception:
            # fallback: try geometry
            pass

    def clear_root(self):
        # mantenho essa função caso outras partes ainda a usem
        for child in list(self.root.winfo_children()):
            try:
                child.destroy()
            except Exception:
                pass

    def show_login(self):
        # delega para o routers
        view = self.router.show_login()
        self.current_view = view

    def show_main(self):
        # delega para o routers
        view = self.router.show_main()
        self.current_view = view

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
