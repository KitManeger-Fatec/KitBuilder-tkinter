import customtkinter as ctk

class App:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Exemplo Scroll + Frame")
        self.root.geometry("900x600")  # defina um tamanho fixo ou use fullscreen

        # 1️⃣ Frame container principal
        container = ctk.CTkFrame(self.root)
        container.pack(fill="both", expand=True)

        # Use grid para dividir em 2 colunas: esquerda (scrollable) e direita (frame)
        container.grid_columnconfigure(0, weight=1)   # esquerda
        container.grid_columnconfigure(1, weight=2)   # direita
        container.grid_rowconfigure(0, weight=1)

        # 2️⃣ Painel Esquerdo: Scrollable Frame
        self.left_frame = ctk.CTkScrollableFrame(container, width=250)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Adiciona conteúdo de exemplo para gerar rolagem
        for i in range(50):
            ctk.CTkLabel(self.left_frame, text=f"Item {i+1}").pack(anchor="w", pady=2, padx=5)

        # 3️⃣ Painel Direito: Frame normal
        self.right_frame = ctk.CTkFrame(container)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Exemplo de widget no painel direito
        ctk.CTkLabel(self.right_frame, text="Conteúdo da direita").pack(pady=20)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()