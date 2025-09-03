# tests/test_loginView.py
from app.views.loginView import LoginView

def test_login_view_creation(root_window):
    view = LoginView(parent=root_window)
    assert view.controller is None
    assert view.winfo_exists() == 1

def test_get_credenciais(root_window):
    view = LoginView(parent=root_window)
    view.usuario_entry.insert(0, "test_user")
    view.senha_entry.insert(0, "test_pass")
    assert view.get_credenciais() == ("test_user", "test_pass")