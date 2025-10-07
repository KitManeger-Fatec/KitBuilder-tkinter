import customtkinter as ctk
from tkinter import ttk, messagebox
from app.utils.logger_config import get_logger
from app.config.themes.colors import COLORS
from app.controllers.pedidoView_controller import PedidoViewController,AppState


logger = get_logger(__name__)

class PedidoView(ctk.CTkFrame):
    def __init__(self, parent, router=None, controller=None):
        super().__init__(parent)
        self.router = router
        self.controller = controller  # instância do PedidoViewController
        PedidoViewController.view = self

        if self.controller is None:
            raise ValueError("PedidoView precisa de um controller válido")

        self.pack(fill="both", expand=True)

        # --- Usuário logado ---
        usuario = PedidoViewController.usuario_logado or {
            "nome": "Desconhecido", 
            "cargo": "nenhum", 
            "nivel": "0"
            }

        # ----- FRAME SUPERIOR -----
        self.frame_top = ctk.CTkFrame(self)
        self.frame_top.pack(fill="x", padx=10, pady=5)

        # Labels Usuário, Cargo, Nível
        self.label_usuario = ctk.CTkLabel(self.frame_top, text="Usuário Logado:")
        self.label_usuario.grid(row=0, column=0, padx=5, pady=5)
        self.usuario = ctk.CTkLabel(self.frame_top, text=usuario.get("nome", ""))
        self.usuario.grid(row=0, column=1, padx=5, pady=5, columnspan=3, sticky="w")

        self.label_cargo = ctk.CTkLabel(self.frame_top, text="Cargo:")
        self.label_cargo.grid(row=0, column=4, padx=5, pady=5)
        self.cargo = ctk.CTkLabel(self.frame_top, text=usuario.get("cargo", ""))
        self.cargo.grid(row=0, column=5, padx=5, pady=5, columnspan=3, sticky="w")

        self.label_nivel = ctk.CTkLabel(self.frame_top, text="Nível:")
        self.label_nivel.grid(row=0, column=8, padx=5, pady=5)
        self.nivel = ctk.CTkLabel(self.frame_top, text=usuario.get("nivel", ""))
        self.nivel.grid(row=0, column=9, padx=5, pady=5, columnspan=2, sticky="w")

        # Nome do Projeto
        self.label_nome_projeto = ctk.CTkLabel(self.frame_top, text="Nome do Projeto:")
        self.label_nome_projeto.grid(row=1, column=0, padx=5, pady=5)
        self.entry_projeto = ctk.CTkEntry(self.frame_top)
        self.entry_projeto.grid(row=1, column=1, padx=5, pady=5, columnspan=9)
        self.entry_projeto.insert(0, AppState.projeto_nome)
        self.entry_projeto.bind("<KeyRelease>", self.atualizar_projeto)

        # Nome da Lista
        self.label_nome_lista = ctk.CTkLabel(self.frame_top, text="Nome da Lista:")
        self.label_nome_lista.grid(row=2, column=0, padx=5, pady=5)
        self.entry_lista = ctk.CTkEntry(self.frame_top)
        self.entry_lista.grid(row=2, column=1, padx=5, pady=5, columnspan=9)
        self.entry_lista.insert(0, AppState.lista_nome)
        self.entry_lista.bind("<KeyRelease>", self.atualizar_lista)

        # ----- FRAME EDIÇÃO DE ITEM -----
        self.frame_edicao = ctk.CTkFrame(self)
        self.frame_edicao.pack(fill="x", padx=10, pady=5)

        self.entry_qtd = ctk.CTkEntry(self.frame_edicao, placeholder_text="QTD")
        self.entry_qtd.bind("<Return>", self.atualizar_quantidade)
        self.entry_qtd.grid(row=0, column=0, padx=5)

        self.entry_codigo = ctk.CTkEntry(self.frame_edicao, placeholder_text="Código", state="disabled")
        self.entry_codigo.grid(row=0, column=1, padx=5)

        self.entry_desc = ctk.CTkEntry(self.frame_edicao, placeholder_text="Descrição", state="disabled")
        self.entry_desc.grid(row=0, column=2, padx=5)

        self.btn_remover = ctk.CTkButton(self.frame_edicao, text="Remover", command=self.remover_item)
        self.btn_remover.grid(row=0, column=3, padx=5)

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

        # ----- BOTÕES -----
        self.frame_botoes = ctk.CTkFrame(self)
        self.frame_botoes.pack(fill="x", pady=10)

        self.btn_voltar = ctk.CTkButton(
            self.frame_botoes,
            text="Voltar",
            command=lambda: router.show_main() if router else None
        )
        self.btn_voltar.pack(side="left", padx=10)

        self.btn_encerrar = ctk.CTkButton(
            self.frame_botoes,
            text="Encerrar Pedido",
            fg_color=COLORS["danger"],
            command=self.encerrar_pedido
        )
        self.btn_encerrar.pack(side="right", padx=10)

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
