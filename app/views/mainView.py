# app/views/mainView.py
import logging
import customtkinter as ctk
from app.config.themes.colors import COLORS
from app.config.themes.fonts import FONTS
from app.config.settings import BRAND_NAME
from app.controllers.mainView_controller import MainViewController

logger = logging.getLogger(__name__)

class MainView(ctk.CTkFrame):
    def __init__(self, parent=None, router=None):
        self.router = router
        self._standalone = parent is None
        self.root = parent if parent else ctk.CTk()
        super().__init__(self.root, fg_color=COLORS["bg"])
        self.pack(fill="both", expand=True)

        self.categorias_map = {}
        self.subcategorias_map = {}

        self._setup_ui()

    def _setup_ui(self):
        top = ctk.CTkFrame(self, height=64, fg_color=COLORS["panel"])
        top.pack(fill="x", side="top")

        ctk.CTkLabel(top, text=BRAND_NAME, font=FONTS["title"], text_color=COLORS["fg"]).place(x=12, y=10)

        # --- Combos ---
        self.combo_classe = ctk.CTkComboBox(
            top,
            values=MainViewController.get_classes(),
            command=self.on_classe_selected,
            width=150
        )
        self.combo_classe.place(x=200, y=10)

        self.combo_categoria = ctk.CTkComboBox(top, values=[], command=self.on_categoria_selected, width=150)
        self.combo_categoria.place(x=380, y=10)

        self.combo_subcategoria = ctk.CTkComboBox(top, values=[], command=self.on_subcategoria_selected, width=150)
        self.combo_subcategoria.place(x=560, y=10)

        # --- Lista de itens ---
        self.lista_itens = ctk.CTkTextbox(self, width=600, height=400)
        self.lista_itens.pack(pady=20)

        # Seleciona automaticamente a primeira classe
        if self.combo_classe.cget("values"):
            primeiro = self.combo_classe.cget("values")[0]
            self.combo_classe.set(primeiro)
            self.on_classe_selected(primeiro)

    # ---------------- Callbacks ----------------
    def on_classe_selected(self, value=None):
        if not value:
            value = self.combo_classe.get()
        categorias = MainViewController.get_categorias_by_classe(value)
        self.categorias_map = {c.nome_categoria: c.id_categoria for c in categorias}

        self.combo_categoria.configure(values=list(self.categorias_map.keys()) or ["-- Nenhuma --"])
        primeiro = list(self.categorias_map.keys())[0] if self.categorias_map else ""
        self.combo_categoria.set(primeiro)
        self.on_categoria_selected(primeiro)

        self.combo_subcategoria.configure(values=[])
        self.lista_itens.delete("0.0", "end")

    def on_categoria_selected(self, value=None):
        if not value:
            value = self.combo_categoria.get()
        id_categoria = self.categorias_map.get(value)
        if not id_categoria:
            self.combo_subcategoria.configure(values=["-- Nenhuma --"])
            self.lista_itens.delete("0.0", "end")
            return

        subs = MainViewController.get_subcategorias_by_categoria(id_categoria)
        self.subcategorias_map = {s.db_subcategoria: s.nome_subcategoria for s in subs}

        self.combo_subcategoria.configure(values=list(self.subcategorias_map.keys()) or ["-- Nenhuma --"])
        primeiro = list(self.subcategorias_map.keys())[0] if self.subcategorias_map else ""
        self.combo_subcategoria.set(primeiro)
        self.on_subcategoria_selected(primeiro)

    def on_subcategoria_selected(self, value=None):
        if not value:
            value = self.combo_subcategoria.get()
        itens = MainViewController.get_itens_by_subcategoria(value)

        self.lista_itens.delete("0.0", "end")
        if itens:
            for item in itens:
                # Converte objeto ORM em dicionário com colunas da tabela
                item_dict = {col.name: getattr(item, col.name) for col in item.__table__.columns}
                self.lista_itens.insert("end", str(item_dict) + "\n")
        else:
            self.lista_itens.insert("end", "-- Nenhum item encontrado --")
