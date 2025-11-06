from flask import Blueprint, render_template, request
import requests
from flask import send_from_directory
import os

ASSETS_FOLDER = os.path.join(os.getcwd(), "assets", "images")




API_URL = "http://127.0.0.1:8000"

dashboard_bp = Blueprint("dashboard_bp", __name__, template_folder="templates")

#caminho seguro para os assets, como imagens
@dashboard_bp.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory(ASSETS_FOLDER, filename)

@dashboard_bp.route("/dashboard/<int:user_id>")
def dashboard(user_id):
    # Puxa pedidos
    pedidos = requests.get(f"{API_URL}/pedidos").json()

    # Puxa chefias do usuário
    chefias = requests.get(f"{API_URL}/chefes/{user_id}").json()

    # Lista IDs em que ele é chefia direta
    ids_chefia = [c["id_confere"] for c in chefias]

    # Informações do usuário (painel esquerdo)
    funcionario = None
    if len(chefias) > 0:
        funcionario = {
            "nome": chefias[0]["funcionario_nome"],
            "cargo": "Chefia direta",
            "nivel": "Nível 1"
        }

    return render_template(
        "dashboard.html",
        pedidos=pedidos,
        funcionario=funcionario,
        ids_chefia=ids_chefia,
        user_id=user_id,
        itens=[],
        pedido_selecionado=None
    )


@dashboard_bp.get("/dashboard/<int:user_id>/pedido/<int:id_pedido>")
def ver_itens(user_id, id_pedido):
    pedidos = requests.get(f"{API_URL}/pedidos").json()
    itens = requests.get(f"{API_URL}/pedido/{id_pedido}").json()
    chefias = requests.get(f"{API_URL}/chefes/{user_id}").json()
    ids_chefia = [c["id_confere"] for c in chefias]

    funcionario = None
    if len(chefias) > 0:
        funcionario = {
            "nome": chefias[0]["funcionario_nome"],
            "cargo": "Chefia direta",
            "nivel": "Nível 1"
        }

    return render_template(
        "dashboard.html",
        pedidos=pedidos,
        itens=itens,
        funcionario=funcionario,
        user_id=user_id,
        ids_chefia=ids_chefia,
        pedido_selecionado=id_pedido
    )
