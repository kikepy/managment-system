import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox
from events import *

FACULTIES = [
    "MATCOM", "FHS", "LEX", "EKO",
    "FCOM", "BIO", "INSTEC", "FAYL", "Geo", "FLEX", "CONFIN",
    "IFAL", "AAAC", "FTUR", "ISDI", "PSICO", "FENHI", "FISICA",
    "ISRI", "QUIMICA"
]
class EventCreationGUI:
    def __init__(self, root, save_event_callback, selected_date, current_date):
        self.root = root
        self.root.title("Create Event")
        self.save_event_callback = save_event_callback
        self.selected_date = selected_date
        self.current_date = current_date

        # Common fields
        tk.Label(root, text="Event Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Location:").grid(row=1, column=0, padx=5, pady=5)
        self.location_entry = tk.StringVar(value="Stadium A")
        self.location_menu = tk.OptionMenu(root, self.location_entry, "Stadium A", "Stadium B", "Stadium C",
                                           "Stadium D")
        self.location_menu.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Start Time:").grid(row=2, column=0, padx=5, pady=5)
        self.start_hour = tk.Spinbox(root, from_=7, to=18, wrap=True, width=5, command=self.adjust_time)
        self.start_hour.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.start_minute = tk.Spinbox(root, from_=0, to=59, wrap=True, width=5, command=self.adjust_time)
        self.start_minute.grid(row=2, column=1, padx=5, pady=5, sticky="e")

        tk.Label(root, text="Duration (minutes):").grid(row=3, column=0, padx=5, pady=5)
        self.duration_spinbox = tk.Spinbox(root, from_=15, to=480, increment=15, width=5)
        self.duration_spinbox.grid(row=3, column=1, padx=5, pady=5)

        # Event type selection
        tk.Label(root, text="Event Type:").grid(row=4, column=0, padx=5, pady=5)
        self.event_type_var = tk.StringVar(value="Friendly")
        self.event_type_menu = tk.OptionMenu(root, self.event_type_var, "Friendly", "Official", "Tournament",
                                             "Training",
                                             command=self.update_dynamic_fields)
        self.event_type_menu.grid(row=4, column=1, padx=5, pady=5)

        # Sport selection
        tk.Label(root, text="Sport:").grid(row=5, column=0, padx=5, pady=5)
        self.sport_var = tk.StringVar(value="Futsal")
        self.sport_menu = tk.OptionMenu(root, self.sport_var, "Futsal", "Basketball", "Volleyball")
        self.sport_menu.grid(row=5, column=1, padx=5, pady=5)

        # Dynamic fields frame
        self.dynamic_frame = tk.Frame(root)
        self.dynamic_frame.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        # Save button
        tk.Button(root, text="Save Event", command=self.save_event).grid(row=7, column=0, columnspan=2, pady=10)

        # Initialize dynamic fields
        self.update_dynamic_fields("Friendly")

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

    def update_dynamic_fields(self, event_type):
        # Clear dynamic fields
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        # Add fields based on event type
        if event_type == "Friendly":
            tk.Label(self.dynamic_frame, text="Teams:").grid(row=0, column=0, padx=5, pady=5)
            self.teams_listbox = tk.Listbox(self.dynamic_frame, selectmode="multiple", exportselection=False, height=10)
            for faculty in FACULTIES:
                self.teams_listbox.insert("end", faculty)
            self.teams_listbox.grid(row=0, column=1, padx=5, pady=5)

        elif event_type == "Official":
            tk.Label(self.dynamic_frame, text="Referee Level:").grid(row=0, column=0, padx=5, pady=5)
            self.referee_entry = tk.Entry(self.dynamic_frame)
            self.referee_entry.grid(row=0, column=1, padx=5, pady=5)

            tk.Label(self.dynamic_frame, text="Commentators (comma-separated):").grid(row=1, column=0, padx=5, pady=5)
            self.commentators_entry = tk.Entry(self.dynamic_frame)
            self.commentators_entry.grid(row=1, column=1, padx=5, pady=5)

        elif event_type == "Tournament":
            tk.Label(self.dynamic_frame, text="Teams (comma-separated):").grid(row=0, column=0, padx=5, pady=5)
            self.teams_entry = tk.Entry(self.dynamic_frame)
            self.teams_entry.grid(row=0, column=1, padx=5, pady=5)

            tk.Label(self.dynamic_frame, text="Format (knockout/round-robin/mixed):").grid(row=1, column=0, padx=5, pady=5)
            self.format_entry = tk.Entry(self.dynamic_frame)
            self.format_entry.grid(row=1, column=1, padx=5, pady=5)

        elif event_type == "Training":
            tk.Label(self.dynamic_frame, text="Coach Name:").grid(row=0, column=0, padx=5, pady=5)
            self.coach_entry = tk.Entry(self.dynamic_frame)
            self.coach_entry.grid(row=0, column=1, padx=5, pady=5)

    def save_event(self):
        # Collect common fields
        event_type = self.event_type_var.get()
        name = self.name_entry.get()
        location = self.location_entry.get()
        sport = self.sport_var.get()
        start_hour = int(self.start_hour.get())
        start_minute = int(self.start_minute.get())
        duration = int(self.duration_spinbox.get())

        # Use the selected date (passed during initialization)
        selected_date = self.selected_date  # Ensure this is passed when initializing EventCreationGUI
        start_datetime = datetime.combine(selected_date, datetime.min.time()).replace(
            hour=start_hour, minute=start_minute
        )
        end_datetime = start_datetime + timedelta(minutes=duration)

        # Check if the event is in the past
        if start_datetime < datetime.now():
            messagebox.showerror("Error", "The event cannot be created in the past.")
            return

        try:
            # Collect dynamic fields based on event type
            if event_type == "Friendly":
                # Use the Listbox to get selected teams
                selected_indices = self.teams_listbox.curselection()
                teams = [FACULTIES[i] for i in selected_indices]

                if len(teams) < 2:
                    messagebox.showerror("Error", "You must select at least two teams.")
                    return

                event = FriendlyMatch(name, start_datetime, location, sport, teams)

            elif event_type == "Official":
                referee = {"level": self.referee_entry.get()}
                commentators = [c.strip() for c in self.commentators_entry.get().split(",")]
                event = OfficialMatch(name, start_datetime, location, referee, commentators)

            elif event_type == "Tournament":
                teams = [team.strip() for team in self.teams_entry.get().split(",")]
                format = self.format_entry.get()
                event = Tournament(name, start_datetime, end_datetime, location, teams, format)

            elif event_type == "Training":
                coach = self.coach_entry.get()
                event = Training(name, start_datetime, end_datetime, location, coach)

            else:
                raise ValueError("Invalid event type.")

            # Load existing events
            existing_events = scheduling.load_schedule_from_file()

            # Validate for overlaps
            try:
                 validation.validate_no_overlap(event, existing_events)
            except ValueError as e:
                messagebox.showerror("Overlap Error", str(e))
                return  # Stop further execution if there's an overlap

            # Save the event using the callback
            self.save_event_callback(event)
            self.root.destroy()

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")