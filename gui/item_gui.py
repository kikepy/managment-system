import tkinter as tk
from tkinter import ttk, messagebox
import json


class ItemGUI:
    def __init__(self, root, data_file_path):
        self.root = root
        self.data_file_path = data_file_path
        self.root.title("Items Manager")
        self.root.geometry("800x600")

        self.items = self.load_items()

        self.create_widgets()
        self.display_items()

    def create_widgets(self):
        # Item Type Selection
        tk.Label(self.root, text="Item Type:").grid(row=0, column=0, padx=5, pady=5)
        self.item_type = tk.StringVar(value="Whistle")
        item_type_menu = tk.OptionMenu(
            self.root, self.item_type, "Whistle", "Ball", "Yellow Card", "Red Card", "Speaker", "Microphone", "Net",
            command=self.toggle_sport_field
        )
        item_type_menu.grid(row=0, column=1, padx=5, pady=5)

        # Quantity Selection
        tk.Label(self.root, text="Quantity:").grid(row=1, column=0, padx=5, pady=5)
        self.quantity_var = tk.StringVar(value="1")
        self.quantity_entry = tk.Entry(self.root, textvariable=self.quantity_var, validate="key")
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5)
        self.quantity_entry.config(validatecommand=(self.root.register(self.validate_quantity), "%P"))

        # Sport Selection (for Ball)
        self.sport_label = tk.Label(self.root, text="Sport:")
        self.sport_var = tk.StringVar(value="Football")
        self.sport_combobox = ttk.Combobox(
            self.root, textvariable=self.sport_var, values=["Football", "Basketball", "Volleyball"], state="readonly"
        )

        # Add Button
        tk.Button(self.root, text="Add Item", command=self.add_item).grid(row=3, column=0, columnspan=2, pady=10)

        # Item Display
        self.item_listbox = tk.Listbox(self.root, width=50)
        self.item_listbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Save and Close Button
        tk.Button(self.root, text="Save and Close", command=self.save_and_close).grid(row=5, column=0, columnspan=2, pady=10)

        # Initialize sport field visibility
        self.toggle_sport_field("Whistle")

    def toggle_sport_field(self, selected_item_type):
        if selected_item_type == "Ball":
            self.sport_label.grid(row=2, column=0, padx=5, pady=5)
            self.sport_combobox.grid(row=2, column=1, padx=5, pady=5)
        else:
            self.sport_label.grid_remove()
            self.sport_combobox.grid_remove()

    def validate_quantity(self, value_if_allowed):
        return value_if_allowed.isdigit() or value_if_allowed == ""

    def add_item(self):
        try:
            item_type = self.item_type.get()
            quantity = int(self.quantity_var.get())
            sport = self.sport_var.get() if item_type == "Ball" else None

            # Check if the item already exists
            for item in self.items:
                if item["type"] == item_type and (item_type != "Ball" or item["sport"] == sport):
                    item["total_quantity"] += quantity
                    break
            else:
                new_item = {"type": item_type, "total_quantity": quantity}
                if sport:
                    new_item["sport"] = sport
                self.items.append(new_item)

            self.save_items()
            self.display_items()
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity. Please enter a valid number.")

    def display_items(self):
        self.item_listbox.delete(0, tk.END)
        for item in self.items:
            self.item_listbox.insert(tk.END, f"{item['type']} - {item.get('sport', 'N/A')} - {item['total_quantity']}")

    def save_items(self):
        try:
            with open(self.data_file_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        data["items"] = self.items

        with open(self.data_file_path, "w") as file:
            json.dump(data, file, indent=4)

    def load_items(self):
        try:
            with open(self.data_file_path, "r") as file:
                data = json.load(file)
            return data.get("items", [])
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error decoding data.json.")
            return []

    def save_and_close(self):
        self.save_items()
        self.root.destroy()