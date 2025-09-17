# app/views/main_view.py
import logging
import customtkinter as ctk
from app.config.themes.colors import COLORS
from app.config.themes.fonts import FONTS
from app.config.settings import BRAND_NAME, APP_TITLE
from app.controllers.categoria_controller import CategoriaController

logger = logging.getLogger(__name__)

class MainView(ctk.CTkFrame):
    def __init__(self, parent=None, router=None):
        logger.debug("Inicializando MainView")
        self.router = router

        if parent is None:
            self._standalone = True
            self.root = ctk.CTk()
            super().__init__(self.root, fg_color=COLORS["bg"])
            self.root.title(APP_TITLE)

            # Fullscreen inicial
            try:
                self.root.attributes("-fullscreen", True)
            except Exception as e:
                logger.error(f"Erro ao definir fullscreen: {e}")

            self.pack(fill="both", expand=True)

            # Evento para monitorar mudanças na janela
            self.root.bind("<Configure>", self.on_window_configure)
            self._was_fullscreen = True
        else:
            self._standalone = False
            self.root = parent
            super().__init__(parent, fg_color=COLORS["bg"])
            self.pack(fill="both", expand=True)

        self.categorias_map = {}  # mapeia nome_categoria -> id_categoria
        self._setup_ui()
        logger.info("MainView inicializada com sucesso")

    def on_window_configure(self, event):
        """Redimensiona a janela proporcionalmente ao sair/entrar do fullscreen"""
        fullscreen = self.root.attributes("-fullscreen")
        # Saiu do fullscreen
        if self._was_fullscreen and not fullscreen:
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            new_width = int(screen_width * 0.8)
            new_height = int(screen_height * 0.8)
            self.root.geometry(f"{new_width}x{new_height}")
        # Entrou em fullscreen
        elif not self._was_fullscreen and fullscreen:
            self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        self._was_fullscreen = fullscreen

    def _setup_ui(self):
        top = ctk.CTkFrame(self, height=64, fg_color=COLORS["panel"])
        top.pack(fill="x", side="top")

        ctk.CTkLabel(top, text=BRAND_NAME, font=FONTS["title"], text_color=COLORS["fg"]).place(x=12, y=10)
        ctk.CTkLabel(top, text="Kit Manager", font=FONTS["text"], text_color=COLORS["muted"]).place(x=16, y=40)

        # --- Combos ---
        self.combo_classe = ctk.CTkComboBox(
            top,
            values=CategoriaController.get_classes(),
            command=self.on_classe_selected,
            width=150
        )
        self.combo_classe.place(x=200, y=10)

        self.combo_categoria = ctk.CTkComboBox(
            top,
            values=[],
            command=self.on_categoria_selected,
            width=150
        )
        self.combo_categoria.place(x=380, y=10)

        self.combo_subcategoria = ctk.CTkComboBox(
            top,
            values=[],
            width=150
        )
        self.combo_subcategoria.place(x=560, y=10)

        # Seleciona automaticamente o primeiro item da combo_classe
        if self.combo_classe.cget("values"):
            primeiro = self.combo_classe.cget("values")[0]
            self.combo_classe.set(primeiro)
            self.on_classe_selected(primeiro)

    # ---------------- Callbacks ----------------
    def on_classe_selected(self, value=None):
        if value is None:
            value = self.combo_classe.get() or (self.combo_classe.cget("values")[0] if self.combo_classe.cget("values") else "")
        logger.debug(f"Classe selecionada: {value}")

        categorias = CategoriaController.get_categorias_by_classe(value)
        self.categorias_map = {c.nome_categoria: c.id_categoria for c in categorias}

        if not self.categorias_map:
            self.combo_categoria.configure(values=["-- Nenhuma categoria --"])
        else:
            self.combo_categoria.configure(values=list(self.categorias_map.keys()))
            # Seleciona automaticamente o primeiro item
            primeiro = list(self.categorias_map.keys())[0]
            self.combo_categoria.set(primeiro)
            self.on_categoria_selected(primeiro)

        self.combo_subcategoria.configure(values=[])
        self.combo_subcategoria.set("")

    def on_categoria_selected(self, value=None):
        if value is None:
            value = self.combo_categoria.get() or (self.combo_categoria.cget("values")[0] if self.combo_categoria.cget("values") else "")
        logger.debug(f"Categoria selecionada: {value}")

        id_categoria = self.categorias_map.get(value)
        if not id_categoria:
            self.combo_subcategoria.configure(values=["-- Nenhuma subcategoria --"])
            self.combo_subcategoria.set("")
            return

        subs = CategoriaController.get_subcategorias_by_categoria(id_categoria)
        if not subs:
            self.combo_subcategoria.configure(values=["-- Nenhuma subcategoria --"])
        else:
            nomes_subs = [s.nome_subcategoria for s in subs]
            self.combo_subcategoria.configure(values=nomes_subs)
            # Seleciona automaticamente o primeiro item
            self.combo_subcategoria.set(nomes_subs[0])
