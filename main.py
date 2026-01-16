import tkinter as tk
from gui.main_gui import MainGUI
from config import data_file_path, events_file_path

if __name__ == "__main__":
    root = tk.Tk()
    app = MainGUI(root, data_file_path, events_file_path)
    root.mainloop()