# tests/conftest.py
import sys
import os
from pathlib import Path
import pytest
import customtkinter as ctk
from dotenv import load_dotenv

# Adiciona o diretório raiz ao Python path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

load_dotenv()

@pytest.fixture(autouse=True)
def setup_env():
    os.environ["USERNAME"] = "test_user"
    os.environ["PASSWORD"] = "test_pass"
    os.environ["FULLSCREEN"] = "False"

@pytest.fixture
def root_window():
    root = ctk.CTk()
    root.title("Test App")
    yield root
    root.destroy()
