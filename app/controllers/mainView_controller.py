# app/controllers/mainView_controller.py
import logging
from sqlalchemy import Table, MetaData, select
from app.database import engine
from collections import defaultdict

logger = logging.getLogger(__name__)

class MainViewController:

    @staticmethod
    def get_classes():
        """Retorna todas as classes (grupos)"""
        metadata = MetaData()
        grupos = Table("grupos", metadata, autoload_with=engine)
        stmt = select(grupos)
        try:
            with engine.connect() as conn:
                result = conn.execute(stmt).fetchall()
            return [row.nome_classe for row in result]
        except Exception as e:
            logger.error(f"Erro ao buscar classes: {e}")
            return []

    @staticmethod
    def get_categorias_by_classe(nome_classe):
        """Retorna categorias de uma classe"""
        metadata = MetaData()
        categorias = Table("categorias", metadata, autoload_with=engine)
        grupos = Table("grupos", metadata, autoload_with=engine)

        stmt = select(categorias).join(grupos, categorias.c.Classes_idClasses == grupos.c.idClasses)\
                                .where(grupos.c.nome_classe == nome_classe)
        try:
            with engine.connect() as conn:
                result = conn.execute(stmt).fetchall()
            return result
        except Exception as e:
            logger.error(f"Erro ao buscar categorias da classe '{nome_classe}': {e}")
            return []

    @staticmethod
    def get_subcategorias_by_categoria(id_categoria):
        """Retorna subcategorias de uma categoria"""
        metadata = MetaData()
        subcategorias = Table("subcategoria", metadata, autoload_with=engine)

        stmt = select(subcategorias).where(subcategorias.c.categorias_id_categoria == id_categoria)
        try:
            with engine.connect() as conn:
                result = conn.execute(stmt).fetchall()
            return result
        except Exception as e:
            logger.error(f"Erro ao buscar subcategorias da categoria '{id_categoria}': {e}")
            return []

    @staticmethod
    def get_itens_by_subcategoria(nome_subcategoria):
        """Retorna todos os itens da tabela dinâmica indicada pelo campo db_subcategoria"""
        metadata = MetaData()
        try:
            tabela = Table(nome_subcategoria, metadata, autoload_with=engine)
            stmt = select(tabela)
            with engine.connect() as conn:
                result = conn.execute(stmt).fetchall()
            return result
        except Exception as e:
            logger.error(f"Erro ao buscar itens da subcategoria '{nome_subcategoria}': {e}")
            return []
        
    @staticmethod
    def get_renomear(db_sub: str):
        """
        Retorna um dicionário: {nome_coluna_original: nome_amigavel}
        filtrando pela subcategoria (db_sub) na tabela renomear.s
        """
        metadata = MetaData()
        renomear = Table("renomear", metadata, autoload_with=engine)

        stmt = select(renomear).where(renomear.c.renomear_coluna == db_sub)
        with engine.connect() as conn:
            rows = conn.execute(stmt).fetchall()

        # supondo que as colunas da tabela sejam exatamente:
        # db_subcategoria | coluna | renomeada
        logger.debug(f"Mapeamento de renomeação para '{db_sub}': {rows}")
        return {r.renomear_coluna: r.renomear_colunaRenomeada for r in rows}
    

    @staticmethod
    def get_descricao_subcategoria(nome_subcategoria: str, dados_item: dict | None = None) -> str:
        """
        Busca a máscara de descrição para a subcategoria e
        retorna a descrição já formatada.

        Se dados_item estiver vazio ou faltar alguma chave,
        os campos são preenchidos com string vazia.
        """
        logger.info(f"Buscando descrição para subcategoria '{nome_subcategoria}' com dados: {dados_item}")
        metadata = MetaData()
        subcategorias = Table("subcategoria", metadata, autoload_with=engine)
        stmt = select(subcategorias.c.descricao_subcategoria).where(
            subcategorias.c.nome_subcategoria == nome_subcategoria
        )

        mascara_descricao = ""
        try:
            with engine.connect() as conn:
                mascara_descricao = conn.execute(stmt).scalar_one_or_none()
        except Exception as e:
            logger.error(f"Erro ao buscar a descrição da subcategoria '{nome_subcategoria}': {e}")
            return "Erro ao buscar máscara de descrição."

        logger.info(f"Máscara de descrição para '{nome_subcategoria}': {mascara_descricao}")

        if not mascara_descricao:
            return ""  # não tem máscara, retorna vazio

        # garante dict com valores vazios se não existir chave
        dados_seguro = defaultdict(str, dados_item or {})

        try:
            return mascara_descricao.format(**dados_seguro)
        except Exception as e:
            logger.error(f"Erro ao formatar descrição: {e}")
            return "Erro ao formatar descrição. Verifique os dados."
        
    @staticmethod
    def montar_descricao(item, mascara):
        """
        Monta a descrição do item baseado na máscara fornecida.
        A máscara pode conter placeholders como {campo1}, {campo2}, etc.
        """
        if not mascara:
            return "Descrição não disponível"
        
        descricao = mascara
        for key, value in item.items():
            placeholder = f"{{{key}}}"
            if placeholder in descricao:
                descricao = descricao.replace(placeholder, str(value) if value is not None else "")
        
        # Limpa espaços extras
        descricao = ' '.join(descricao.split())
        return descricao
    
    @staticmethod
    def unidade_medida_to_abreviacao(unidade):
        """Converte unidade de medida para abreviação"""
        mapping = {
            "Unidade": "un",
            "Unidade(s)": "un", 
            "peça": "pc",
            "Peça": "pc",
            "Peça(s)": "pc",
            "Pacote(s)": "pct", 
            "Pacote": "pct",
            "Caixa": "cx",
            "Caixa(s)": "cx",
            "Metro": "m",
            "Metros": "m",
            "Milímetro": "mm",
            "Milímetro(s)": "mm", 
            "Litro": "lt",
            "Litros": "lt",
            "Grama": "g",  
            "Gramas": "g",
            "Quilo(s)": "kg",    
            "Quilo": "kg",
            # Adicione mais conforme necessário
        }
        return mapping.get(unidade,"")  # Retorna a abreviação ou a própria unidade se não encontrada
    
    @staticmethod
    def get_unidade_medida(nome_subcategoria):
        """Retorna a máscara de descrição para uma subcategoria."""
        metadata = MetaData()
        subcategorias = Table("subcategoria", metadata, autoload_with=engine)
        
        stmt = select(subcategorias.c.unidade_medida).where(subcategorias.c.nome_subcategoria == nome_subcategoria)
        
        try:
            with engine.connect() as conn:
                result = conn.execute(stmt).scalar_one_or_none()
            return result
        except Exception as e:
            logger.error(f"Erro ao buscar a unidade da subcategoria '{nome_subcategoria}': {e}")
            return None