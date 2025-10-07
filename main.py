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
from app.database import engine
from sqlalchemy import text
from datetime import datetime

logger = get_logger(__name__)

load_dotenv()

# -----------------------------
# FUNÇÃO PARA CRIAR TABELAS
# -----------------------------
def criar_tabelas():
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dados_pedido (
                id_pedido INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                funcionario_pedido INT NOT NULL,
                datetime_pedido VARCHAR(45) NOT NULL,
                nome_projeto VARCHAR(45) NOT NULL,
                nome_lista VARCHAR(45) NOT NULL,
                CONSTRAINT fk_funcionario_pedido FOREIGN KEY (funcionario_pedido)
                REFERENCES funcionarios(idfuncionarios)
                ON DELETE NO ACTION ON UPDATE NO ACTION
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS pedido (
                linha_pedido INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                id_dados_pedido INT NOT NULL,
                aceito TINYINT NULL,
                quantidade INT NOT NULL,
                medida VARCHAR(20) NOT NULL,
                codigo VARCHAR(20) NOT NULL,
                produto VARCHAR(200) NOT NULL,
                fabricante VARCHAR(45) NULL,
                cod_fabricante VARCHAR(45) NULL,
                CONSTRAINT fk_id_dados_pedido FOREIGN KEY (id_dados_pedido)
                REFERENCES dados_pedido(id_pedido)
                ON DELETE NO ACTION ON UPDATE NO ACTION
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS pedido_aprova (
                idpedido_aprova INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                pedido_idpedido INT NOT NULL,
                id_chefia_aprova INT NOT NULL,
                pedido_aprovado TINYINT NULL,
                CONSTRAINT fk_pedido_aprova_pedido FOREIGN KEY (pedido_idpedido)
                REFERENCES pedido(linha_pedido)
                ON DELETE NO ACTION ON UPDATE NO ACTION,
                CONSTRAINT fk_pedido_aprova_chefia FOREIGN KEY (id_chefia_aprova)
                REFERENCES chefia_direta(id_funcionario)
                ON DELETE NO ACTION ON UPDATE NO ACTION
            )
        """))
    logger.info("Tabelas do pedido criadas (se não existiam)")

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

        # Controller do Pedido (instância, mas não mostra ainda)
        self.pedido_controller = PedidoViewController()
        self.pedido_controller.set_usuario_logado(2)  # ID do usuário de teste

        self.current_view = None  # ainda não há view exibida

        # Global keybindings: Escape => toggle fullscreen
        self.root.bind("<Escape>", lambda event: self.toggle_fullscreen())
        logger.debug("Tecla Escape vinculada para alternar fullscreen")

        # Start in main screen (login pulado ou MainView)
        self.show_main()
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


# -----------------------------
# INÍCIO DO SCRIPT
# -----------------------------
if __name__ == "__main__":
    if SETUP_LOGGING:
        setup_logging(LOG_LEVEL)
        logger.info("Sistema de logging configurado")

    criar_tabelas()  # <<< Garante que as tabelas existem

    app = App()
    app.run()
''