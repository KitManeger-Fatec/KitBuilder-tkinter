# app/controllers/pedidoView_controller.py

class PedidoViewController:
    itens = []  # lista de tuplas (produto, quantidade)

    @classmethod
    def add_item(cls, produto, quantidade):
        cls.itens.append((produto, quantidade))
