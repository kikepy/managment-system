import tkinter as tk
from tkinter import messagebox
import json
from resources.staff import *

class StaffGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Staff Manager")
        self.staff = []

        # Load existing staff from JSON
        self.load_staff()

        # Staff Type Selection
        tk.Label(root, text="Staff Type:").grid(row=0, column=0, padx=5, pady=5)
        self.staff_type = tk.StringVar(value="Commentator")
        tk.OptionMenu(root, self.staff_type, "Commentator", "Seller").grid(row=0, column=1, padx=5, pady=5)

        # Name Input
        tk.Label(root, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        # Experience Input
        tk.Label(root, text="Experience (years):").grid(row=2, column=0, padx=5, pady=5)
        self.experience_entry = tk.Entry(root)
        self.experience_entry.grid(row=2, column=1, padx=5, pady=5)

        # Languages Input (for Commentator)
        tk.Label(root, text="Languages (comma-separated):").grid(row=3, column=0, padx=5, pady=5)
        self.languages_entry = tk.Entry(root)
        self.languages_entry.grid(row=3, column=1, padx=5, pady=5)

        # Products Input (for Seller)
        tk.Label(root, text="Products (comma-separated):").grid(row=4, column=0, padx=5, pady=5)
        self.products_entry = tk.Entry(root)
        self.products_entry.grid(row=4, column=1, padx=5, pady=5)

        # Add Button
        tk.Button(root, text="Add Staff", command=self.add_staff).grid(row=5, column=0, columnspan=2, pady=10)

        # Staff Display
        self.staff_listbox = tk.Listbox(root, width=50)
        self.staff_listbox.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        self.display_staff()

        tk.Button(root, text="Add Staff", command=self.add_staff).grid(row=5, column=0, columnspan=2, pady=10)

        # Save and Close Button
        tk.Button(root, text="Save and Close", command=self.save_and_close).grid(row=7, column=0, columnspan=2, pady=10)

        # Save and Close Method
    def save_and_close(self):
        self.save_staff()
        self.root.destroy()

    def add_staff(self):
        staff_type = self.staff_type.get()
        name = self.name_entry.get()
        experience = self.experience_entry.get()
        languages = self.languages_entry.get()
        products = self.products_entry.get()

        try:
            experience = int(experience)
            if staff_type == "Commentator":
                language_list = [lang.strip() for lang in languages.split(",")]
                staff = Commentator(name, language_list, experience)
            elif staff_type == "Seller":
                product_list = [product.strip() for product in products.split(",")]
                staff = Seller(name, experience, product_list)
            else:
                raise ValueError("Invalid staff type.")

            self.staff.append(staff)
            self.save_staff()
            self.display_staff()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def display_staff(self):
        self.staff_listbox.delete(0, tk.END)
        for staff in self.staff:
            self.staff_listbox.insert(tk.END, repr(staff))

    def save_staff(self):
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        data["staff"] = [staff.__dict__ for staff in self.staff]

        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)

    def load_staff(self):
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
                self.staff = [
                    Commentator(**staff) if "languages" in staff else Seller(**staff)
                    for staff in data.get("staff", [])
                ]
        except FileNotFoundError:
            pass

