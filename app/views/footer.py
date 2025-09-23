import customtkinter as ctk
import tkinter as tk    
from app.controllers.pedidoView_controller import PedidoViewController
from app.config.themes.fonts import FONTS   
from app.config.themes.colors import COLORS

# ---- Métodos de interface para os botões de quantidade ----

def criar_footer(parent_frame, treeview, router=None):
    """
    Cria footer com:
    - Botões + e -
    - Entry editável de quantidade
    - Botão Adicionar ao Pedido (usa item selecionado na treeview)
    - Botão Ir para Pedido
    """

    footer_frame = ctk.CTkFrame(parent_frame, fg_color="transparent", height=50)
    footer_frame.grid(row=1, column=0, columnspan=2, sticky="we", pady=10)
    footer_frame.grid_columnconfigure((0,1,2,3,4), weight=0)
    footer_frame.grid_propagate(False)

    # Variável quantidade
    quantidade = tk.IntVar(value=1)

    # --- Funções ---
    def diminuir():
        if quantidade.get() > 1:
            quantidade.set(quantidade.get() - 1)

    def aumentar():
        quantidade.set(quantidade.get() + 1)

    def validar(valor_digitado):
        if not valor_digitado:
            return True
        try:
            v = int(valor_digitado)
            if v > 0:
                quantidade.set(v)
                return True
        except ValueError:
            pass
        return False

    vcmd = (footer_frame.register(validar), "%P")

    def adicionar_pedido():
        selected = treeview.selection()
        if not selected:
            print("Nenhum item selecionado!")
            return
        idx = treeview.index(selected[0])
        if idx < len(treeview.get_children()):
            # Pegando os valores do item selecionado
            item = treeview.item(selected[0])['values']
            produto = item[0]  # ou outro índice que corresponda ao nome do produto
            qtd = quantidade.get()
            PedidoViewController.add_item(produto, qtd)
            print(f"Adicionado ao pedido: {produto} x {qtd}")

    # --- Widgets ---
    ctk.CTkButton(footer_frame, text="-", width=40, command=diminuir).grid(row=0, column=0, padx=(10,5))
    ctk.CTkEntry(footer_frame, width=60, justify="center", textvariable=quantidade,
                validate="key", validatecommand=vcmd).grid(row=0, column=1)
    ctk.CTkButton(footer_frame, text="+", width=40, command=aumentar).grid(row=0, column=2, padx=(5,10))
    ctk.CTkButton(footer_frame, text="Adicionar ao Pedido", width=150,
                command=adicionar_pedido).grid(row=0, column=3, padx=20)

    return footer_frame, quantidade, adicionar_pedido
