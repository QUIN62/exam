# Main.py
import tkinter as tk
from classGet import classGet
from classShow import classShow

if __name__ == "__main__":
    base_url = "https://671be41c2c842d92c381a500.mockapi.io"  # URL base actualizada
    db = classGet(base_url)

    root = tk.Tk()
    app = classShow(root, db)
    root.mainloop()
