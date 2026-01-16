import random
import tkinter as tk
from tkinter import ttk, messagebox
import json
from resources.staff import *


class StaffGUI:
    def __init__(self, root, data_file_path):
        self.root = root
        self.data_file_path = data_file_path
        self.root.title("Staff Manager")
        self.root.geometry("800x600")

        self.staff = self.load_staff()
        self.input_fields = {}

        self.create_widgets()
        self.display_staff()

    def create_widgets(self):
        # Staff Role Selection
        tk.Label(self.root, text="Staff Role:").grid(row=0, column=0, padx=5, pady=5)
        self.staff_role = tk.StringVar(value="Referee")
        staff_role_menu = tk.OptionMenu(
            self.root, self.staff_role, "Referee", "Trainer", "Commentator", "Doctor", "Maintenance", "Seller",
            command=self.update_form_fields
        )
        staff_role_menu.grid(row=0, column=1, padx=5, pady=5)

        # Quantity Input
        tk.Label(self.root, text="Quantity:").grid(row=1, column=0, padx=5, pady=5)
        self.quantity_var = tk.StringVar(value="1")
        self.quantity_entry = tk.Entry(self.root, textvariable=self.quantity_var, validate="key")
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5)
        self.quantity_entry.config(validatecommand=(self.root.register(self.validate_quantity), "%P"))

        # Dynamic form area
        self.form_frame = tk.Frame(self.root)
        self.form_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Add Staff Button
        tk.Button(self.root, text="Add Staff", command=self.add_staff).grid(row=3, column=0, columnspan=2, pady=10)

        # Staff Display
        self.staff_listbox = tk.Listbox(self.root, width=50, height=10)
        self.staff_listbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Save and Close Button
        tk.Button(self.root, text="Save and Close", command=self.save_and_close).grid(row=5, column=0, columnspan=2, pady=10)

        self.update_form_fields("Referee")

    def validate_quantity(self, value_if_allowed):
        return value_if_allowed.isdigit() or value_if_allowed == ""

    def update_form_fields(self, role):
        for widget in self.form_frame.winfo_children():
            widget.destroy()

        self.input_fields = {}
        current_row = 0

        if role == "Referee":
            self.add_field("Sport", "Futsal", current_row)
            current_row += 1
            self.add_field("Certification Level", "Low", current_row, ["Low", "Mid", "High"])
        elif role == "Trainer":
            self.add_field("Sport", "Futsal", current_row)
        elif role == "Commentator":
            self.add_field("Languages", "English,Spanish", current_row)
            current_row += 1
            self.add_field("Experience (Years)", "5", current_row)
        elif role == "Doctor":
            self.add_field("Specialization", "Sports Medicine", current_row)
            current_row += 1
            self.add_field("Certification", "Medical License", current_row)
        elif role == "Maintenance":
            self.add_field("Skills", "Electrical,Plumbing", current_row)
            current_row += 1
            self.add_field("Shift", "Morning", current_row, ["Morning", "Afternoon", "Night"])
            current_row += 1
            self.add_field("Tools", "Screwdriver,Wrench", current_row)
        elif role == "Seller":
            self.add_field("Sales Experience (Years)", "3", current_row)
            current_row += 1
            self.add_field("Products", "Tickets,Merchandise", current_row)

        self.input_fields["Availability"] = tk.BooleanVar(value=True)
        tk.Checkbutton(self.form_frame, text="Available", variable=self.input_fields["Availability"]).grid(
            row=current_row + 1, column=0, columnspan=2, pady=5
        )

    def add_field(self, label, default, row, options=None):
        tk.Label(self.form_frame, text=f"{label}:").grid(row=row, column=0, padx=5, pady=5)
        if options:
            var = tk.StringVar(value=default)
            self.input_fields[label] = var
            ttk.Combobox(self.form_frame, textvariable=var, values=options, state="readonly").grid(row=row, column=1, padx=5, pady=5)
        else:
            var = tk.StringVar(value=default)
            self.input_fields[label] = var
            tk.Entry(self.form_frame, textvariable=var).grid(row=row, column=1, padx=5, pady=5)

    def add_staff(self):
        try:
            role = self.staff_role.get()
            quantity = int(self.quantity_var.get())
            staff_data = {key: var.get() for key, var in self.input_fields.items() if key != "Availability"}
            staff_data["Availability"] = self.input_fields["Availability"].get()

            for _ in range(quantity):
                self.staff.append({"role": role, **staff_data})

            self.save_staff()
            self.display_staff()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please check the fields.")

    def display_staff(self):
        self.staff_listbox.delete(0, tk.END)
        for member in self.staff:
            self.staff_listbox.insert(tk.END, f"{member['role']} - {member}")

    def save_staff(self):
        try:
            with open(self.data_file_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        data["staff"] = self.staff

        with open(self.data_file_path, "w") as file:
            json.dump(data, file, indent=4)

    def load_staff(self):
        try:
            with open(self.data_file_path, "r") as file:
                data = json.load(file)
            return data.get("staff", [])
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error decoding data.json.")
            return []

    def save_and_close(self):
        self.save_staff()
        self.root.destroy()