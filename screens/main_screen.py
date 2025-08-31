# screens/main_screen.py
import customtkinter as ctk
from config.colors import COLORS
from config.fonts import FONTS
from config.settings import VAR_GLOBAL, APP_TITLE


class MainScreen(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(APP_TITLE)
        self.attributes("-fullscreen", True)  # FULLSCREEN garantido
        self.configure(fg_color=COLORS["bg"])

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(self, text="Tela Principal", font=FONTS["title"], text_color=COLORS["fg"]).grid(row=0, column=0)

        ctk.CTkLabel(self, text=f"Variável Global: {VAR_GLOBAL}", font=FONTS["subtitle"], text_color=COLORS["fg"]).grid(row=1, column=0)

        ctk.CTkButton(self, text="Sair", command=self.destroy,
                      fg_color=COLORS["button"], text_color=COLORS["button_text"],
                      font=FONTS["button"]).grid(row=2, column=0, pady=20)

        self.mainloop()
