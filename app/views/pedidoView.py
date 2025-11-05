import customtkinter as ctk
from tkinter import ttk, messagebox
from app.utils.logger_config import get_logger
from app.config.themes.colors import COLORS
from app.controllers.pedidoView_controller import PedidoViewController,AppState
from app.utils.session_manager import SessionManager
from app.config.themes.fonts import FONTS
from app.config.themes.colors import COLORS


logger = get_logger(__name__)

class PedidoView(ctk.CTkFrame):
    def __init__(self, parent, router=None, controller=None):
        super().__init__(parent)
        self.router = router
        self.controller = controller  # instância do PedidoViewController
        PedidoViewController.view = self

        if self.controller is None:
            raise ValueError("PedidoView precisa de um controller válido")
        
    
                # --- Usuário logado ---
        PedidoViewController.set_usuario_logado(SessionManager.get_usuario_id())
        usuario = PedidoViewController.usuario_logado or {
            "nome": "Desconhecido", 
            "cargo": "nenhum", 
            "nivel": "0"
        }

        self.pack(fill="both", expand=True)

        # ----- FRAME SUPERIOR (Top Bar Moderna) -----
        self.frame_top = ctk.CTkFrame(self, fg_color=COLORS["panel"], corner_radius=12)
        self.frame_top.pack(fill="x", padx=15, pady=15)

        # Grade mais proporcional
        self.frame_top.grid_columnconfigure(0, weight=0)
        self.frame_top.grid_columnconfigure(1, weight=0)
        self.frame_top.grid_columnconfigure(2, weight=0)
        self.frame_top.grid_columnconfigure(3, weight=0)
        self.frame_top.grid_columnconfigure(4, weight=0)
        self.frame_top.grid_columnconfigure(5, weight=0)
        self.frame_top.grid_columnconfigure(6, weight=1)

        # Estilos consistentes
        LABEL = FONTS["subtitle"]
        VALUE = FONTS["text"]
        PADX = 10
        PADY = 5

        # ---- Linha 1: Usuário | Cargo | Nível ----
        self.label_usuario = ctk.CTkLabel(self.frame_top, text="Usuário:", font=LABEL)
        self.label_usuario.grid(row=0, column=1, padx=PADX, pady=PADY, sticky="w")

        self.usuario = ctk.CTkLabel(self.frame_top, text=usuario.get("nome", ""), font=VALUE)
        self.usuario.grid(row=0, column=2, padx=(0,PADX), pady=PADY, sticky="w")

        self.label_cargo = ctk.CTkLabel(self.frame_top, text="Cargo:", font=LABEL)
        self.label_cargo.grid(row=0, column=3, padx=PADX, pady=PADY, sticky="w")

        self.cargo = ctk.CTkLabel(self.frame_top, text=usuario.get("cargo", ""), font=VALUE)
        self.cargo.grid(row=0, column=4, padx=(0,PADX), pady=PADY, sticky="w")

        self.label_nivel = ctk.CTkLabel(self.frame_top, text="Nível:", font=LABEL)
        self.label_nivel.grid(row=0, column=5, padx=PADX, pady=PADY, sticky="w")

        self.nivel = ctk.CTkLabel(self.frame_top, text=usuario.get("nivel", ""), font=VALUE)
        self.nivel.grid(row=0, column=6, padx=(0,PADX), pady=PADY, sticky="w")

        # Margem entre seção 1 e 2
        ctk.CTkLabel(self.frame_top, text="").grid(row=1, column=0)

        # ---- Linha 2: Nome do Projeto ----
        self.label_nome_projeto = ctk.CTkLabel(self.frame_top, text="Nome do Projeto:", font=LABEL)
        self.label_nome_projeto.grid(row=2, column=0, padx=PADX, pady=PADY, sticky="w")

        self.entry_projeto = ctk.CTkEntry(self.frame_top, height=35, corner_radius=8)
        self.entry_projeto.grid(row=2, column=1, columnspan=5, padx=0, pady=PADY, sticky="we")
        self.entry_projeto.insert(0, AppState.projeto_nome)
        self.entry_projeto.bind("<KeyRelease>", self.atualizar_projeto)

        # ---- Linha 3: Nome da Lista ----
        self.label_nome_lista = ctk.CTkLabel(self.frame_top, text="Nome da Lista:", font=LABEL)
        self.label_nome_lista.grid(row=3, column=0, padx=PADX, pady=PADY, sticky="w")

        self.entry_lista = ctk.CTkEntry(self.frame_top, height=35, corner_radius=8)
        self.entry_lista.grid(row=3, column=1, columnspan=5, padx=0, pady=PADY, sticky="we")
        self.entry_lista.insert(0, AppState.lista_nome)
        self.entry_lista.bind("<KeyRelease>", self.atualizar_lista)


        # ----- FRAME EDIÇÃO DE ITEM -----
        self.frame_edicao = ctk.CTkFrame(self)
        self.frame_edicao.pack(fill="x", padx=10, pady=10)

        # Grid mais organizado
        self.frame_edicao.grid_columnconfigure(0, weight=0)   # qtd
        self.frame_edicao.grid_columnconfigure(1, weight=0)   # codigo
        self.frame_edicao.grid_columnconfigure(2, weight=1)   # descrição grande
        self.frame_edicao.grid_columnconfigure(3, weight=0)   # remover
        self.frame_edicao.grid_columnconfigure(4, weight=0)   # voltar
        self.frame_edicao.grid_columnconfigure(5, weight=0)   # encerrar

        PADX = 8
        PADY = 6

        # QTD
        self.entry_qtd = ctk.CTkEntry(
            self.frame_edicao,
            placeholder_text="Quantidade",
            width=80
        )
        self.entry_qtd.bind("<Return>", self.atualizar_quantidade)
        self.entry_qtd.grid(row=0, column=0, padx=PADX, pady=PADY, sticky="we")

        # Código
        self.entry_codigo = ctk.CTkEntry(self.frame_edicao, placeholder_text="Código do produto", width=120, state="disabled")
        self.entry_codigo.grid(row=0, column=1, padx=PADX, pady=PADY)

        # coluna da descrição
        self.frame_edicao.grid_columnconfigure(2, weight=1, minsize=200)

        self.entry_desc = ctk.CTkEntry(
            self.frame_edicao,
            placeholder_text="Descrição do produto",
            state="disabled"
        )
        self.entry_desc.grid(row=0, column=2, padx=PADX, pady=PADY, sticky="we")

        # Botão Remover
        self.btn_remover = ctk.CTkButton(self.frame_edicao, text="Remover Item", width=100, 
                                        font=FONTS["button"],command=self.remover_item)
        self.btn_remover.grid(row=0, column=3, padx=PADX, pady=PADY)

        # --- Botão Voltar (agora na barra de edição) ---
        self.btn_voltar = ctk.CTkButton(
            self.frame_edicao,
            text="Voltar à Tela Principal",
            width=100,font=FONTS["button"],
            command=lambda: router.show_main() if router else None
        )
        self.btn_voltar.grid(row=0, column=4, padx=PADX, pady=PADY)

        # --- Botão Encerrar Pedido (agora na barra de edição) ---
        self.btn_encerrar = ctk.CTkButton(
            self.frame_edicao,
            text="Encerrar Pedido",
            width=150,font=FONTS["button"],
            fg_color=COLORS["danger"],
            command=self.encerrar_pedido
        )
        self.btn_encerrar.grid(row=0, column=5, padx=(PADX,100), pady=PADY)


        # ----- TREEVIEW ITENS -----

        self.tree_itens = ttk.Treeview(
            self,
            columns=("quantidade", "medida", "codigo", "produto", "fabricante", "cod_fab"),
            show="headings"
        )
        for col, text_col in [
            ("quantidade", "QTD"),
            ("medida", "Medida"),
            ("codigo", "Código"),
            ("produto", "Produto"),
            ("fabricante", "Fabricante"),
            ("cod_fab", "Cód. Fabricante")
        ]:
            self.tree_itens.heading(col, text=text_col)
            self.tree_itens.column(col, width=100)
        self.tree_itens.pack(fill="both", expand=True, padx=20, pady=10)
        self.tree_itens.bind("<<TreeviewSelect>>", self.on_item_selected)


        # Atualiza treeview
        self.atualizar_itens()

    # -----------------------------
    # MÉTODOS
    # -----------------------------
    def atualizar_itens(self):
        self.tree_itens.delete(*self.tree_itens.get_children())
        for item in self.controller.itens:
            self.tree_itens.insert("", "end", values=(
                item.get("quantidade", ""),
                item.get("medida", ""),
                item.get("codigo", ""),
                item.get("produto", ""),
                item.get("fabricante", ""),
                item.get("codigo_fabricante", "")
            ))

    def on_item_selected(self, event):
        selected = self.tree_itens.selection()
        if not selected:
            self.item_selecionado = None
            return

        idx = self.tree_itens.index(selected[0])
        self.item_selecionado = self.controller.itens[idx]

        self.entry_qtd.delete(0, "end")
        self.entry_qtd.insert(0, self.item_selecionado.get("quantidade", ""))

        self.entry_codigo.configure(state="normal")
        self.entry_codigo.delete(0, "end")
        self.entry_codigo.insert(0, self.item_selecionado.get("codigo", ""))
        self.entry_codigo.configure(state="disabled")

        self.entry_desc.configure(state="normal")
        self.entry_desc.delete(0, "end")
        self.entry_desc.insert(0, self.item_selecionado.get("produto", ""))
        self.entry_desc.configure(state="disabled")

    def adicionar_item(self):
        if not hasattr(self, "item_selecionado") or not self.item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um item para adicionar.")
            return

        try:
            codigo = self.item_selecionado.get("codigo", "")
            produto = self.item_selecionado.get("produto", "")
            medida = self.item_selecionado.get("medida", "")

            qtd_str = self.entry_qtd.get()
            if not qtd_str.isdigit() or int(qtd_str) <= 0:
                messagebox.showwarning("Aviso", "Quantidade inválida.")
                return
            quantidade = int(qtd_str)

            fabricante = ""
            codigo_fab = ""

            self.controller.add_item(
                codigo=codigo,
                produto=produto,
                quantidade=quantidade,
                medida=medida,
                fabricante=fabricante,
                codigo_fabricante=codigo_fab
            )

            logger.info(f"Item adicionado: {produto}, Quantidade: {quantidade}")
            self.atualizar_itens()

        except Exception as e:
            logger.exception(f"Erro ao adicionar item: {e}")
            messagebox.showerror("Erro", f"Não foi possível adicionar o item.\n{e}")

    def remover_item(self):
        codigo = self.entry_codigo.get()
        if codigo:
            self.controller.remover_item(codigo)
            self.atualizar_itens()
            self.item_selecionado = None

    def atualizar_quantidade(self, event=None):
        codigo = self.entry_codigo.get()
        nova_qtd = self.entry_qtd.get()
        if not codigo or not nova_qtd.isdigit():
            return
        self.controller.atualizar_quantidade(codigo, int(nova_qtd))
        self.atualizar_itens()


    def encerrar_pedido(self):
        try:
            self.controller.finalizar_pedido()
            self.atualizar_itens()
        except Exception as e:
            logger.exception("Erro ao encerrar pedido")
            messagebox.showerror("Erro", f"Não foi possível encerrar o pedido.\n{e}")

    def atualizar_projeto(self, event=None):
        AppState.projeto_nome = self.entry_projeto.get()

    def atualizar_lista(self, event=None):
        AppState.lista_nome = self.entry_lista.get()
