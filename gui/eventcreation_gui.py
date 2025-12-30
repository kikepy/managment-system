import json
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta
from events import *
from events.validation import validate_event

FACULTIES = [
    "MATCOM", "FHS", "LEX", "EKO",
    "FCOM", "BIO", "INSTEC", "FAYL", "Geo", "FLEX", "CONFIN",
    "IFAL", "AAAC", "FTUR", "ISDI", "PSICO", "FENHI", "FISICA",
    "ISRI", "QUIMICA"
]

FORMAT = [
    "Knockout",
    "League",
]
class EventCreationGUI:
    def __init__(self, root, save_event_callback, selected_date, current_date):
        self.root = root
        self.root.title("Create Event")
        self.save_event_callback = save_event_callback
        self.selected_date = selected_date
        self.current_date = current_date
        self.selected_dates = []

        common_frame = ttk.LabelFrame(root, text="Event Details", padding=10)
        common_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(common_frame, text="Event Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = ttk.Entry(common_frame, width=30)
        self.name_entry.grid(row=0, column=1, pady=5)

        ttk.Label(common_frame, text="Location:").grid(row=1, column=0, sticky="w", pady=5)
        self.location_entry = ttk.Combobox(common_frame, values=["Stadium A", "Stadium B", "Stadium C"],
                                           state="readonly")
        self.location_entry.grid(row=1, column=1, pady=5)
        self.location_entry.set("Stadium A")

        ttk.Label(common_frame, text="Start Time:").grid(row=2, column=0, sticky="w", pady=5)
        time_frame = ttk.Frame(common_frame)
        time_frame.grid(row=2, column=1, sticky="w")
        self.start_hour = ttk.Spinbox(time_frame, from_=7, to=18, width=5)
        self.start_hour.grid(row=0, column=0, padx=(0, 5))
        self.start_minute = ttk.Spinbox(time_frame, from_=0, to=59, width=5)
        self.start_minute.grid(row=0, column=1)

        ttk.Label(common_frame, text="Duration (minutes):").grid(row=3, column=0, sticky="w", pady=5)
        self.duration_spinbox = ttk.Spinbox(common_frame, from_=15, to=480, increment=15, width=10)
        self.duration_spinbox.grid(row=3, column=1, pady=5)

        ttk.Label(common_frame, text="Event Type:").grid(row=4, column=0, sticky="w", pady=5)
        self.event_type_var = tk.StringVar(value="Friendly")
        self.event_type_menu = ttk.Combobox(common_frame, textvariable=self.event_type_var,
                                            values=["Friendly", "Official", "Tournament", "Training"], state="readonly")
        self.event_type_menu.grid(row=4, column=1, pady=5)
        self.event_type_menu.bind("<<ComboboxSelected>>", self.update_dynamic_fields)

        self.dynamic_frame = ttk.LabelFrame(root, text="Event-Specific Details", padding=10)
        self.dynamic_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ttk.Button(root, text="Save Event", command=self.save_event).grid(row=2, column=0, pady=10)

        self.update_dynamic_fields()

    def update_dynamic_fields(self, *args):
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        event_type = self.event_type_var.get()

        if event_type == "Friendly":
            ttk.Label(self.dynamic_frame, text="Teams:").grid(row=0, column=0, sticky="w", pady=5)
            self.teams_listbox = tk.Listbox(self.dynamic_frame, selectmode="multiple", height=5)
            self.teams_listbox.grid(row=0, column=1, pady=5)
            for team in FACULTIES:
                self.teams_listbox.insert("end", team)

        elif event_type == "Official":
            ttk.Label(self.dynamic_frame, text="Referee Level:").grid(row=0, column=0, sticky="w", pady=5)
            self.referee_entry = ttk.Entry(self.dynamic_frame, width=20)
            self.referee_entry.grid(row=0, column=1, pady=5)

            ttk.Label(self.dynamic_frame, text="Commentators:").grid(row=1, column=0, sticky="w", pady=5)
            self.commentators_entry = ttk.Entry(self.dynamic_frame, width=30)
            self.commentators_entry.grid(row=1, column=1, pady=5)

        elif event_type == "Tournament":
            ttk.Label(self.dynamic_frame, text="Teams:").grid(row=0, column=0, sticky="w", pady=5)
            self.teams_listbox = tk.Listbox(self.dynamic_frame, selectmode="multiple", height=5)
            self.teams_listbox.grid(row=0, column=1, pady=5)
            for team in FACULTIES:
                self.teams_listbox.insert("end", team)

            ttk.Label(self.dynamic_frame, text="Format:").grid(row=1, column=0, sticky="w", pady=5)
            self.format_var = tk.StringVar(value="Knockout")
            self.format_menu = ttk.Combobox(self.dynamic_frame, textvariable=self.format_var, values=FORMAT,
                                            state="readonly")
            self.format_menu.grid(row=1, column=1, pady=5)

            ttk.Label(self.dynamic_frame, text="Specific Days:").grid(row=2, column=0, sticky="w", pady=5)
            self.calendar = Calendar(self.dynamic_frame, selectmode="day", date_pattern="yyyy-mm-dd")
            self.calendar.grid(row=2, column=1, pady=5)

        elif event_type == "Training":
            ttk.Label(self.dynamic_frame, text="Coach Name:").grid(row=0, column=0, sticky="w", pady=5)
            self.coach_entry = ttk.Entry(self.dynamic_frame, width=30)
            self.coach_entry.grid(row=0, column=1, pady=5)

    def update_dynamic_fields(self, *args):
        # Clear dynamic fields
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        event_type = self.event_type_var.get()

        if event_type == "Friendly":
            ttk.Label(self.dynamic_frame, text="Teams:").grid(row=0, column=0, sticky="w", pady=5)
            self.teams_listbox = tk.Listbox(self.dynamic_frame, selectmode="multiple", height=5)
            self.teams_listbox.grid(row=0, column=1, pady=5)
            for team in ["Team A", "Team B", "Team C"]:
                self.teams_listbox.insert("end", team)

        elif event_type == "Official":
            ttk.Label(self.dynamic_frame, text="Referee Level:").grid(row=0, column=0, sticky="w", pady=5)
            self.referee_entry = ttk.Entry(self.dynamic_frame, width=20)
            self.referee_entry.grid(row=0, column=1, pady=5)

            ttk.Label(self.dynamic_frame, text="Commentators:").grid(row=1, column=0, sticky="w", pady=5)
            self.commentators_entry = ttk.Entry(self.dynamic_frame, width=30)
            self.commentators_entry.grid(row=1, column=1, pady=5)

        elif event_type == "Tournament":
            ttk.Label(self.dynamic_frame, text="Teams:").grid(row=0, column=0, sticky="w", pady=5)
            self.teams_listbox = tk.Listbox(self.dynamic_frame, selectmode="multiple", height=5)
            self.teams_listbox.grid(row=0, column=1, pady=5)
            for team in ["Team A", "Team B", "Team C", "Team D"]:
                self.teams_listbox.insert("end", team)

            ttk.Label(self.dynamic_frame, text="Format:").grid(row=1, column=0, sticky="w", pady=5)
            self.format_var = tk.StringVar(value="Knockout")
            self.format_menu = ttk.Combobox(self.dynamic_frame, textvariable=self.format_var,
                                            values=["Knockout", "Round-Robin"], state="readonly")
            self.format_menu.grid(row=1, column=1, pady=5)

            ttk.Label(self.dynamic_frame, text="Specific Days:").grid(row=2, column=0, sticky="w", pady=5)
            self.calendar = Calendar(self.dynamic_frame, selectmode="day", date_pattern="yyyy-mm-dd")
            self.calendar.grid(row=2, column=1, pady=5)

        elif event_type == "Training":
            ttk.Label(self.dynamic_frame, text="Coach Name:").grid(row=0, column=0, sticky="w", pady=5)
            self.coach_entry = ttk.Entry(self.dynamic_frame, width=30)
            self.coach_entry.grid(row=0, column=1, pady=5)

    def add_tournament_date(self):
        selected_date = self.tournament_calendar.get_date()
        if selected_date:
            if selected_date not in self.selected_dates:
                self.selected_dates.append(selected_date)
                self.selected_dates.sort()
                self.update_dates_listbox()

    def remove_tournament_date(self):
        selection = self.dates_listbox.curselection()
        if selection:
            index = selection[0]
            date = self.dates_listbox.get(index)
            self.selected_dates.remove(date)
            self.update_dates_listbox()

    def update_dates_listbox(self):
        self.dates_listbox.delete(0, tk.END)
        for date in sorted(self.selected_dates):
            self.dates_listbox.insert(tk.END, date)

    def save_event(self):
        try:
            # Collect common fields
            event_type = self.event_type_var.get()
            name = self.name_entry.get()
            location = self.location_entry.get()
            sport = self.sport_var.get()
            start_hour = int(self.start_hour.get())
            start_minute = int(self.start_minute.get())
            duration = int(self.duration_spinbox.get())

            # Use the selected date (passed during initialization)
            selected_date = self.selected_date
            start_datetime = datetime.combine(selected_date, datetime.min.time()).replace(
                hour=start_hour, minute=start_minute
            )
            end_datetime = start_datetime + timedelta(minutes=duration)

            # Collect dynamic fields based on event type
            if event_type == "Friendly":
                selected_indices = self.teams_listbox.curselection()
                teams = [FACULTIES[i] for i in selected_indices]
                event = FriendlyMatch(name, start_datetime, location, sport, teams)

            elif event_type == "Official":
                referee = {"level": self.referee_entry.get()}
                commentators = [c.strip() for c in self.commentators_entry.get().split(",")]
                event = OfficialMatch(name, start_datetime, location, sport, referee, commentators)

            elif event_type == "Tournament":
                selected_indices = self.teams_listbox.curselection()
                teams = [self.teams_listbox.get(i) for i in selected_indices]
                format = self.format_var.get().lower()
                specific_days = [datetime.strptime(date, '%Y-%m-%d') for date in self.selected_dates]
                event = Tournament(name, start_datetime, location, sport, teams, format, specific_days)

            elif event_type == "Training":
                coach = self.coach_entry.get()
                event = Training(name, start_datetime, end_datetime, location, coach)

            else:
                raise ValueError("Invalid event type.")

            # Load resources
            events_file_path = 'events.json'
            data_file_path = 'data.json'

            with open(data_file_path, 'r') as file:
                data = json.load(file)

            available_items = {item['type']: item['total_quantity'] for item in data['items']}
            available_staff = {staff['role']: staff['availability'] for staff in data['staff']}

            try:
                with open(events_file_path, 'r') as file:
                    events_data = json.load(file)
                    existing_events = [
                        globals()[event_type].from_dict(event_dict)
                        for event_dict in events_data.get(event_type, [])
                    ]
            except FileNotFoundError:
                existing_events = []

            # Delegate validation to the centralized function
            try:
                validate_event(event, available_items, available_staff, existing_events)

                # Save the event
                if event_type not in events_data:
                    events_data[event_type] = []
                events_data[event_type].append(event.to_dict())

                with open(events_file_path, 'w') as file:
                    json.dump(events_data, file, indent=4)

                messagebox.showinfo("Success", "Event saved successfully!")
                self.root.destroy()

            except ValueError as e:
                messagebox.showerror("Error", f"Validation failed: {e}")

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

def adjust_time(self):
    """Adjust time to handle hour wrapping and minute overflow."""
    hour = int(self.start_hour.get())
    minute = int(self.start_minute.get())

        # Handle minute overflow
    if minute >= 60:
        minute = 0
        hour += 1
    # Wrap hour back to 7 AM if it exceeds 6 PM
    if hour > 18:
        hour = 7

        # Update the Spinbox values
    self.start_hour.delete(0, "end")
    self.start_hour.insert(0, hour)
    self.start_minute.delete(0, "end")
    self.start_minute.insert(0, minute)