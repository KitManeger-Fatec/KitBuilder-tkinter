import customtkinter as ctk
from tkinter import ttk
from app.controllers.pedidoView_controller import PedidoViewController

class PedidoView(ctk.CTkFrame):
    def __init__(self, parent, router=None):
        super().__init__(parent)
        self.router = router
        self.pack(fill="both", expand=True)

        # Treeview para mostrar itens do pedido
        self.tree_itens = ttk.Treeview(self, columns=("produto", "quantidade"), show="headings")
        self.tree_itens.heading("produto", text="Produto")
        self.tree_itens.heading("quantidade", text="Quantidade")
        self.tree_itens.pack(fill="both", expand=True, padx=20, pady=20)

        # Botão voltar
        ctk.CTkButton(self, text="Voltar", command=lambda: router.show_principal() if router else None).pack(pady=10)

        # Atualiza a tree com itens do pedido
        self.atualizar_itens()

    def atualizar_itens(self):
        """Preenche a Treeview com os itens do PedidoViewController"""
        self.tree_itens.delete(*self.tree_itens.get_children())
        for produto, qtd in PedidoViewController.itens:
            self.tree_itens.insert("", "end", values=(produto, qtd))
