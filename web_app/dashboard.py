from flask import Blueprint, render_template, request, send_from_directory
import requests
import os
from app.utils.logger_config import get_logger   # 👈 importa seu logger

API_URL = "http://127.0.0.1:8000"
dashboard_bp = Blueprint("dashboard_bp", __name__, template_folder="templates")

# logger do módulo
logger = get_logger(__name__)   # 👈 cria o logger específico do dashboard

# Caminho absoluto correto para a pasta de imagens
ASSETS_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "images")


# ================================
#  SERVIR IMAGENS
# ================================
@dashboard_bp.route("/assets/images/<path:filename>")
def serve_image(filename):
    logger.debug(f"[IMAGEM] Solicitada imagem: {filename}")
    return send_from_directory(ASSETS_FOLDER, filename)


# ================================
#  DASHBOARD PRINCIPAL
# ================================
@dashboard_bp.route("/dashboard/<int:user_id>")
def dashboard(user_id):

    logger.debug(f"\n===== ABRINDO DASHBOARD (user_id={user_id}) =====")

    # Pedidos
    logger.debug(f"[API] GET {API_URL}/pedidos")
    pedidos = requests.get(f"{API_URL}/pedidos").json()
    logger.debug(f"[API RESPONSE] pedidos: {pedidos}")

    # Chefias
    logger.debug(f"[API] GET {API_URL}/chefes/{user_id}")
    chefias = requests.get(f"{API_URL}/chefes/{user_id}").json()
    logger.debug(f"[API RESPONSE] chefias: {chefias}")

    ids_chefia = [c.get("id_confere") for c in chefias]
    logger.debug(f"[DEBUG] IDs de chefia extraídos: {ids_chefia}")

    # Funcionário
    logger.debug(f"[API] GET {API_URL}/dadosFuncionarios/{user_id}")
    func_api = requests.get(f"{API_URL}/dadosFuncionarios/{user_id}").json()
    logger.debug(f"[API RESPONSE] funcionario: {func_api}")

    funcionario = {
        "nome": func_api.get("nome_funcionario"),
        "cargo": func_api.get("cargo_funcionario"),
        "nivel": func_api.get("nivel_funcionario")
    }
    logger.debug(f"[DEBUG] Funcionário montado: {funcionario}")

    return render_template(
        "dashboard.html",
        pedidos=pedidos,
        funcionario=funcionario,
        ids_chefia=ids_chefia,
        user_id=user_id,
        itens=[],
        pedido_selecionado=None,
        API_URL=API_URL
    )


# ================================
#  VER ITENS DO PEDIDO
# ================================
@dashboard_bp.get("/dashboard/<int:user_id>/pedido/<int:id_pedido>")
def ver_itens(user_id, id_pedido):

    logger.debug(f"\n===== ABRINDO PEDIDO {id_pedido} (user_id={user_id}) =====")

    # Pedidos
    logger.debug(f"[API] GET {API_URL}/pedidos")
    pedidos = requests.get(f"{API_URL}/pedidos").json()
    logger.info(f"[API RESPONSE] pedidos: {pedidos}")

    # Itens
    logger.debug(f"[API] GET {API_URL}/pedido/{id_pedido}")
    itens = requests.get(f"{API_URL}/pedido/{id_pedido}").json()
    logger.debug(f"[API RESPONSE] itens: {itens}")

    # Chefias
    logger.debug(f"[API] GET {API_URL}/pedido/{id_pedido}/chefes")
    chefias = requests.get(f"{API_URL}/pedido/{id_pedido}/chefes").json()
    logger.info(f"[API RESPONSE] chefias: {chefias}")

    # Força chefias a ser uma lista válida
    if not isinstance(chefias, list):
        logger.warning(f"Chefias NÃO É LISTA! Valor recebido: {chefias}")
        chefias = [{
    "id_pedido": 0,
    "id_chefia": 0,
    "nome_chefia": "0",
    "nivel_chefia": 0,
    "aprovado": 0
        }]

    ids_chefia = [c.get("id_confere") for c in chefias]
    logger.debug(f"[DEBUG] IDs de chefia extraídos: {ids_chefia}")

    # Funcionário
    logger.debug(f"[API] GET {API_URL}/dadosFuncionarios/{user_id}")
    func_api = requests.get(f"{API_URL}/dadosFuncionarios/{user_id}").json()
    logger.debug(f"[API RESPONSE] funcionario: {func_api}")

    funcionario = {
        "nome": func_api.get("nome_funcionario"),
        "cargo": func_api.get("cargo_funcionario"),
        "nivel": func_api.get("nivel_funcionario")
    }
    logger.debug(f"[DEBUG] Funcionário montado: {funcionario}")

    return render_template(
        "dashboard.html",
        pedidos=pedidos,
        funcionario=funcionario,
        ids_chefia=chefias,
        user_id=user_id,
        itens=itens,
        pedido_selecionado=id_pedido,
        API_URL=API_URL
    )
