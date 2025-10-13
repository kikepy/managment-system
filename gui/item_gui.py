import tkinter as tk
from tkinter import ttk, messagebox
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
        self.item_type = tk.StringVar(value="Whistle")
        item_type_menu = tk.OptionMenu(root, self.item_type, "Whistle", "Ball", "Yellow Card", "Red Card", "Speaker",
                                       "Microphone", "Net", command=self.toggle_sport_field)
        item_type_menu.grid(row=0, column=1, padx=5, pady=5)

        # Quantity Selection
        tk.Label(root, text="Quantity:").grid(row=2, column=0, padx=5, pady=5)
        self.quantity_var = tk.StringVar(value="1")
        self.quantity_entry = tk.Entry(root, textvariable=self.quantity_var)
        self.quantity_entry.grid(row=2, column=1, padx=5, pady=5)

        #Validattion for Quantity
        def validate_quantity(value_if_allowed):
            if value_if_allowed.isdigit() or value_if_allowed == "":
                return True
            return False

        vcmd = (root.register(validate_quantity), "%P")
        self.quantity_entry.config(validate="key", validatecommand=vcmd)

        # Sport Selection (for Ball)
        self.sport_label = tk.Label(root, text="Sport:")
        self.sport_var = tk.StringVar(value="Football")
        self.sport_combobox = ttk.Combobox(root, textvariable=self.sport_var,
                                           values=["Football", "Basketball", "Volleyball"], state="readonly")

        # Add Button
        tk.Button(root, text="Add Item", command=self.add_item).grid(row=4, column=0, columnspan=2, pady=10)

        # Item Display
        self.item_listbox = tk.Listbox(root, width=50)
        self.item_listbox.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        self.display_items()

        # Save and Close Button
        tk.Button(root, text="Save and Close", command=self.save_and_close).grid(row=6, column=0, columnspan=2, pady=10)

        # Initialize sport field visibility
        self.toggle_sport_field("Whistle")

    def toggle_sport_field(self, selected_item_type):
        if selected_item_type == "Ball":
            self.sport_label.grid(row=3, column=0, padx=5, pady=5)
            self.sport_combobox.grid(row=3, column=1, padx=5, pady=5)
        else:
            self.sport_label.grid_remove()
            self.sport_combobox.grid_remove()

    def save_and_close(self):
        self.save_items()
        self.root.destroy()

    def add_item(self):
        item_type = self.item_type.get()
        quantity = int(self.quantity_var.get())
        sport = self.sport_var.get()

        try:

            # Check if the item already exists in the inventory
            for item in self.items:
                if isinstance(item, Ball) and item_type == "Ball" and item.sport == sport:
                    item.add(quantity)
                    break
                elif isinstance(item, Whistle) and item_type == "Whistle":
                    item.add(quantity)
                    break
                elif isinstance(item, Net) and item_type == "Net":
                    item.add(quantity)
                    break
                elif isinstance(item, Microphone) and item_type == "Microphone":
                    item.add(quantity)
                    break
                elif isinstance(item, Speaker) and item_type == "Speaker":
                    item.add(quantity)
                    break
                elif isinstance(item, Yellow) and item_type == "Yellow Card":
                    item.add(quantity)
                    break
                elif isinstance(item, Red) and item_type == "Red Card":
                    item.add(quantity)
                    break
            else:
                # If no matching item is found, create a new one
                if item_type == "Whistle":
                    self.items.append(Whistle(quantity))
                elif item_type == "Ball":
                    self.items.append(Ball(sport, quantity))
                elif item_type == "Net":
                    self.items.append(Net(quantity))
                elif item_type == "Microphone":
                    self.items.append(Microphone(quantity))
                elif item_type == "Speaker":
                    self.items.append(Speaker(quantity))
                elif item_type == "Yellow Card":
                    self.items.append(Yellow(quantity))
                elif item_type == "Red Card":
                    self.items.append(Red(quantity))
                else:
                    raise ValueError("Invalid item type.")

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

        data["items"] = []
        for item in self.items:
            if isinstance(item, Ball):
                data["items"].append({
                    "type": "Ball",
                    "sport": item.sport,
                    "total_quantity": item.total_quantity,
                })
            else:
                data["items"].append({
                    "type": item.__class__.__name__,
                    "name": item.name,
                    "total_quantity": item.total_quantity,
                })

        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)


    def load_items(self):
        try:
            with open("data.json", "r") as file:
                data = json.load(file)

            self.items = []
            for item_data in data.get("items", []):
                item_type = item_data.pop("type", None)
                if item_type == "Ball":
                    self.items.append(
                        Ball(sport=item_data.get("sport", ""), total_quantity=item_data.get("total_quantity", 0))
                    )
                elif item_type == "Whistle":
                    self.items.append(Whistle(total_quantity=item_data.get("total_quantity", 0)))
                elif item_type == "Yellow Card":
                    self.items.append(Yellow(total_quantity=item_data.get("total_quantity", 0)))
                elif item_type == "Red Card":
                    self.items.append(Red(total_quantity=item_data.get("total_quantity", 0)))
                elif item_type == "Speaker":
                    self.items.append(Speaker(total_quantity=item_data.get("total_quantity", 0)))
                elif item_type == "Microphone":
                    self.items.append(Microphone(total_quantity=item_data.get("total_quantity", 0)))
                elif item_type == "Net":
                    self.items.append(Net(total_quantity=item_data.get("total_quantity", 0)))
                else:
                    self.items.append(
                        Item(name=item_data.get("name", "Unknown"), total_quantity=item_data.get("total_quantity", 0)))
        except FileNotFoundError:
            print("data.json not found. Starting with an empty list.")
            self.items = []
        except Exception as e:
            print("Error loading items:", e)
            messagebox.showerror("Error", f"Error loading items: {e}")