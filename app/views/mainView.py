import logging
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from sqlalchemy import MetaData, Table
from app.controllers.mainView_controller import MainViewController
from app.config.themes.colors import COLORS
from app.config.themes.fonts import FONTS
from app.config.settings import BRAND_NAME
from app.database import engine

# Configura o logger
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

        self.categorias_map = {}
        self.subcategorias_map = {}

        self.itens_completos = []
        self.colunas = []
        self.filtros_widgets = {}

        self._setup_ui()
        self._carregar_classes()

    # ---------------- Setup UI ----------------
    def _setup_ui(self):
        # --- Top bar ---
        top = ctk.CTkFrame(self, height=64, fg_color=COLORS["panel"])
        top.pack(fill="x", side="top")
        ctk.CTkLabel(top, text=BRAND_NAME, font=FONTS["title"], text_color=COLORS["fg"]).place(x=12, y=10)

        # Combos classe / categoria / subcategoria
        self.combo_classe = ctk.CTkComboBox(top, values=["Escolha uma classe"], command=self.on_classe_selected, width=250)
        self.combo_classe.set("Escolha uma classe")
        self.combo_classe.place(x=200, y=10)

        self.combo_categoria = ctk.CTkComboBox(top, values=["Escolha uma categoria"], command=self.on_categoria_selected, width=250)
        self.combo_categoria.set("Escolha uma categoria")
        self.combo_categoria.place(x=500, y=10)

        self.combo_subcategoria = ctk.CTkComboBox(top, values=["Escolha uma subcategoria"], command=self.on_subcategoria_selected, width=250)
        self.combo_subcategoria.set("Escolha uma subcategoria")
        self.combo_subcategoria.place(x=800, y=10)

        # --- Frame principal: filtros + tabela ---
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Configura as colunas: 0 (filtros) e 1 (tabela)
        main_frame.grid_columnconfigure(0, weight=0, minsize=200) # Coluna de filtros, largura mínima
        main_frame.grid_columnconfigure(1, weight=1) # Coluna da tabela, se expande

        # Configura a linha única para expandir verticalmente
        main_frame.grid_rowconfigure(0, weight=1)

        # Lado esquerdo: filtros (coluna 0)
        self.frame_filtros = ctk.CTkFrame(main_frame)
        self.frame_filtros.grid(row=0, column=0, sticky="nswe", padx=(0,10))
        self.frame_filtros.grid_columnconfigure(0, weight=1)
        self.frame_filtros.grid_rowconfigure(0, weight=1)

        # Lado direito: tabela (coluna 1)
        self.frame_tree = ctk.CTkFrame(main_frame)
        self.frame_tree.grid(row=0, column=1, sticky="nswe")
        self.frame_tree.grid_columnconfigure(0, weight=1)
        self.frame_tree.grid_rowconfigure(0, weight=1)

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

    # ---------------- Carregar classes ----------------
    def _carregar_classes(self):
        classes = MainViewController.get_classes()
        valores = ["Escolha uma classe"] + classes if classes else ["Escolha uma classe"]
        self.combo_classe.configure(values=valores)
        self.combo_classe.set("Escolha uma classe")

    # ---------------- Callbacks ----------------
    def on_classe_selected(self, value=None):
        if not value:
            value = self.combo_classe.get()
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
        if not value:
            value = self.combo_categoria.get()
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
        if not value:
            value = self.combo_subcategoria.get()
        if value == "Escolha uma subcategoria":
            self._limpar_tabela()
            return

        db_sub = self.subcategorias_map.get(value)
        if not db_sub:
            self._limpar_tabela()
            return

        # Monta a tabela dinamicamente
        metadata = MetaData()
        tabela = Table(db_sub, metadata, autoload_with=engine)
        colunas = [c.name for c in tabela.columns]
        
        # Filtra as colunas para a tabela (removendo 'codigo_produto', 'imagem' e as que vêm depois de 'imagem')
        self.colunas = []
        encontrou_imagem = False
        for col in colunas:
            if col == 'imagem':
                encontrou_imagem = True
            if not encontrou_imagem:
                self.colunas.append(col)
        
        # Carrega todos os itens, incluindo as colunas extras que não estarão na tabela
        itens = MainViewController.get_itens_by_subcategoria(db_sub)
        self.itens_completos = [dict(zip([c.name for c in tabela.columns], l)) for l in itens]
        
        # Atualiza Treeview
        self._atualizar_treeview(self.itens_completos)

        # Cria combos/checkboxes/labels de filtros
        self._criar_combos_filtros()
        
    # ---------------- Helpers ----------------
    def _limpar_tabela(self):
        self.tree_itens.delete(*self.tree_itens.get_children())
        self.itens_completos = []
        self.colunas = []
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

    def _atualizar_treeview(self, dados):
        self.tree_itens.delete(*self.tree_itens.get_children())
        self.tree_itens["columns"] = self.colunas
        
        # Configura colunas
        for col in self.colunas:
            self.tree_itens.heading(col, text=col)
            self.tree_itens.column(col, width=120, anchor="w")
        
        # Insere dados
        for registro in dados:
            # Pega apenas os valores das colunas que serão exibidas
            valores = [registro.get(col, "") for col in self.colunas]
            self.tree_itens.insert("", "end", values=valores)

    # ---------------- Filtros ----------------
    def _criar_combos_filtros(self):
        logger.info("Iniciando a criação de filtros.")
        db_sub = self.subcategorias_map.get(self.combo_subcategoria.get())
        logger.info("Tabela de origem: %s", db_sub)
        
        # Limpa frame de filtros
        for w in self.frame_filtros.winfo_children():
            w.destroy()
        self.filtros_widgets.clear()

        # Cria um canvas e scrollbar para filtros
        canvas = tk.Canvas(self.frame_filtros, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.frame_filtros, orient="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas)
        scrollable_frame.grid_columnconfigure(0, weight=1)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=self.frame_filtros.winfo_width())
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        row = 0
        
        # Colunas de fabricante (após 'imagem')
        colunas_fabricante = []
        colunas_normais = []
        encontrou_imagem = False
        
        for col in self.itens_completos[0].keys():
            if col == 'imagem':
                encontrou_imagem = True
                continue
            if encontrou_imagem:
                colunas_fabricante.append(col)
            else:
                colunas_normais.append(col)

        # Filtros de colunas principais (antes da 'imagem')
        for col in colunas_normais:
            try:
                lbl = ctk.CTkLabel(scrollable_frame, text=col, anchor="w")
                lbl.grid(row=row, column=0, sticky="ew", padx=5, pady=(10, 2))
                row += 1

                valores_unicos = sorted(list(set(str(item.get(col, "")) for item in self.itens_completos if item.get(col) is not None and str(item.get(col, "")).strip() != "")))

                if not valores_unicos:
                    lbl_vazio = ctk.CTkLabel(scrollable_frame, text="Nenhum valor", text_color="gray")
                    lbl_vazio.grid(row=row, column=0, padx=10, pady=2, sticky="w")
                    row += 1
                    continue

                if len(valores_unicos) == 1:
                    lbl_val = ctk.CTkLabel(scrollable_frame, text=valores_unicos[0], font=ctk.CTkFont(size=12, weight="bold"))
                    lbl_val.grid(row=row, column=0, padx=10, pady=2, sticky="w")
                    row += 1
                    self.filtros_widgets[col] = ("label", lbl_val, valores_unicos[0])
                    continue

                # Checkbox para booleanos (0/1)
                primeiro_val = self.itens_completos[0].get(col) if self.itens_completos else None
                if isinstance(primeiro_val, int) and set(valores_unicos).issubset({"0", "1"}):
                    var = tk.IntVar(value=0)
                    cb = ctk.CTkCheckBox(scrollable_frame, text="Sim", variable=var,
                                         command=self._aplicar_filtros)
                    cb.grid(row=row, column=0, pady=2, padx=5, sticky="w")
                    row += 1
                    self.filtros_widgets[col] = ("checkbox", var)
                    continue

                # ComboBox padrão
                combo = ctk.CTkComboBox(scrollable_frame, values=["Todos"] + valores_unicos, width=180, command=self._aplicar_filtros)
                combo.set("Todos")
                combo.grid(row=row, column=0, pady=2, padx=5, sticky="ew")
                row += 1
                self.filtros_widgets[col] = ("combobox", combo)
            
            except Exception as e:
                logger.error("Erro ao criar widget para a coluna '%s': %s", col, e)

        # Filtro de Fabricante (nova lógica)
        if colunas_fabricante:
            lbl = ctk.CTkLabel(scrollable_frame, text="Fabricante", anchor="w")
            lbl.grid(row=row, column=0, sticky="ew", padx=5, pady=(10, 2))
            row += 1
            
            # A combobox de Fabricante deve ter os nomes das colunas como itens
            combo_fab_values = ["Todos"] + colunas_fabricante
            combo_fab = ctk.CTkComboBox(scrollable_frame, values=combo_fab_values, width=180, command=self._aplicar_filtros)
            combo_fab.set("Todos")
            combo_fab.grid(row=row, column=0, pady=2, padx=5, sticky="ew")
            row += 1
            self.filtros_widgets["fabricante"] = ("combobox_fab", combo_fab)
            
        logger.info("Filtros finalizados. Total de widgets: %d", len(self.filtros_widgets))
        self._aplicar_filtros() # Aplica filtros iniciais para carregar dados na tabela

    def _aplicar_filtros(self, *args):
        """Aplica todos os filtros selecionados e atualiza as opções das comboboxes."""
        if not self.itens_completos:
            return
            
        dados_filtrados = []
        
        # Passo 1: Filtrar os dados da tabela com base nos filtros atuais
        for item in self.itens_completos:
            match = True
            for col, (tipo, widget, *_) in self.filtros_widgets.items():
                valor_selecionado = None
                
                # Exclui o filtro de fabricante desta parte
                if tipo == "combobox_fab":
                    continue
                
                if tipo == "combobox":
                    valor_selecionado = widget.get()
                    if valor_selecionado != "Todos" and str(item.get(col)) != valor_selecionado:
                        match = False
                        break
                elif tipo == "checkbox":
                    valor_selecionado = widget.get()
                    if item.get(col, 0) != valor_selecionado:
                        match = False
                        break
                elif tipo == "label":
                    valor_selecionado = widget.cget("text")
                    if str(item.get(col, "")) != valor_selecionado:
                        match = False
                        break
            
            if match:
                dados_filtrados.append(item)
        
        # Passo 2: Aplica o filtro de fabricante (não se atualiza em cascata)
        if "fabricante" in self.filtros_widgets:
            tipo, widget = self.filtros_widgets["fabricante"]
            valor_fab_selecionado = widget.get()
            if valor_fab_selecionado != "Todos":
                # Filtra pelos itens que têm um valor não vazio para a coluna selecionada
                dados_filtrados = [item for item in dados_filtrados if item.get(valor_fab_selecionado) is not None and str(item.get(valor_fab_selecionado)).strip() != ""]
        
        # Passo 3: Atualizar a Treeview com os dados filtrados
        logger.info("Filtros aplicados. Resultados: %d de %d", len(dados_filtrados), len(self.itens_completos))
        self._atualizar_treeview(dados_filtrados)

        # Passo 4: Atualizar as opções dos filtros restantes (exceto fabricante) com base nos dados filtrados
        if not dados_filtrados:
            return
        
        for col_filtro, (tipo, widget, *_) in self.filtros_widgets.items():
            if tipo == "combobox":
                valor_selecionado_atual = widget.get()
                valores_novos = sorted(list(set(str(item.get(col_filtro, "")) for item in dados_filtrados if item.get(col_filtro) is not None and str(item.get(col_filtro, "")).strip() != "")))
                
                # Se não houver valores, limpa a combobox.
                if not valores_novos:
                    widget.configure(values=["Todos"])
                    widget.set("Todos")
                else:
                    valores_atualizados = ["Todos"] + valores_novos
                    widget.configure(values=valores_atualizados)
                    # Tenta manter o valor selecionado se ele ainda existir, caso contrário, redefine para "Todos"
                    if valor_selecionado_atual in valores_atualizados:
                        widget.set(valor_selecionado_atual)
                    else:
                        widget.set("Todos")
