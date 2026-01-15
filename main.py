import tkinter as tk
import sys
import os

# Add the root directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import MainGUI from gui.main_gui
from gui.main_gui import MainGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = MainGUI(root)
    root.mainloop()