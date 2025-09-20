import logging
import os
import customtkinter as ctk
from tkinter import ttk
from sqlalchemy import MetaData, Table
from app.controllers.mainView_controller import MainViewController
from app.config.themes.colors import COLORS
from app.config.themes.fonts import FONTS
from app.config.settings import BRAND_NAME
from app.database import engine
from PIL import Image, ImageTk

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class MainView(ctk.CTkFrame):
    def __init__(self, parent=None, router=None):
        self.router = router
        self._standalone = parent is None
        self.root = parent if parent else ctk.CTk()
        super().__init__(self.root, fg_color=COLORS["bg"])
        self.pack(fill="both", expand=True)

        # Dados internos
        self.categorias_map = {}
        self.subcategorias_map = {}
        self.itens_completos = []
        self.colunas = []
        self.colunas_visiveis = []
        self.colunas_fabricantes = []
        self.renomear_map = {}
        self.filtros_widgets = {}

        self._setup_ui()
        self._carregar_classes()

    # ---------------- Setup UI ----------------
    def _setup_ui(self):
        # Barra superior
        top = ctk.CTkFrame(self, height=64, fg_color=COLORS["panel"])
        top.pack(fill="x", side="top")
        ctk.CTkLabel(top, text=BRAND_NAME, font=FONTS["title"], text_color=COLORS["fg"]).place(x=12, y=10)

        self.combo_classe = ctk.CTkComboBox(top, values=["Escolha uma classe"],
                                            command=self.on_classe_selected, width=250)
        self.combo_classe.set("Escolha uma classe")
        self.combo_classe.place(x=200, y=10)

        self.combo_categoria = ctk.CTkComboBox(top, values=["Escolha uma categoria"],
                                               command=self.on_categoria_selected, width=250)
        self.combo_categoria.set("Escolha uma categoria")
        self.combo_categoria.place(x=500, y=10)

        self.combo_subcategoria = ctk.CTkComboBox(top, values=["Escolha uma subcategoria"],
                                                  command=self.on_subcategoria_selected, width=250)
        self.combo_subcategoria.set("Escolha uma subcategoria")
        self.combo_subcategoria.place(x=800, y=10)

        # Frame principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Filtros à esquerda
        self.frame_filtros = ctk.CTkScrollableFrame(main_frame, width=220)
        self.frame_filtros.pack(side="left", fill="y", padx=(0, 10))
        self.frame_filtros.pack_propagate(False)

        # Painel direito
        frame_direita = ctk.CTkFrame(main_frame)
        frame_direita.pack(side="right", fill="both", expand=True)

        # Detalhes do item (topo)
        self.frame_detalhes = ctk.CTkFrame(frame_direita, height=150, fg_color=COLORS["panel"])
        self.frame_detalhes.pack(fill="x", side="top", pady=(0, 10))
        self.frame_detalhes.pack_propagate(False)

        # Treeview (inferior)
        self.frame_tree = ctk.CTkFrame(frame_direita)
        self.frame_tree.pack(fill="both", expand=True)

        self.tree_scroll_y = ttk.Scrollbar(self.frame_tree, orient="vertical")
        self.tree_scroll_x = ttk.Scrollbar(self.frame_tree, orient="horizontal")

        self.tree_itens = ttk.Treeview(
            self.frame_tree,
            columns=(),
            show="headings",
            yscrollcommand=self.tree_scroll_y.set,
            xscrollcommand=self.tree_scroll_x.set
        )

        self.tree_scroll_y.config(command=self.tree_itens.yview)
        self.tree_scroll_x.config(command=self.tree_itens.xview)
        self.tree_scroll_y.pack(side="right", fill="y")
        self.tree_scroll_x.pack(side="bottom", fill="x")
        self.tree_itens.pack(fill="both", expand=True, pady=(0, 5))

        # Bind seleção
        self.tree_itens.bind("<<TreeviewSelect>>", self.on_item_selected)

    # ---------------- Carregar classes ----------------
    def _carregar_classes(self):
        classes = MainViewController.get_classes() or []
        logger.info(f"Classes carregadas: {classes}")
        valores = ["Escolha uma classe"] + classes
        self.combo_classe.configure(values=valores)
        self.combo_classe.set("Escolha uma classe")

    # ---------------- Callbacks ----------------
    def on_classe_selected(self, value=None):
        value = value or self.combo_classe.get()
        if value == "Escolha uma classe":
            self._reset_categoria_sub()
            self._limpar_tabela()
            return

        categorias = MainViewController.get_categorias_by_classe(value)
        self.categorias_map = {c.nome_categoria: c.id_categoria for c in categorias}
        valores = ["Escolha uma categoria"] + list(self.categorias_map.keys()) if self.categorias_map else ["Escolha uma categoria"]
        self.combo_categoria.configure(values=valores)
        self.combo_categoria.set("Escolha uma categoria")
        self._reset_sub()
        self._limpar_tabela()

    def on_categoria_selected(self, value=None):
        value = value or self.combo_categoria.get()
        if value == "Escolha uma categoria":
            self._reset_sub()
            self._limpar_tabela()
            return

        id_categoria = self.categorias_map.get(value)
        subs = MainViewController.get_subcategorias_by_categoria(id_categoria)
        self.subcategorias_map = {s.nome_subcategoria: s.db_subcategoria for s in subs}
        valores = ["Escolha uma subcategoria"] + list(self.subcategorias_map.keys()) if self.subcategorias_map else ["Escolha uma subcategoria"]
        self.combo_subcategoria.configure(values=valores)
        self.combo_subcategoria.set("Escolha uma subcategoria")
        self._limpar_tabela()

    def on_subcategoria_selected(self, value=None):
        value = value or self.combo_subcategoria.get()
        if value == "Escolha uma subcategoria":
            self._limpar_tabela()
            return

        db_sub = self.subcategorias_map.get(value)
        if not db_sub:
            self._limpar_tabela()
            return

        # --- Carrega metadados da tabela ---
        metadata = MetaData()
        tabela = Table(db_sub, metadata, autoload_with=engine)
        colunas = [c.name for c in tabela.columns]

        # --- Nomes amigáveis ---
        self.renomear_map = {r['renomear_coluna']: r['renomear_colunaRenomeada'] 
                             for r in MainViewController.get_renomear(db_sub)}

        # --- Colunas visíveis (antes de imagem, sem codigo_produto) ---
        self.colunas_visiveis = []
        for c in colunas:
            if c == "imagem":
                break
            if c != "codigo_produto":
                self.colunas_visiveis.append(c)

        # --- Colunas "Fabricantes" (após imagem) ---
        if "imagem" in colunas:
            idx_imagem = colunas.index("imagem")
            self.colunas_fabricantes = colunas[idx_imagem + 1:]
        else:
            self.colunas_fabricantes = []

        # --- Itens completos ---
        itens = MainViewController.get_itens_by_subcategoria(db_sub)
        self.itens_completos = [dict(zip(colunas, l)) for l in itens]
        self.colunas = colunas  # mantém todas as colunas

        logger.info(f"Itens carregados: {len(self.itens_completos)}")

        # --- Atualiza Treeview ---
        self._atualizar_treeview(self.itens_completos)

        # --- Atualiza filtros ---
        self._criar_combos_filtros()

    # ---------------- Helpers ----------------
    def _limpar_tabela(self):
        self.tree_itens.delete(*self.tree_itens.get_children())
        self.itens_completos = []
        self.colunas = []
        self.colunas_visiveis = []
        self.colunas_fabricantes = []
        for w in self.frame_filtros.winfo_children():
            w.destroy()
        self.filtros_widgets.clear()

    def _reset_categoria_sub(self):
        self.combo_categoria.configure(values=["Escolha uma categoria"])
        self.combo_categoria.set("Escolha uma categoria")
        self._reset_sub()

    def _reset_sub(self):
        self.combo_subcategoria.configure(values=["Escolha uma subcategoria"])
        self.combo_subcategoria.set("Escolha uma subcategoria")
        self.subcategorias_map.clear()

    def _atualizar_treeview(self, itens):
        self.tree_itens.delete(*self.tree_itens.get_children())
        self.tree_itens["columns"] = self.colunas_visiveis
        for c in self.colunas_visiveis:
            self.tree_itens.heading(c, text=self.renomear_map.get(c, c))
            self.tree_itens.column(c, width=120)

        for item in itens:
            valores = [item[c] for c in self.colunas_visiveis]
            self.tree_itens.insert("", "end", values=valores)

    # ---------------- Filtros ----------------
    def _criar_combos_filtros(self):
        if not self.itens_completos:
            return

        for w in self.frame_filtros.winfo_children():
            w.destroy()
        self.filtros_widgets.clear()

        row = 0

        # --- Combobox Fabricantes ---
        if self.colunas_fabricantes:
            lbl_fab = ctk.CTkLabel(self.frame_filtros, text="Fabricantes", anchor="w")
            lbl_fab.grid(row=row, column=0, sticky="ew", padx=5, pady=(10, 2))
            row += 1

            self.combo_fabricantes = ctk.CTkComboBox(
                self.frame_filtros,
                values=self.colunas_fabricantes,
                width=180,
                command=self.on_fabricante_selected
            )
            self.combo_fabricantes.set("Escolha um fabricante")
            self.combo_fabricantes.grid(row=row, column=0, pady=2, padx=5, sticky="ew")
            row += 1

        # --- Filtros dinâmicos ---
        for col in self.colunas_visiveis:
            lbl = ctk.CTkLabel(self.frame_filtros, text=col, anchor="w")
            lbl.grid(row=row, column=0, sticky="ew", padx=5, pady=(10, 2))
            row += 1

            valores_unicos = sorted(list(set(
                str(item.get(col, "")) for item in self.itens_completos if item.get(col) not in (None, "")
            )))

            if not valores_unicos:
                ctk.CTkLabel(self.frame_filtros, text="Nenhum valor", text_color="gray")\
                    .grid(row=row, column=0, padx=10, pady=2, sticky="w")
                row += 1
                continue

            if len(valores_unicos) == 1:
                lbl_val = ctk.CTkLabel(self.frame_filtros, text=valores_unicos[0],
                                        font=ctk.CTkFont(size=12, weight="bold"))
                lbl_val.grid(row=row, column=0, padx=10, pady=2, sticky="w")
                row += 1
                self.filtros_widgets[col] = ("label", lbl_val, valores_unicos[0])
                continue

            combo = ctk.CTkComboBox(
                self.frame_filtros,
                values=["Todos"] + valores_unicos,
                width=180,
                command=lambda v=None: self._aplicar_filtros()
            )
            combo.set("Todos")
            combo.grid(row=row, column=0, pady=2, padx=5, sticky="ew")
            row += 1
            self.filtros_widgets[col] = ("combobox", combo)

        self._aplicar_filtros()

    def _aplicar_filtros(self):
        if not self.itens_completos:
            return

        dados_filtrados = self.itens_completos
        for col, w in self.filtros_widgets.items():
            tipo, widget = w[0], w[1]
            if tipo == "combobox":
                val = widget.get()
                if val != "Todos":
                    dados_filtrados = [item for item in dados_filtrados if str(item.get(col, "")) == val]

        self._atualizar_treeview(dados_filtrados)

    # ---------------- Seleção de item ----------------
    def on_item_selected(self, event):
        selected = self.tree_itens.selection()
        if not selected:
            return

        idx = self.tree_itens.index(selected[0])
        if idx >= len(self.itens_completos):
            return
        dados_item = self.itens_completos[idx]

        for w in self.frame_detalhes.winfo_children():
            w.destroy()

        row = 0

        # Mostrar imagem
        img_file = dados_item.get("imagem")
        if img_file:
            img_file = img_file.strip()
            img_path = os.path.join(os.getcwd(), "assets", "images", img_file)
            if os.path.exists(img_path):
                try:
                    pil_img = Image.open(img_path)
                    pil_img = pil_img.resize((120, 120))
                    tk_img = ImageTk.PhotoImage(pil_img)
                    lbl_img = ctk.CTkLabel(self.frame_detalhes, image=tk_img)
                    lbl_img.image = tk_img
                    lbl_img.grid(row=0, column=0, rowspan=len(dados_item), padx=10, pady=5)
                except Exception as e:
                    logger.warning(f"Não foi possível carregar a imagem: {e}")

        col_offset = 1 if img_file else 0
        for col, val in dados_item.items():
            if col == "imagem":
                continue
            lbl_col = ctk.CTkLabel(self.frame_detalhes, text=f"{col}: {val}", anchor="w")
            lbl_col.grid(row=row, column=col_offset, sticky="w", padx=5, pady=2)
            row += 1

    def on_fabricante_selected(self, col_selecionada):
        if not col_selecionada:
            return
        # Atualiza painel de detalhes
        for w in self.frame_detalhes.winfo_children():
            if isinstance(w, ctk.CTkLabel) and "Fabricante selecionado" in w.cget("text"):
                w.destroy()
        lbl = ctk.CTkLabel(self.frame_detalhes, text=f"Fabricante selecionado: {col_selecionada}", anchor="w")
        lbl.grid(row=0, column=99, sticky="e", padx=10)
