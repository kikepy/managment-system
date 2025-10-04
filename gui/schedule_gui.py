import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime, time
from events import *
from events import validation, scheduling
from gui.eventcreation_gui import EventCreationGUI


class ScheduleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Event Calendar")

        # Load events from the file
        self.events = scheduling.load_schedule_from_file()

        # Calendar widget
        self.calendar = Calendar(root, date_pattern="yyyy-mm-dd", selectmode="day")
        self.calendar.pack(pady=20)

        # Highlight busy days
        self.highlight_busy_days()

        # Button to select a date
        tk.Button(root, text="Check Availability", command=self.check_availability).pack(pady=10)

        # Dropdown for available slots
        self.slot_var = tk.StringVar(value="Select a time slot")
        self.slot_menu = tk.OptionMenu(root, self.slot_var, [])
        self.slot_menu.pack(pady=10)

        # Button to confirm event creation
        tk.Button(root, text="Create Event", command=self.create_event).pack(pady=10)
    def highlight_busy_days(self):
        # Create a dictionary to count events per day
        day_event_count = {}
        for event in self.events:
            event_date = event["start"].date()
            day_event_count[event_date] = day_event_count.get(event_date, 0) + 1

        # Highlight days with events
        for day, count in day_event_count.items():
            self.calendar.calevent_create(day, f"{count} events", "busy")
            self.calendar.tag_config("busy", background="blue", foreground="white")

        # Highlight days with full schedules
        for day, count in day_event_count.items():
            if count >= 12:  # Assuming 12 one-hour slots from 7 AM to 7 PM
                self.calendar.calevent_create(day, "Full", "busy")
                self.calendar.tag_config("busy", background="red", foreground="white")

    def check_availability(self):
        selected_date = self.calendar.get_date()
        selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()

        # Count events for the selected day
        day_events = [
            event for event in self.events
            if event["start"].date() == selected_date
        ]

        if day_events:
            messagebox.showinfo("Events", f"There are {len(day_events)} events on {selected_date}.")
        else:
            messagebox.showinfo("Events", f"No events scheduled for {selected_date}.")

    def create_event(self):
        def save_event_callback(new_event):
            try:
                validation.validate_no_overlap(new_event)
                self.events.append(new_event)
                scheduling.save_schedule_to_file(self.events)
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        event_window = tk.Toplevel(self.root)
        EventCreationGUI(event_window, save_event_callback)

