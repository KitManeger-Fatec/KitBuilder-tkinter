from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import os
from web_app.dashboard import dashboard_bp



web = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)
web.secret_key = "chave-secreta"
web.register_blueprint(dashboard_bp)

API_URL = "http://127.0.0.1:8000"

@web.context_processor
def inject_env():
    return dict(getenv=os.getenv)

@web.get("/")
def login_page():
    return render_template("login.html")


@web.post("/login")
def login_action():
    usuario = request.form.get("usuario")
    senha = request.form.get("senha")

    payload = {"username": usuario, "password": senha}

    try:
        resp = requests.post(f"{API_URL}/auth/login", json=payload)
    except Exception as e:
        flash("Erro ao conectar com API FastAPI")
        return redirect(url_for("login_page"))

    if resp.status_code != 200:
        flash("Usuário ou senha inválidos!")
        return redirect(url_for("login_page"))

    user = resp.json()
    return redirect(url_for("dashboard", user_id=user["id"]))


@web.get("/dashboard/<int:user_id>")
def dashboard(user_id):
    return render_template("dashboard.html", id=user_id)
