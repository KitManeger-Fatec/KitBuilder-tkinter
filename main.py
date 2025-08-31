# main.py
import os
from screens.login import LoginScreen

if __name__ == "__main__":
    # Se o .env não existir, cria
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write("USER=admin\n")
            f.write("PASSWORD=admin\n")

    app = LoginScreen()
    app.mainloop()
