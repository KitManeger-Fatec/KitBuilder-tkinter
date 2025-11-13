from flask import Blueprint, render_template, request, send_from_directory
import requests
import os


API_URL = "http://127.0.0.1:8000"
dashboard_bp = Blueprint("dashboard_bp", __name__, template_folder="templates")

# Caminho absoluto correto para a pasta de imagens
ASSETS_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "images")


# ✅ Servir arquivos da pasta assets/images/
@dashboard_bp.route("/assets/images/<path:filename>")
def serve_image(filename):
    return send_from_directory(ASSETS_FOLDER, filename)

@dashboard_bp.route("/dashboard/<int:user_id>")
def dashboard(user_id):
    pedidos = requests.get(f"{API_URL}/pedidos").json()
    chefias = requests.get(f"{API_URL}/chefes/{user_id}").json()
    ids_chefia = [c["id_confere"] for c in chefias]

    funcionario = requests.get(f"{API_URL}/dadosFuncionarios/{user_id}").json()
    funcionario = {
        "nome": funcionario["nome_funcionario"],
        "cargo": funcionario["cargo_funcionario"],
        "nivel": funcionario["nivel_funcionario"]
    }

    return render_template(
        "dashboard.html",
        pedidos=pedidos,
        funcionario=funcionario,
        ids_chefia=ids_chefia,
        user_id=user_id,
        itens=[],
        pedido_selecionado=None,
        API_URL=API_URL  # 👈 adiciona isso
    )

@dashboard_bp.get("/dashboard/<int:user_id>/pedido/<int:id_pedido>")
def ver_itens(user_id, id_pedido):
    pedidos = requests.get(f"{API_URL}/pedidos").json()
    itens = requests.get(f"{API_URL}/pedido/{id_pedido}").json()
    chefias = requests.get(f"{API_URL}/chefes/{user_id}").json()
    ids_chefia = [c["id_confere"] for c in chefias]

    funcionario = requests.get(f"{API_URL}/dadosFuncionarios/{user_id}").json()
    funcionario = {
        "nome": funcionario["nome_funcionario"],
        "cargo": funcionario["cargo_funcionario"],
        "nivel": funcionario["nivel_funcionario"]
    }

    return render_template(
        "dashboard.html",
        pedidos=pedidos,
        funcionario=funcionario,
        ids_chefia=ids_chefia,
        user_id=user_id,
        itens=itens,
        pedido_selecionado=None,
        API_URL=API_URL  # 👈 adiciona isso
    )
