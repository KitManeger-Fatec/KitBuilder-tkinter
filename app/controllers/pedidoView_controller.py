from app.utils.logger_config import get_logger

logger = get_logger(__name__)

class PedidoViewController:
    itens = []  # lista de dicionários

    @classmethod
    def add_item(cls, codigo, descricao, quantidade,
                medida, fabricante, codigo_fabricante):
        """Adiciona item ao pedido (lista estática)"""
        cls.itens.append({
            "codigo": codigo,
            "produto": descricao,  # nome consistente
            "quantidade": quantidade,
            "medida": medida,
            "fabricante": fabricante,
            "codigo_fabricante": codigo_fabricante
        })
