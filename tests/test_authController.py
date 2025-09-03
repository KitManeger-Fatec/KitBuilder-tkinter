# tests/test_authController.py
from unittest.mock import Mock
from app.controllers.authController import AuthController


def test_fazer_login_sucesso(root_window, mocker):
    mock_router = Mock()
    controller = AuthController(root=root_window, router=mock_router)
    mock_view = Mock()
    mock_view.get_credenciais.return_value = ("test_user", "test_pass")
    controller.view = mock_view

    result = controller.fazer_login()
    assert result is True
    mock_router.show_main.assert_called_once()


def test_fazer_login_falha(root_window, mocker):
    mock_router = Mock()
    controller = AuthController(root=root_window, router=mock_router)
    mock_view = Mock()
    mock_view.get_credenciais.return_value = ("wrong", "credentials")
    controller.view = mock_view

    result = controller.fazer_login()
    assert result is False
    mock_view.mostrar_erro.assert_called_with("Usuário ou senha incorretos")
