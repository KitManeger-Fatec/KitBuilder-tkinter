import customtkinter as ctk
from app.database import SessionLocal
from app.models.funcionarios import Funcionario
import random

class TelaTesteLogin(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        self.lbl = ctk.CTkLabel(self, text="Usuário logado: (nenhum)")
        self.lbl.pack(pady=8)

        # Botão para fingir login
        ctk.CTkButton(self, text="Fingir login", command=self.finge_login).pack(pady=4)

    def finge_login(self):
        # Pega um funcionário aleatório do banco
        with SessionLocal() as session:
            funcionarios = session.query(Funcionario).all()
            if not funcionarios:
                self.lbl.configure(text="Nenhum funcionário no banco!")
                return
            func = random.choice(funcionarios)

            # Simula login apenas com o ID
            self.usuario_logado_id = func.idfuncionarios
            print(f"💡 ID do funcionário logado: {self.usuario_logado_id}")

            # Opcional: buscar dados completos usando o ID
            func_detalhes = session.query(Funcionario).filter_by(idfuncionarios=self.usuario_logado_id).first()
            self.lbl.configure(
                text=f"Usuário logado: {func_detalhes.nome_funcionario} | Nível: {func_detalhes.nivel_funcionario}"
            )


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("400x200")
    app = TelaTesteLogin(root)
    root.mainloop()
