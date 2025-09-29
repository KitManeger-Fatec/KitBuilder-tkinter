import customtkinter as ctk
from tkinter import ttk
from app.controllers.pedidoView_controller import PedidoViewController, AppState


class PedidoView(ctk.CTkFrame):
    def __init__(self, parent, router=None):
        super().__init__(parent)
        self.router = router
        self.pack(fill="both", expand=True)

        # ----- FRAME SUPERIOR -----
        self.frame_top = ctk.CTkFrame(self)
        self.frame_top.pack(fill="x", padx=10, pady=5)

        usuario = PedidoViewController.usuario_logado or {"nome": "Desconhecido", "cargo": "", "nivel": ""}

        # Labels Usuário, Cargo, Nível
        ctk.CTkLabel(self.frame_top, text=f"Usuário: {usuario['nome']}").grid(row=0, column=0, padx=5)
        ctk.CTkLabel(self.frame_top, text=f"Cargo: {usuario['cargo']}").grid(row=0, column=1, padx=5)
        ctk.CTkLabel(self.frame_top, text=f"Nível: {usuario['nivel']}").grid(row=0, column=2, padx=5)

        # Nome do Projeto
        self.entry_projeto = ctk.CTkEntry(self.frame_top)
        self.entry_projeto.grid(row=1, column=0, padx=5, pady=5)
        self.entry_projeto.insert(0, AppState.projeto_nome)
        self.entry_projeto.bind("<KeyRelease>", self.atualizar_projeto)

        # Nome da Lista
        self.entry_lista = ctk.CTkEntry(self.frame_top)
        self.entry_lista.grid(row=1, column=1, padx=5, pady=5)
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
        self.tree_itens = ttk.Treeview(self, columns=("quantidade","medida","codigo","produto","fabricante","cod_fab"), show="headings")
        for col, text in [("quantidade","QTD"), ("medida","Medida"), ("codigo","Código"),
                        ("produto","Produto"), ("fabricante","Fabricante"), ("cod_fab","Cód. Fabricante")]:
            self.tree_itens.heading(col, text=text)

        self.tree_itens.pack(fill="both", expand=True, padx=20, pady=10)
        self.tree_itens.bind("<<TreeviewSelect>>", self.on_item_selected)

        # ----- BOTÃO VOLTAR -----
        self.btn_voltar = ctk.CTkButton(self, text="Voltar", command=lambda: router.show_main() if router else None)
        self.btn_voltar.pack(pady=10)

        self.atualizar_itens()

    # ----- MÉTODOS -----
    def atualizar_itens(self):
        self.tree_itens.delete(*self.tree_itens.get_children())
        for item in PedidoViewController.itens:
            self.tree_itens.insert("", "end", values=(
                item.get("quantidade",""),
                item.get("medida",""),
                item.get("codigo",""),
                item.get("produto",""),
                item.get("fabricante",""),
                item.get("codigo_fabricante","")
            ))

    def on_item_selected(self, event):
        selected = self.tree_itens.selection()
        if not selected:
            return
        idx = self.tree_itens.index(selected[0])
        item = PedidoViewController.itens[idx]

        # Preenche os campos de edição
        self.entry_qtd.delete(0, "end")
        self.entry_qtd.insert(0, item.get("quantidade",""))

        self.entry_codigo.configure(state="normal")
        self.entry_codigo.delete(0, "end")
        self.entry_codigo.insert(0, item.get("codigo",""))
        self.entry_codigo.configure(state="disabled")

        self.entry_desc.configure(state="normal")
        self.entry_desc.delete(0, "end")
        self.entry_desc.insert(0, item.get("produto",""))   # ou a chave correta
        self.entry_desc.configure(state="disabled")

    def remover_item(self):
        codigo = self.entry_codigo.get()
        if codigo:
            PedidoViewController.remover_item(codigo)
            self.atualizar_itens()

    def atualizar_quantidade(self, event=None):
        codigo = self.entry_codigo.get()
        nova_qtd = self.entry_qtd.get()

        if not codigo or not nova_qtd.isdigit():
            return

        # atualiza o item no controller
        for item in PedidoViewController.itens:
            if item["codigo"] == codigo:
                item["quantidade"] = int(nova_qtd)
                break

        # atualiza a treeview
        self.atualizar_itens()

    def atualizar_projeto(self, event=None):
        AppState.projeto_nome = self.entry_projeto.get()

    def atualizar_lista(self, event=None):
        AppState.lista_nome = self.entry_lista.get()

