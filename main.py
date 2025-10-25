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
from sqlalchemy import text
from datetime import datetime
from app.models import Base
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
import logging
from app.models.dados_pedido import DadosPedido
from app.models.pedido import Pedido
from app.models.chefia_direta import ChefiaDireta 

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

        # Controller do Pedido (instância, mas não mostra ainda)
        self.pedido_controller = PedidoViewController()
        self.pedido_controller.set_usuario_logado(2)  # ID do usuário de teste
        self.cadastro_controller = CadastroViewController()
        self.cadastro_controller.set_usuario_logado(2)  # ID do usuário de teste

        self.current_view = None  # ainda não há view exibida

        # Global keybindings: Escape => toggle fullscreen
        self.root.bind("<Escape>", lambda event: self.toggle_fullscreen())
        logger.debug("Tecla Escape vinculada para alternar fullscreen")

        # Start in main screen (View escolhida para testes)
        self.show_cadastro()
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


#------------------------------
# Fast API
#------------------------------

app = FastAPI(title="Minha API MVC")


# Dependência para injetar a sessão
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"status": "ok", "mensagem": "API FastAPI conectada ao MVC!"}


@app.get("/pedidos")
def get_pedidos(db: Session = Depends(get_db)):
    pedidos = db.query(DadosPedido).all()
    return [pedido.to_dict() for pedido in pedidos]

@app.get("/pedido/{id_pedido}")
def get_linhas_pedido(id_pedido: int, db: Session = Depends(get_db)):
    # Busca todas as linhas do pedido com id_dados_pedido = id_pedido
    linhas = db.query(Pedido).filter(Pedido.id_dados_pedido == id_pedido, Pedido.aceito == 1).all()

    # Retorna cada linha em dicionário
    return [linha.to_dict() for linha in linhas]

@app.get("/chefes/{id_funcionario}")
def get_chefes(id_funcionario: int, db: Session = Depends(get_db)):
    registros = db.query(ChefiaDireta).filter(ChefiaDireta.id_funcionario == id_funcionario).all()
    
    return [
        {
            "id_confere": reg.id_confere,
            "id_funcionario": reg.id_funcionario,
            "funcionario_nome": reg.funcionario.nome_funcionario if reg.funcionario else None,
            "id_chefia": reg.id_chefia,
            "chefe_nome": reg.chefe.nome_funcionario if reg.chefe else None,
        }
        for reg in registros
    ]

# -----------------------------
# INÍCIO DO SCRIPT
# -----------------------------
if __name__ == "__main__":
    if SETUP_LOGGING:
        setup_logging(LOG_LEVEL)
        logger.info("Sistema de logging configurado")

    app = App()
    app.run()
''