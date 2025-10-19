import random
import tkinter as tk
from tkinter import ttk, messagebox
import json
import time
from resources.staff import *


class StaffGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Staff Manager")
        self.staff = []
        self.input_fields = {}
        self.current_row = 2

        self.staff_names = {
            "Referee": ["John", "Michael", "Sarah", "Emily", "Daniel", "Jessica", "Mark", "Emma"],
            "Trainer": ["Chris", "Anna", "James", "Sophia", "Luis", "Elier", "Marta", "Henry"],
            "Commentator": ["David", "Laura", "Robert", "Olivia", "Mario Kempes", "DjMario", "Messi"],
            "Doctor": ["Dr. Smith", "Dr. Brown", "Dr. Taylor", "Dr. Wilson", "Dr. Garcia", "Dr. Martinez", "Dr. Lee", "Dr. Hernandez"],
            "Maintenance": ["Tom", "Jerry", "Sam", "Alex", "Oscar", "Jian", "Ernesto", "Miguel"],
            "Seller": ["Alice", "Bob", "Charlie", "Diana", "Yasmani", "Yusimi", "Yamila", "Kevin"]
        }

        # Load existing staff from JSON
        self.load_staff()

        # Staff Role Selection
        tk.Label(root, text="Staff Role:").grid(row=0, column=0, padx=5, pady=5)
        self.staff_role = tk.StringVar(value="Referee")
        staff_role_menu = tk.OptionMenu(root, self.staff_role,
                                        "Referee", "Trainer", "Commentator", "Doctor", "Maintenance", "Seller",
                                        command=self.update_form_fields)
        staff_role_menu.grid(row=0, column=1, padx=5, pady=5)

        # Quantity Input
        tk.Label(root, text="Quantity:").grid(row=1, column=0, padx=5, pady=5)
        self.quantity_var = tk.StringVar(value="1")
        self.quantity_entry = tk.Entry(root, textvariable=self.quantity_var)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        # Validation for Quantity
        def validate_quantity(value_if_allowed):
            if value_if_allowed.isdigit() or value_if_allowed == "":
                return True
            return False

        vcmd = (root.register(validate_quantity), "%P")
        self.quantity_entry.config(validate="key", validatecommand=vcmd)

        # Dynamic form area - will be populated based on role
        self.form_frame = tk.Frame(root)
        self.form_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Add Staff Button
        self.add_button = tk.Button(root, text="Add Staff", command=self.add_staff)
        self.add_button.grid(row=100, column=0, columnspan=2, pady=10)

        # Initialize dynamic form fields
        self.update_form_fields("Referee")

        # Staff Display
        self.staff_listbox = tk.Listbox(root, width=50, height=10)
        self.staff_listbox.grid(row=101, column=0, columnspan=2, padx=5, pady=5)
        self.display_staff()

        # Save and Close Button
        tk.Button(root, text="Save and Close", command=self.save_and_close).grid(row=102, column=0, columnspan=2, pady=10)

    def update_form_fields(self, role):
        # Clear previous fields
        for widget in self.form_frame.winfo_children():
            widget.destroy()

        self.input_fields = {}
        current_row = 0

        # Create fields based on selected role
        if role == "Referee":
            # Sport field
            tk.Label(self.form_frame, text="Sport:").grid(row=current_row, column=0, padx=5, pady=5)
            self.input_fields["sport"] = tk.StringVar(value="Futsal")
            sport_menu = ttk.Combobox(self.form_frame, textvariable=self.input_fields["sport"],
                                      values=["Futsal", "Basketball", "Volleyball"], state="readonly")
            sport_menu.grid(row=current_row, column=1, padx=5, pady=5)
            current_row += 1

            # Certification level field
            tk.Label(self.form_frame, text="Certification:").grid(row=current_row, column=0, padx=5, pady=5)
            self.input_fields["certification_level"] = tk.StringVar(value="Low")
            cert_menu = ttk.Combobox(self.form_frame, textvariable=self.input_fields["certification_level"],
                                     values=["Low", "Mid", "High"], state="readonly")
            cert_menu.grid(row=current_row, column=1, padx=5, pady=5)
            current_row += 1

        elif role == "Trainer":
            # Sport field for Trainer
            tk.Label(self.form_frame, text="Sport:").grid(row=current_row, column=0, padx=5, pady=5)
            self.input_fields["sport"] = tk.StringVar(value="Futsal")
            sport_menu = ttk.Combobox(self.form_frame, textvariable=self.input_fields["sport"],
                                      values=["Futsal", "Basketball", "Volleyball"], state="readonly")
            sport_menu.grid(row=current_row, column=1, padx=5, pady=5)
            current_row += 1

        elif role == "Commentator":
            # Languages
            tk.Label(self.form_frame, text="Languages (comma-separated):").grid(row=current_row, column=0, padx=5, pady=5)
            self.input_fields["languages"] = tk.StringVar(value="English,Spanish")
            lang_entry = tk.Entry(self.form_frame, textvariable=self.input_fields["languages"])
            lang_entry.grid(row=current_row, column=1, padx=5, pady=5)
            current_row += 1

            # Experience years
            tk.Label(self.form_frame, text="Experience (years):").grid(row=current_row, column=0, padx=5, pady=5)
            self.input_fields["experience_years"] = tk.StringVar(value="5")
            exp_entry = tk.Entry(self.form_frame, textvariable=self.input_fields["experience_years"])
            exp_entry.grid(row=current_row, column=1, padx=5, pady=5)
            current_row += 1

        elif role == "Doctor":
            # Specialization
            tk.Label(self.form_frame, text="Specialization:").grid(row=current_row, column=0, padx=5, pady=5)
            self.input_fields["specialization"] = tk.StringVar(value="Sports Medicine")
            spec_entry = tk.Entry(self.form_frame, textvariable=self.input_fields["specialization"])
            spec_entry.grid(row=current_row, column=1, padx=5, pady=5)
            current_row += 1

            # Certification
            tk.Label(self.form_frame, text="Certification:").grid(row=current_row, column=0, padx=5, pady=5)
            self.input_fields["certification"] = tk.StringVar(value="Medical License")
            cert_entry = tk.Entry(self.form_frame, textvariable=self.input_fields["certification"])
            cert_entry.grid(row=current_row, column=1, padx=5, pady=5)
            current_row += 1

        elif role == "Maintenance":
            # Skills
            tk.Label(self.form_frame, text="Skills (comma-separated):").grid(row=current_row, column=0, padx=5, pady=5)
            self.input_fields["skills"] = tk.StringVar(value="Electrical,Plumbing")
            skills_entry = tk.Entry(self.form_frame, textvariable=self.input_fields["skills"])
            skills_entry.grid(row=current_row, column=1, padx=5, pady=5)
            current_row += 1

            # Shift
            tk.Label(self.form_frame, text="Shift:").grid(row=current_row, column=0, padx=5, pady=5)
            self.input_fields["shift"] = tk.StringVar(value="Morning")
            shift_menu = ttk.Combobox(self.form_frame, textvariable=self.input_fields["shift"],
                                      values=["Morning", "Afternoon", "Night"], state="readonly")
            shift_menu.grid(row=current_row, column=1, padx=5, pady=5)
            current_row += 1

            # Tools
            tk.Label(self.form_frame, text="Tools (comma-separated):").grid(row=current_row, column=0, padx=5, pady=5)
            self.input_fields["tools"] = tk.StringVar(value="screwdriver,wrench")
            tools_entry = tk.Entry(self.form_frame, textvariable=self.input_fields["tools"])
            tools_entry.grid(row=current_row, column=1, padx=5, pady=5)
            current_row += 1

        elif role == "Seller":
            # Sales experience
            tk.Label(self.form_frame, text="Sales Experience (years):").grid(row=current_row, column=0, padx=5, pady=5)
            self.input_fields["sales_experience"] = tk.StringVar(value="3")
            exp_entry = tk.Entry(self.form_frame, textvariable=self.input_fields["sales_experience"])
            exp_entry.grid(row=current_row, column=1, padx=5, pady=5)
            current_row += 1

            # Products
            tk.Label(self.form_frame, text="Products (comma-separated):").grid(row=current_row, column=0, padx=5, pady=5)
            self.input_fields["products"] = tk.StringVar(value="Tickets,Merchandise")
            products_entry = tk.Entry(self.form_frame, textvariable=self.input_fields["products"])
            products_entry.grid(row=current_row, column=1, padx=5, pady=5)
            current_row += 1

        # Availability checkbox (common for all)
        self.input_fields["availability"] = tk.BooleanVar(value=True)
        tk.Checkbutton(self.form_frame, text="Available", variable=self.input_fields["availability"]).grid(
            row=current_row, column=0, columnspan=2, pady=5)

    def add_staff(self):
        role = self.staff_role.get()
        availability = self.input_fields.get("availability", tk.BooleanVar(value=True)).get()

        # Get and validate quantity
        quantity = self.quantity_var.get().strip()
        if not quantity or not quantity.isdigit() or int(quantity) < 1:
            messagebox.showerror("Error", "Quantity must be a positive number.")
            return

        quantity = int(quantity)

        try:
            for i in range(quantity):
                # Generate a default name based on role and timestamp
                name = random.choice(self.staff_names.get(role, ["StaffMember"]))

                # Create an instance of the specific staff class based on the role
                if role == "Referee":
                    new_staff = Referee(
                        name=name,
                        sport=self.input_fields["sport"].get(),
                        certification_level=self.input_fields["certification_level"].get(),
                        availability=availability
                    )
                elif role == "Trainer":
                    new_staff = Trainer(
                        name=name,
                        sport=self.input_fields["sport"].get(),
                        availability=availability
                    )
                elif role == "Commentator":
                    languages = [lang.strip() for lang in self.input_fields["languages"].get().split(",")]
                    experience_years = int(self.input_fields["experience_years"].get())
                    new_staff = Commentator(
                        name=name,
                        languages=languages,
                        experience_years=experience_years,
                        aviability=availability  # Note: typo in original class
                    )
                elif role == "Doctor":
                    new_staff = Doctor(
                        name=name,
                        specialization=self.input_fields["specialization"].get(),
                        certification=self.input_fields["certification"].get(),
                        availability=availability
                    )
                elif role == "Maintenance":
                    skills = self.input_fields["skills"].get()
                    shift = self.input_fields["shift"].get()
                    tools = [tool.strip() for tool in self.input_fields["tools"].get().split(",")]
                    new_staff = Maintenance(
                        name=name,
                        skills=skills,
                        shift=shift,
                        availability=availability,
                        tools=tools
                    )
                elif role == "Seller":
                    sales_experience = int(self.input_fields["sales_experience"].get())
                    products = [p.strip() for p in self.input_fields["products"].get().split(",")]
                    new_staff = Seller(
                        name=name,
                        sales_experience=sales_experience,
                        products=products,
                        availability=availability
                    )
                else:
                    messagebox.showerror("Error", "Invalid role selected.")
                    return

                self.staff.append(new_staff)

            self.save_staff()
            self.display_staff()
            self.quantity_var.set("1")  # Reset quantity to 1

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def display_staff(self):
        self.staff_listbox.delete(0, tk.END)
        for member in self.staff:
            self.staff_listbox.insert(tk.END, repr(member))

    def save_staff(self):
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        # Convert staff objects to dictionaries for JSON serialization
        staff_data = []
        for member in self.staff:
            class_name = member.__class__.__name__
            member_dict = {"role": class_name}

            # Add specific attributes based on class type
            if class_name == "Referee":
                member_dict.update({
                    "name": member.name,
                    "sport": member.sport,
                    "certification_level": member.certification_level,
                    "availability": member.availability
                })
            elif class_name == "Trainer":
                member_dict.update({
                    "name": member.name,
                    "sport": member.sport,
                    "availability": member.availability
                })
            elif class_name == "Commentator":
                member_dict.update({
                    "name": member.name,
                    "languages": member.languages,
                    "experience_years": member.experience_years,
                    "availability": member.availability
                })
            elif class_name == "Doctor":
                member_dict.update({
                    "name": member.name,
                    "specialization": member.specialization,
                    "certification": member.certification,
                    "availability": member.availability
                })
            elif class_name == "Maintenance":
                member_dict.update({
                    "name": member.name,
                    "skills": member.skills,
                    "shift": member.shift,
                    "availability": member.availability,
                    "tools": list(member.required_items.keys())
                })
            elif class_name == "Seller":
                member_dict.update({
                    "name": member.name,
                    "sales_experience": member.sales_experience,
                    "products": member.products,
                    "availability": member.availability
                })

            staff_data.append(member_dict)

        data["staff"] = staff_data

        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)

    def load_staff(self):
        try:
            with open("data.json", "r") as file:
                data = json.load(file)

            self.staff = []
            for member_data in data.get("staff", []):
                role = member_data.pop("role", None)
                name = member_data.pop("name", f"Unknown_{int(time.time())}")
                availability = member_data.pop("availability", True)

                if role == "Referee":
                    self.staff.append(Referee(
                        name=name,
                        sport=member_data.get("sport", "futsal"),
                        certification_level=member_data.get("certification_level", "low"),
                        availability=availability
                    ))
                elif role == "Trainer":
                    self.staff.append(Trainer(
                        name=name,
                        sport=member_data.get("sport", "futsal"),
                        availability=availability
                    ))
                elif role == "Commentator":
                    self.staff.append(Commentator(
                        name=name,
                        languages=member_data.get("languages", ["English"]),
                        experience_years=member_data.get("experience_years", 1),
                        aviability=availability
                    ))
                elif role == "Doctor":
                    self.staff.append(Doctor(
                        name=name,
                        specialization=member_data.get("specialization", "General"),
                        certification=member_data.get("certification", "Medical"),
                        availability=availability
                    ))
                elif role == "Maintenance":
                    self.staff.append(Maintenance(
                        name=name,
                        skills=member_data.get("skills", "General"),
                        shift=member_data.get("shift", "Morning"),
                        availability=availability,
                        tools=member_data.get("tools", ["tool"])
                    ))
                elif role == "Seller":
                    self.staff.append(Seller(
                        name=name,
                        sales_experience=member_data.get("sales_experience", 1),
                        products=member_data.get("products", ["Product"]),
                        availability=availability
                    ))

        except FileNotFoundError:
            print("data.json not found. Starting with an empty staff list.")
            self.staff = []
        except Exception as e:
            print("Error loading staff:", e)
            messagebox.showerror("Error", f"Error loading staff: {e}")

    def save_and_close(self):
        self.save_staff()
        self.root.destroy()