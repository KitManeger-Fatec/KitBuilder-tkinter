# screens/login.py
import customtkinter as ctk
from PIL import Image
from config.colors import COLORS
from config.fonts import FONTS
from config.settings import USUARIO_PADRAO, SENHA_PADRAO
from screens.main_screen import MainScreen


class LoginScreen(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tela de Login")
        self.attributes("-fullscreen", True)  # FULLSCREEN garantido
        self.configure(fg_color=COLORS["bg"])

        # Container central (margens = borda do fundo)
        container = ctk.CTkFrame(self, fg_color=COLORS["bg"])
        container.pack(expand=True)  # centraliza vertical e horizontal

        # Frame do "card" de login
        frame = ctk.CTkFrame(container, corner_radius=20, fg_color=COLORS["bg"])
        frame.pack(padx=80, pady=60)

        # --- LOGO (300x300) ---
        self.logo_image = ctk.CTkImage(
            light_image=Image.open("logo.jpg"),
            dark_image=Image.open("logo.jpg"),
            size=(300, 300)
        )
        ctk.CTkLabel(frame, image=self.logo_image, text="").pack(pady=(10, 5))

        # --- TÍTULOS ---
        ctk.CTkLabel(
            frame, text="S.A.G.A",
            font=("Arial", 32, "bold"),
            text_color=COLORS["fg"]
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            frame, text="Sistema Auxílio de Gerenciamento Avançado",
            font=("Arial", 18),
            text_color=COLORS["fg"]
        ).pack(pady=(0, 25))

        # --- CAMPOS LOGIN ---
        ctk.CTkLabel(frame, text="Usuário:", font=FONTS["text"], text_color=COLORS["fg"]).pack()
        self.usuario_entry = ctk.CTkEntry(frame, width=300)
        self.usuario_entry.pack(pady=(0, 10))

        ctk.CTkLabel(frame, text="Senha:", font=FONTS["text"], text_color=COLORS["fg"]).pack()
        self.senha_entry = ctk.CTkEntry(frame, show="*", width=300)
        self.senha_entry.pack(pady=(0, 10))

        # --- MENSAGEM DE ERRO ---
        self.msg_label = ctk.CTkLabel(frame, text="", font=FONTS["text"], text_color=COLORS["error"])
        self.msg_label.pack(pady=(0, 5))

        # --- BOTÃO LOGIN ---
        self.login_button = ctk.CTkButton(
            frame, text="Login", command=self.fazer_login,
            fg_color=COLORS["button"], text_color=COLORS["button_text"],
            font=FONTS["button"], width=300, height=40
        )
        self.login_button.pack(pady=(10, 20))

        # Atalhos
        self.bind("<Escape>", lambda event: self.attributes("-fullscreen", False))
        self.bind("<Return>", lambda event: self.fazer_login())

        # Foco inicial
        self.usuario_entry.focus_set()

    def fazer_login(self):
        usuario = self.usuario_entry.get()
        senha = self.senha_entry.get()

        if usuario == USUARIO_PADRAO and senha == SENHA_PADRAO:
            self.destroy()
            MainScreen()
        else:
            self.msg_label.configure(text="Usuário ou senha incorretos")
