import customtkinter as ctk
import logging
from app.config.themes.colors import COLORS
from app.config.themes.fonts import FONTS
from app.config.settings import BRAND_NAME, APP_TITLE

logger = logging.getLogger(__name__)

class MainView(ctk.CTkFrame):
    """
    MainView pensada para montagem de kits
    """
    def __init__(self, parent=None, router=None):
        logger.debug("Inicializando MainView")
        self.router = router

        if parent is None:
            self._standalone = True
            self.root = ctk.CTk()
            super().__init__(self.root, fg_color=COLORS["bg"])
            self.root.title(APP_TITLE)
            try:
                self.root.attributes("-fullscreen", True)
                logger.debug("Modo fullscreen ativado para MainView standalone")
            except Exception as e:
                logger.error(f"Erro ao definir fullscreen: {e}")
            self.pack(fill="both", expand=True)
        else:
            self._standalone = False
            self.root = parent
            super().__init__(parent, fg_color=COLORS["bg"])
            self.pack(fill="both", expand=True)

        # internal state: lista fictícia de kits (exemplo)
        self.kits = [
            {"id": 1, "name": "Kit Básico - Parafusos", "price": 9.90, "items": 12},
            {"id": 2, "name": "Kit Avançado - Elétrico", "price": 49.90, "items": 48},
            {"id": 3, "name": "Kit Profissional - Carroceria", "price": 129.00, "items": 120},
        ]

        self._setup_ui()
        logger.info("MainView inicializada com sucesso")

    def _setup_ui(self):
        logger.debug("Configurando interface da MainView")
        # top appbar
        top = ctk.CTkFrame(self, height=64, fg_color=COLORS["panel"])
        top.pack(fill="x", side="top")

        ctk.CTkLabel(top, text=BRAND_NAME, font=FONTS["title"], text_color=COLORS["fg"]).place(x=12, y=10)
        ctk.CTkLabel(top, text="Kit Manager", font=FONTS["text"], text_color=COLORS["muted"]).place(x=16, y=40)

        # toolbar (right)
        sync_btn = ctk.CTkButton(top, text="Sincronizar com site", width=180, fg_color=COLORS["accent"],
                                 text_color=COLORS["button_text"], command=self.sync_all)
        sync_btn.place(relx=0.85, rely=0.5, anchor="center")

        # main body: left (list), right (details)
        body = ctk.CTkFrame(self, fg_color=COLORS["bg"])
        body.pack(fill="both", expand=True, padx=16, pady=12)

        # left pane
        left_pane = ctk.CTkFrame(body, width=320, fg_color=COLORS["panel"], corner_radius=8)
        left_pane.pack(side="left", fill="y", padx=(0,12), pady=6)

        # search
        ctk.CTkEntry(left_pane, placeholder_text="Pesquisar kits...", width=260, corner_radius=8).pack(padx=12, pady=12)

        # scrollable list of kits
        scroll = ctk.CTkScrollableFrame(left_pane, height=520, fg_color=COLORS["panel"], corner_radius=6)
        scroll.pack(fill="y", padx=12, pady=(0,12), expand=True)

        for kit in self.kits:
            frame = ctk.CTkFrame(scroll, fg_color=COLORS["bg"], corner_radius=6)
            frame.pack(fill="x", padx=8, pady=6)

            title = ctk.CTkLabel(frame, text=kit["name"], font=FONTS["text"], text_color=COLORS["fg"])
            title.grid(row=0, column=0, sticky="w", padx=8, pady=(6,2))

            meta = ctk.CTkLabel(frame, text=f'Itens: {kit["items"]}  •  R$ {kit["price"]:.2f}',
                                 font=FONTS["mono"], text_color=COLORS["muted"])
            meta.grid(row=1, column=0, sticky="w", padx=8, pady=(0,8))

            btn_frame = ctk.CTkFrame(frame, fg_color=COLORS["bg"], corner_radius=0)
            btn_frame.grid(row=0, column=1, rowspan=2, padx=8, pady=6)
            btn_view = ctk.CTkButton(btn_frame, text="Abrir", width=72, command=lambda k=kit: self.open_kit(k))
            btn_view.pack(padx=4, pady=6)

        # bottom add kit
        ctk.CTkButton(left_pane, text="Criar novo kit", fg_color=COLORS["accent"], text_color=COLORS["button_text"],
                      command=self.create_kit).pack(pady=10)

        # right pane (details + preview)
        right_pane = ctk.CTkFrame(body, fg_color=COLORS["bg"])
        right_pane.pack(side="right", fill="both", expand=True)

        # header of details
        self.detail_title = ctk.CTkLabel(right_pane, text="Selecione um kit à esquerda", font=FONTS["subtitle"], text_color=COLORS["muted"])
        self.detail_title.pack(anchor="nw", pady=(8,4), padx=12)

        # preview & fields container
        content = ctk.CTkFrame(right_pane, fg_color=COLORS["panel"], corner_radius=8)
        content.pack(fill="both", expand=True, padx=12, pady=12)

        # preview image (placeholder)
        preview = ctk.CTkFrame(content, height=220, fg_color=COLORS["bg"], corner_radius=8)
        preview.pack(fill="x", padx=16, pady=12)
        ctk.CTkLabel(preview, text="Imagem do kit (preview)", font=FONTS["text"], text_color=COLORS["muted"]).place(relx=0.5, rely=0.5, anchor="center")

        # fields
        field_frame = ctk.CTkFrame(content, fg_color=COLORS["panel"])
        field_frame.pack(fill="both", expand=True, padx=16, pady=(4,16))

        ctk.CTkLabel(field_frame, text="Nome do Kit", font=FONTS["text"], text_color=COLORS["muted"]).pack(anchor="w", padx=8, pady=(8,2))
        self.kit_name = ctk.CTkEntry(field_frame, width=420)
        self.kit_name.pack(padx=8, pady=4)

        ctk.CTkLabel(field_frame, text="Descrição", font=FONTS["text"], text_color=COLORS["muted"]).pack(anchor="w", padx=8, pady=(8,2))
        self.kit_desc = ctk.CTkEntry(field_frame, width=420)
        self.kit_desc.pack(padx=8, pady=4)

        ctk.CTkLabel(field_frame, text="Preço (R$)", font=FONTS["text"], text_color=COLORS["muted"]).pack(anchor="w", padx=8, pady=(8,2))
        self.kit_price = ctk.CTkEntry(field_frame, width=200)
        self.kit_price.pack(padx=8, pady=4, anchor="w")

        # actions
        action_frame = ctk.CTkFrame(content, fg_color=COLORS["panel"])
        action_frame.pack(fill="x", padx=16, pady=8)

        ctk.CTkButton(action_frame, text="Salvar", fg_color=COLORS["accent"], text_color=COLORS["button_text"],
                      command=self.save_kit, width=120).pack(side="left", padx=8)

        ctk.CTkButton(action_frame, text="Publicar no Site", fg_color=COLORS["success"], text_color=COLORS["button_text"],
                      command=self.publish_kit, width=160).pack(side="left", padx=8)

        ctk.CTkButton(action_frame, text="Voltar ao Login", fg_color=COLORS["muted"], command=self.back_to_login, width=140).pack(side="right", padx=8)

        logger.debug("Interface da MainView configurada com sucesso")

    # ---- placeholder actions ----
    def open_kit(self, kit):
        logger.info(f"Abrindo kit: {kit['name']}")
        self.detail_title.configure(text=kit["name"])
        self.kit_name.delete(0, "end")
        self.kit_name.insert(0, kit["name"])
        self.kit_desc.delete(0, "end")
        self.kit_desc.insert(0, f"{kit['items']} itens")
        self.kit_price.delete(0, "end")
        self.kit_price.insert(0, f"{kit['price']:.2f}")

    def create_kit(self):
        logger.debug("Criando novo kit")
        self.detail_title.configure(text="Novo Kit")
        self.kit_name.delete(0, "end")
        self.kit_desc.delete(0, "end")
        self.kit_price.delete(0, "end")

    def save_kit(self):
        name = self.kit_name.get()
        logger.info(f"Salvando kit: {name}")
        print("Salvar kit:", name)

    def publish_kit(self):
        name = self.kit_name.get()
        logger.info(f"Publicando kit no site: {name}")
        print("Publicar no site:", self.kit_name.get())

    def sync_all(self):
        logger.info("Sincronizando todos os kits com o site")
        print("Sincronizando todos os kits com o site...")

    def back_to_login(self):
        logger.info("Voltando para tela de login")
        if self.router and hasattr(self.router, "show_login"):
            self.router.show_login()