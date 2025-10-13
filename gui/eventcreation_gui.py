import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox
from events import FriendlyMatch, Tournament, TrainingSession, OfficialMatch


class EventCreationGUI:
    def __init__(self, root, save_event_callback):
        self.root = root
        self.root.title("Create Event")
        self.save_event_callback = save_event_callback

        # Dynamic fields frame (initialize first)
        self.dynamic_frame = tk.Frame(root)
        self.dynamic_frame.pack(pady=10)

        # Event type selection
        tk.Label(root, text="Select Event Type:").pack(pady=5)
        self.event_type_var = tk.StringVar(value="Friendly")
        self.event_type_menu = tk.OptionMenu(root, self.event_type_var, "Friendly", "Official", "Tournament",
                                             "Training", command=self.update_form)
        self.event_type_menu.pack(pady=5)

        # Common fields
        tk.Label(root, text="Event Name:").pack(pady=5)
        self.name_entry = tk.Entry(root)
        self.name_entry.pack(pady=5)

        tk.Label(root, text="Location:").pack(pady=5)
        self.location_var = tk.StringVar(value="Stadium A")
        self.location_menu = tk.OptionMenu(root, self.location_var, "Stadium A", "Stadium B", "Stadium C", "Stadium D")
        self.location_menu.pack(pady=5)

    def update_form(self, event_type):
        # Clear dynamic fields
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        # Common fields for all event types
        if event_type != "Tournament":
            tk.Label(self.dynamic_frame, text="Start Time:").pack(pady=5)
            self.start_hour = tk.Spinbox(self.dynamic_frame, from_=0, to=23, width=5)
            self.start_hour.pack(side=tk.LEFT, padx=5)
            self.start_minute = tk.Spinbox(self.dynamic_frame, from_=0, to=59, width=5)
            self.start_minute.pack(side=tk.LEFT, padx=5)

            tk.Label(self.dynamic_frame, text="Duration (minutes):").pack(pady=5)
            self.duration_spinbox = tk.Spinbox(self.dynamic_frame, from_=15, to=480, increment=15, width=5)
            self.duration_spinbox.pack(pady=5)

        if event_type == "Friendly":
            tk.Label(self.dynamic_frame, text="Teams (comma-separated):").pack(pady=5)
            self.teams_entry = tk.Entry(self.dynamic_frame)
            self.teams_entry.pack(pady=5)

        elif event_type == "Official":
            tk.Label(self.dynamic_frame, text="Referee Level:").pack(pady=5)
            self.referee_entry = tk.Entry(self.dynamic_frame)
            self.referee_entry.pack(pady=5)
            self.sport_entry = tk.Entry(self.dynamic_frame)
            self.sport_entry.pack(pady=5)

            tk.Label(self.dynamic_frame, text="Commentators (comma-separated):").pack(pady=5)
            self.commentators_entry = tk.Entry(self.dynamic_frame)
            self.commentators_entry.pack(pady=5)

        elif event_type == "Tournament":
            tk.Label(self.dynamic_frame, text="Teams (comma-separated):").pack(pady=5)
            self.teams_entry = tk.Entry(self.dynamic_frame)
            self.teams_entry.pack(pady=5)

            tk.Label(self.dynamic_frame, text="Format (knockout/round-robin/mixed):").pack(pady=5)
            self.format_entry = tk.Entry(self.dynamic_frame)
            self.format_entry.pack(pady=5)

        elif event_type == "Training":
            tk.Label(self.dynamic_frame, text="Coach Name:").pack(pady=5)
            self.coach_entry = tk.Entry(self.dynamic_frame)
            self.coach_entry.pack(pady=5)

    def save_event(self):
        event_type = self.event_type_var.get()
        name = self.name_entry.get()
        location = self.location_var.get()
        commentators = self.commentators_entry.get()
        sport = self.sport_entry.get()


        try:
            # Get start time from Spinbox values
            start_hour = int(self.start_hour.get())
            start_minute = int(self.start_minute.get())
            start_datetime = datetime.now().replace(hour=start_hour, minute=start_minute, second=0, microsecond=0)

            # Get duration and calculate end time
            duration = int(self.duration_spinbox.get())
            end_datetime = start_datetime + timedelta(minutes=duration)

            if event_type == "Friendly":
                teams = [team.strip() for team in self.teams_entry.get().split(",")]
                event = FriendlyMatch(name, start_datetime, end_datetime, location, teams)

            elif event_type == "Official":
                referee = {"level": self.referee_entry.get()}
                commentators = [c.strip() for c in self.commentators_entry.get().split(",")]
                event = OfficialMatch(name, start_datetime, location, sport ,referee, commentators)

            elif event_type == "Tournament":
                teams = [team.strip() for team in self.teams_entry.get().split(",")]
                format = self.format_entry.get()
                event = Tournament(name, start_datetime, end_datetime, location, teams, format)

            elif event_type == "Training":
                coach = self.coach_entry.get()
                event = TrainingSession(name, start_datetime, end_datetime, location, coach)

            else:
                raise ValueError("Invalid event type.")

            # Call the callback to save the event
            self.save_event_callback(event)
            messagebox.showinfo("Success", "Event created successfully!")
            self.root.destroy()

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")