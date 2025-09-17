# app/controllers/categoria_controller.py
import logging
from app.database import SessionLocal
from app.models.categoria import Categoria
from app.models.subcategoria import Subcategoria

logger = logging.getLogger(__name__)

class CategoriaController:

    @staticmethod
    def get_classes():
        """Retorna a lista de classes distintas (nome_classe)"""
        logger.debug("Buscando classes distintas no banco")
        try:
            with SessionLocal() as session:
                result = session.query(Categoria.nome_classe).distinct().all()
                classes = [r[0] for r in result]
                return classes or ["-- Nenhuma classe --"]
        except Exception as e:
            logger.error(f"Erro ao buscar classes: {e}")
            return ["-- Erro ao carregar --"]

    @staticmethod
    def get_categorias_by_classe(nome_classe: str):
        """Retorna todas as categorias de uma classe específica"""
        logger.debug(f"Buscando categorias para classe: {nome_classe}")
        try:
            with SessionLocal() as session:
                categorias = session.query(Categoria)\
                                    .filter(Categoria.nome_classe == nome_classe)\
                                    .all()
                return categorias
        except Exception as e:
            logger.error(f"Erro ao buscar categorias: {e}")
            return []

    @staticmethod
    def get_subcategorias_by_categoria(id_categoria: int):
        """Retorna todas as subcategorias de uma categoria específica"""
        logger.debug(f"Buscando subcategorias para categoria id={id_categoria}")
        try:
            with SessionLocal() as session:
                subs = session.query(Subcategoria)\
                              .filter(Subcategoria.categorias_id_categoria == id_categoria)\
                              .all()
                return subs
        except Exception as e:
            logger.error(f"Erro ao buscar subcategorias: {e}")
            return []
