# tests/test_mainView
import pytest
from unittest.mock import Mock
from views.mainView import MainView

def test_main_view_creation(root_window):
    view = MainView(parent=root_window)
    assert view.winfo_exists() == 1
    assert hasattr(view, 'kits')

def test_open_kit(root_window):
    view = MainView(parent=root_window)
    test_kit = {"id": 1, "name": "Test Kit", "price": 10.0, "items": 5}
    view.open_kit(test_kit)
    assert view.kit_name.get() == "Test Kit"
    assert float(view.kit_price.get()) == 10.0