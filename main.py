# main.py
from pathlib import Path
import customtkinter as ctk
import logging
import os
from dotenv import load_dotenv


from app.controllers.authController import AuthController
from app.config import FULLSCREEN, APP_TITLE, SETUP_LOGGING, LOG_LEVEL
from app.routers.appRouter import AppRouter
from app.config.logging_config import setup_logging

logger = logging.getLogger(__name__)



class App:
    def __init__(self):
        logger.info(f"Inicializando aplicação {os.getenv("BRAND_NAME")}")


        # CustomTkinter settings
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        logger.debug("Configuração de tema do CustomTkinter definida")

        # Root (single instance)
        self.root = ctk.CTk()
        self.root.title(os.getenv("BRAND_NAME"))
        logger.debug(f"Janela principal criada com título: {os.getenv("BRAND_NAME")}")

        # start fullscreen according to config
        try:
            if FULLSCREEN:
                self.root.attributes("-fullscreen", True)
                logger.debug("Modo fullscreen ativado")
        except Exception as e:
            logger.error(f"Erro ao definir fullscreen: {e}")

        # routers (responsável por show_login / show_main)
        self.router = AppRouter(self.root)
        logger.debug("AppRouter inicializado")

        # Controller -> agora exige routers externo
        self.controller = AuthController(root=self.root, router=self.router)
        logger.debug("AuthController inicializado")

        # conecta controller ao routers
        self.router.set_controller(self.controller)
        logger.debug("Controller conectado ao router")

        # current view reference (opcional)
        self.current_view = None

        # Global keybindings: Escape => toggle fullscreen
        self.root.bind("<Escape>", lambda event: self.toggle_fullscreen())
        logger.debug("Tecla Escape vinculada para alternar fullscreen")

        # Start in login screen (delegado ao routers)
        self.show_login()
        logger.info("Aplicação inicializada com sucesso")

    def toggle_fullscreen(self):
        try:
            current = bool(self.root.attributes("-fullscreen"))
            self.root.attributes("-fullscreen", not current)
            logger.debug(f"Fullscreen alternado para: {not current}")
        except Exception as e:
            logger.error(f"Erro ao alternar fullscreen: {e}")

    def clear_root(self):
        logger.debug("Limpando widgets da janela principal")
        for child in list(self.root.winfo_children()):
            try:
                child.destroy()
            except Exception as e:
                logger.error(f"Erro ao destruir widget: {e}")

    def show_login(self):
        logger.debug("Navegando para tela de login")
        view = self.router.show_login()
        self.current_view = view

    def show_main(self):
        logger.debug("Navegando para tela principal")
        view = self.router.show_main()
        self.current_view = view

    def run(self):
        logger.info("Iniciando loop principal da aplicação")
        self.root.mainloop()


if __name__ == "__main__":
    if SETUP_LOGGING:
        setup_logging(LOG_LEVEL)
        logger.info("Sistema de logging configurado")
    app = App()
    app.run()