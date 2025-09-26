import customtkinter as ctk
from tkinter import ttk
from app.controllers.pedidoView_controller import PedidoViewController
from app.config.themes.colors import COLORS 
from app.config.themes.fonts import FONTS
from app.utils.logger_config import get_logger
logger = get_logger(__name__)

class PedidoView(ctk.CTkFrame):
    def __init__(self, parent, router=None):
        super().__init__(parent)
        self.router = router
        self.pack(fill="both", expand=True)

        # Treeview para mostrar itens do pedido
        self.tree_itens = ttk.Treeview(self, columns=("quantidade","medida","codigo","produto","fabricante","cod_fab"), show="headings")
        self.tree_itens.heading("quantidade", text="Quantidade")
        self.tree_itens.heading("medida", text="Medida")
        self.tree_itens.heading("produto", text="Produto")
        self.tree_itens.heading("fabricante", text="Fabricante")
        self.tree_itens.heading("cod_fab", text="Cód. Fabricante")
        self.tree_itens.heading("codigo", text="Código")

        self.tree_itens.pack(fill="both", expand=True, padx=20, pady=20)

        # Botão voltar
        ctk.CTkButton(self, text="Voltar", command=lambda: router.show_main() if router else None).pack(pady=10)

        # Atualiza a tree com itens do pedido
        self.atualizar_itens()

    def atualizar_itens(self):
        """Preenche a Treeview com os itens do PedidoViewController"""
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
