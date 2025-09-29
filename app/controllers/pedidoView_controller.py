import logging

logger = logging.getLogger(__name__)

class PedidoViewController:
    usuario_logado = None   # dict com campos: id, nome, cargo, nivel
    nome_projeto = ""
    nome_lista = ""
    itens = []  # lista de dicionários representando itens do pedido

    @classmethod
    def set_usuario_logado(cls, usuario_dict):
        cls.usuario_logado = usuario_dict
        logger.info(f"Usuário logado: {usuario_dict}")

    @classmethod
    def add_item(cls, codigo, descricao, quantidade, medida, fabricante, codigo_fabricante):
        cls.itens.append({
            "codigo": codigo,
            "produto": descricao,
            "quantidade": quantidade,
            "medida": medida,
            "fabricante": fabricante,
            "codigo_fabricante": codigo_fabricante
        })
        logger.info(f"Item adicionado: {codigo}, qtd={quantidade}, fab={fabricante}")

    @classmethod
    def remover_item(cls, codigo):
        before = len(cls.itens)
        cls.itens = [i for i in cls.itens if i["codigo"] != codigo]
        after = len(cls.itens)
        logger.info(f"Item removido: {codigo}, {before-after} removido(s)")

class AppState:
    """Armazena estado global da aplicação"""
    projeto_nome = ""
    lista_nome = ""
    funcionario_logado_id = None