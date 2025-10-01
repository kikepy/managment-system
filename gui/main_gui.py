import tkinter as tk
from tkinter import messagebox
import json
import os
from resources import *

class ScheduleManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple GUI")

        # Create a label
        label = tk.Label(root, text="Welcome to the GUI!")
        label.pack(pady=10)

        # Create a button
        button = tk.Button(root, text="Click Me", command=self.on_button_click)
        button.pack(pady=10)

    def on_button_click(self):
        # Example usage of Staff and Inventory class
        staff_member = Commentator(name="John Doe", languages="English",experience_years=5)
        inventory_item = Ball("soccer ball", "soccer")
        messagebox.showinfo("Info", f"Staff: {staff_member.name}, Item: {inventory_item.name}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScheduleManagementGUI(root)
    root.mainloop()