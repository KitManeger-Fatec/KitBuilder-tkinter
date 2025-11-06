from pathlib import Path
import customtkinter as ctk
import os
from dotenv import load_dotenv
from app.utils.logger_config import get_logger  
from app.controllers.authController import AuthController
from app.config import FULLSCREEN, APP_TITLE, SETUP_LOGGING, LOG_LEVEL
from app.routers.appRouter import AppRouter
from app.config.logging_config import setup_logging
from app.controllers.pedidoView_controller import PedidoViewController
from app.controllers.cadastroView_controller import CadastroViewController
from app.database import engine
from app.models import Base
from passlib.context import CryptContext
import logging
import threading
import uvicorn
from api.routes import api 
from web_app.web import web  # Importa a aplicação Flask

Base.metadata.create_all(bind=engine)

logger = get_logger(__name__)

load_dotenv()
# -----------------------------
# CLASSE APP
# -----------------------------
class App:
    def __init__(self):
        logger.info(f"Inicializando aplicação {os.getenv('BRAND_NAME')}")


        # CustomTkinter settings
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        logger.debug("Configuração de tema do CustomTkinter definida")

        # Root (single instance)
        self.root = ctk.CTk()
        self.root.title(os.getenv("BRAND_NAME"))
        logger.debug(f"Janela principal criada com título: {os.getenv('BRAND_NAME')}")

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

        # Controller Auth
        self.controller = AuthController(root=self.root, router=self.router)
        logger.debug("AuthController inicializado")

        # conecta controller ao routers
        self.router.set_controller(self.controller)
        logger.debug("Controller conectado ao router")


        self.current_view = None  # ainda não há view exibida

        # Global keybindings: Escape => toggle fullscreen
        self.root.bind("<Escape>", lambda event: self.toggle_fullscreen())
        logger.debug("Tecla Escape vinculada para alternar fullscreen")

        # Start in main screen (View escolhida para testes)
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

    def show_cadastro(self):
        logger.debug("Navegando para tela de cadastro de funcionário")
        view = self.router.show_cadastro()
        self.current_view = view

    def run(self):
        logger.info("Iniciando loop principal da aplicação")
        self.root.mainloop()

# -----------------------------
# INÍCIO DO SCRIPT DA API 
# -----------------------------

def start_api():
    logging.basicConfig(level=logging.DEBUG)
    uvicorn.run(api, host="127.0.0.1", port=8000, reload=False, log_level="info")

# -----------------------------
# INÍCIO DO SCRIPT DO SITE 
# -----------------------------
def start_flask():
    web.run(host="127.0.0.1", port=5001, debug=False, use_reloader=False)

if __name__ == "__main__":
    if SETUP_LOGGING:
        setup_logging(LOG_LEVEL)
        logger.info("Sistema de logging configurado")

    # INICIA FASTAPI EM THREAD
    threading.Thread(target=start_api, daemon=True).start()
    logger.info("FastAPI iniciada em http://127.0.0.1:8000")

    # INICIA FLASK EM OUTRA THREAD
    threading.Thread(target=start_flask, daemon=True).start()
    logger.info("Flask iniciado em http://127.0.0.1:5001")

    # INICIA TKINTER (principal)
    app = App()
    app.run()
''