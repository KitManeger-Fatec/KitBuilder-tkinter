import customtkinter as ctk
from PIL import Image
import logging
from app.config.themes.colors import COLORS
from app.config.themes.fonts import FONTS

logger = logging.getLogger(__name__)

class LoginView(ctk.CTkFrame):
    """
    LoginView como frame que ocupa o root.
    """
    def __init__(self, parent, controller=None):
        logger.debug("Inicializando LoginView")
        super().__init__(parent, fg_color=COLORS["bg"])
        self.controller = controller
        self.pack(fill="both", expand=True)

        # configura grid para responsividade
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, uniform="a")
        self.grid_columnconfigure(1, weight=1, uniform="a")

        self._setup_ui()
        logger.debug("LoginView inicializada com sucesso")

    def _setup_ui(self):
        logger.debug("Configurando interface do LoginView")
        # Container central (um painel com canto arredondado)
        container = ctk.CTkFrame(self, fg_color=COLORS["panel"], corner_radius=14, width=1000, height=600)
        container.grid(row=0, column=0, columnspan=2, padx=40, pady=60, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)

        # Left: área de imagem / branding
        left = ctk.CTkFrame(container, fg_color=COLORS["panel"], corner_radius=10)
        left.grid(row=0, column=0, sticky="nsew", padx=(24,12), pady=24)
        left.grid_rowconfigure(0, weight=1)
        left.grid_columnconfigure(0, weight=1)

        # Tenta carregar logo.jpg e ajustar para exibição
        try:
            img = Image.open("assets/images/Logo.jpg")
            max_size = (560, 560)
            img.thumbnail(max_size, Image.LANCZOS)
            self.logo_image = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            ctk.CTkLabel(left, image=self.logo_image, text="").grid(row=0, column=0, sticky="n", padx=12, pady=20)
            logger.debug("Logo carregada com sucesso")
        except Exception as e:
            logger.error(f"Erro ao carregar logo: {e}")
            # placeholder quando não há imagem
            placeholder = ctk.CTkFrame(left, fg_color=COLORS["bg"], corner_radius=8, height=300, width=400)
            placeholder.grid(row=0, column=0, padx=12, pady=12)
            ctk.CTkLabel(left, text="LOGO", font=FONTS["title"], text_color=COLORS["fg"]).place(in_=placeholder, relx=0.5, rely=0.5, anchor="center")
            logger.debug("Placeholder de logo criado")

        # Branding / frase de apoio abaixo da imagem
        ctk.CTkLabel(left, text="S.A.G.A", font=FONTS["title"], text_color=COLORS["fg"]).grid(row=1, column=0, pady=(6,2))
        ctk.CTkLabel(left, text="Sistema Auxílio de Gerenciamento Avançado", font=FONTS["text"], text_color=COLORS["muted"]).grid(row=2, column=0, pady=(0,16))

        # Right: formulário de login
        right = ctk.CTkFrame(container, fg_color=COLORS["bg"], corner_radius=10)
        right.grid(row=0, column=1, sticky="nsew", padx=(12,24), pady=24)
        right.grid_rowconfigure(0, weight=0)
        right.grid_rowconfigure(1, weight=1)

        form_holder = ctk.CTkFrame(right, fg_color=COLORS["panel"], corner_radius=5, width=420, height=360)
        form_holder.place(relx=0.5, rely=0.5, anchor="center")  # centraliza dentro do right

        # Títulos do formulário
        ctk.CTkLabel(form_holder, text="Acesse sua conta", font=FONTS["subtitle"], text_color=COLORS["fg"]).pack(pady=(22,6))

        # Campo Usuário
        ctk.CTkLabel(form_holder, text="Usuário", font=FONTS["text"], text_color=COLORS["muted"]).pack(anchor="w", padx=24, pady=(8,0))
        self.usuario_entry = ctk.CTkEntry(form_holder, width=340)
        self.usuario_entry.pack(pady=(6,12), padx=20)

        # Campo Senha
        ctk.CTkLabel(form_holder, text="Senha", font=FONTS["text"], text_color=COLORS["muted"]).pack(anchor="w", padx=24, pady=(8,0))
        self.senha_entry = ctk.CTkEntry(form_holder, show="*", width=340)
        self.senha_entry.pack(pady=(6,12))

        # Mensagem de erro
        self.msg_label = ctk.CTkLabel(form_holder, text="", font=FONTS["text"], text_color=COLORS["error"])
        self.msg_label.pack(pady=(4,6))

        # Botão Login
        self.login_button = ctk.CTkButton(
            form_holder, text="Entrar",
            command=(self.controller.fazer_login if self.controller else None),
            fg_color=COLORS["button"], text_color=COLORS["button_text"],
            font=FONTS["button"], width=340, height=44
        )
        self.login_button.pack(pady=(10,18))

        # Atalho local (opcional): Enter foca no botão quando em formulário
        try:
            self.usuario_entry.bind("<Return>", lambda e: self.controller.fazer_login() if self.controller else None)
            self.senha_entry.bind("<Return>", lambda e: self.controller.fazer_login() if self.controller else None)
            logger.debug("Atalhos de teclado configurados")
        except Exception as e:
            logger.warning(f"Erro ao configurar atalhos de teclado: {e}")

        # foco inicial
        try:
            self.usuario_entry.focus_set()
        except Exception as e:
            logger.warning(f"Erro ao definir foco inicial: {e}")

        logger.debug("Interface do LoginView configurada com sucesso")

    def get_credenciais(self):
        usuario = self.usuario_entry.get()
        senha = self.senha_entry.get()
        logger.debug(f"Credenciais obtidas - Usuário: {usuario}")
        return usuario, senha

    def mostrar_erro(self, mensagem):
        logger.warning(f"Exibindo mensagem de erro: {mensagem}")
        try:
            self.msg_label.configure(text=mensagem)
        except Exception as e:
            logger.error(f"Erro ao exibir mensagem de erro: {e}")

    def destruir(self):
        logger.debug("Destruindo LoginView")
        try:
            self.destroy()
        except Exception as e:
            logger.error(f"Erro ao destruir LoginView: {e}")