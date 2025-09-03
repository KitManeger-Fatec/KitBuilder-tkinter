# main.py
from pathlib import Path
import customtkinter as ctk

from controllers.authController import AuthController
from config.settings import FULLSCREEN, APP_TITLE

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

        # Controller + Router
        self.controller = AuthController(root=self.root, router=self)

        # current view reference
        self.current_view = None

        # Global keybindings: Escape => toggle fullscreen
        self.root.bind("<Escape>", lambda event: self.toggle_fullscreen())

        # Start in login screen
        self.show_login()

    def toggle_fullscreen(self):
        try:
            current = bool(self.root.attributes("-fullscreen"))
            self.root.attributes("-fullscreen", not current)
        except Exception:
            # fallback: try geometry
            pass

    def clear_root(self):
        for child in list(self.root.winfo_children()):
            try:
                child.destroy()
            except Exception:
                pass

    def show_login(self):
        self.clear_root()
        self.controller.destruir_view_login()
        self.controller.criar_view_login()
        self.current_view = self.controller.view

    def show_main(self):
        self.clear_root()
        self.controller.criar_main_view()
        self.current_view = self.controller.main_view

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
