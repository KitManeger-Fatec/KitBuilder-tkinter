
import customtkinter as ctk
from app.config.themes.colors import COLORS
from app.config.themes.fonts import FONTS   
from app.controllers.mainView_controller import MainViewController

def criar_footer(frame_parent, itens_completos, idx_item, controller, fab_combobox=None, descricao_montada=None):

    footer = ctk.CTkFrame(frame_parent, height=40, fg_color="transparent")
    footer.pack(side="bottom", fill="x", pady=(0,10))

    if idx_item >= len(itens_completos):
        return footer
    item = itens_completos[idx_item]

    def aumentar(): var_qtd.set(var_qtd.get() + 1)
    def diminuir():
        if var_qtd.get() > 1:
            var_qtd.set(var_qtd.get() - 1)

    btn_menos = ctk.CTkButton(footer, text="-", width=25, command=diminuir, font=FONTS["button"])
    btn_menos.pack(side="left", padx=(5,2))
    var_qtd = ctk.IntVar(value=1)
    entry_qtd = ctk.CTkEntry(footer, width=50, textvariable=var_qtd, justify="center", font=FONTS["button"])
    entry_qtd.pack(side="left", padx=(5,5))
    btn_mais = ctk.CTkButton(footer, text="+", width=25, command=aumentar, font=FONTS["button"])
    btn_mais.pack(side="left", padx=(2,10))

    def adicionar_item():
    # Pega o fabricante selecionado da combobox
        fabricante = fab_combobox.get() if fab_combobox else item.get("fabricante", "")
        
        descricao = descricao_montada if descricao_montada else item.get("descricao_produto", "")
        # Se estiver como "Escolha um Fabricante" ou "Todos", envia vazio
        if fabricante in ("Escolha um Fabricante", "Todos"):
            fabricante = ""
            codigo_fab = ""
        else:
            # Busca o código correspondente no mapeamento do item
            codigo_fab = item.get("fabricantes_cod_map", {}).get(fabricante, "")

        controller.add_item(
            codigo=item.get("codigo_produto", ""),
            descricao=descricao,
            quantidade=var_qtd.get(),
            medida=item.get("medida", ""),
            fabricante=fabricante,
            codigo_fabricante=item.get(fabricante,"")
        )
        print(f"Item adicionado: {item.get('codigo_produto','')}, qtd={var_qtd.get()}, fab={fabricante}")

    btn_add = ctk.CTkButton(footer, text="Adicionar ao Pedido", command=adicionar_item, font=FONTS["button"])
    btn_add.pack(side="left", padx=10)

    return footer
