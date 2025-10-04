import tkinter as tk

from tkinter import messagebox
import json
from resources.inventory import *


class ItemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Item Manager")
        self.items = []

        # Load existing items from JSON
        self.load_items()

        # Class Type Selection
        tk.Label(root, text="Item Type:").grid(row=0, column=0, padx=5, pady=5)
        self.item_type = tk.StringVar(value="Item")
        tk.OptionMenu(root, self.item_type, "Whistle", "Ball", "Yellow Card", "Red Card", "Speaker", "Microphone", "Maintenance", "Net").grid(row=0, column=1, padx=5, pady=5)

        # Name Input
        tk.Label(root, text="Name (optional):",).grid(row=1, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        # Quantity Input
        tk.Label(root, text="Quantity:").grid(row=2, column=0, padx=5, pady=5)
        self.quantity_entry = tk.Entry(root)
        self.quantity_entry.grid(row=2, column=1, padx=5, pady=5)

        # Sport Input (for Ball)
        tk.Label(root, text="Sport:").grid(row=3, column=0, padx=5, pady=5)
        self.sport_entry = tk.Entry(root)
        self.sport_entry.grid(row=3, column=1, padx=5, pady=5)

        # Add Button
        tk.Button(root, text="Add Item", command=self.add_item).grid(row=4, column=0, columnspan=2, pady=10)

        # Item Display
        self.item_listbox = tk.Listbox(root, width=50)
        self.item_listbox.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        self.display_items()

        # Add Button
        tk.Button(root, text="Add Item", command=self.add_item).grid(row=4, column=0, columnspan=2, pady=10)

        # Save and Close Button
        tk.Button(root, text="Save and Close", command=self.save_and_close).grid(row=6, column=0, columnspan=2, pady=10)

        # Save and Close Method
    def save_and_close(self):
        self.save_items()
        self.root.destroy()
    def add_item(self):
        item_type = self.item_type.get()
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()
        sport = self.sport_entry.get()

        try:
            quantity = int(quantity)
            if item_type == "Whistle":
                item = Whistle(quantity)
            elif item_type == "Ball":
                if not sport:
                    raise ValueError("Sport is required for Ball.")
                item = Ball(name, sport, quantity)
            elif item_type == "Net":
                item = Net(sport, quantity)
            elif item_type == "Microphone":
                item = Microphone(quantity)
            elif item_type == "Speaker":
                item = Speaker(quantity)
            elif item_type == "Yellow Card":
                item = Yellow(quantity)
            elif item_type == "Red Card":
                item = Red(quantity)
            else:
                raise ValueError("Invalid item type.")

            self.items.append(item)
            self.save_items()
            self.display_items()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def display_items(self):
        self.item_listbox.delete(0, tk.END)
        for item in self.items:
            self.item_listbox.insert(tk.END, repr(item))

    def save_items(self):
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        data["items"] = [item.__dict__ for item in self.items]

        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)

    def load_items(self):
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
                self.items = [Ball(**item) if "sport" in item else Item(**item) for item in data.get("items", [])]
        except FileNotFoundError:
            pass