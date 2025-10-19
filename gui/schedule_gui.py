import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime, time
from events import *
from events import validation, scheduling
from gui.eventcreation_gui import EventCreationGUI

class CustomCalendar:
    def __init__(self, parent, on_date_select, **kwargs):
        # Initialize the tkcalendar.Calendar widget
        self.calendar = Calendar(parent, **kwargs)
        self.calendar.pack(pady=20)
        self.calendar.bind("<<CalendarSelected>>", lambda e: on_date_select(self.get_selected_date()))

    def get_selected_date(self):
        # Return the currently selected date
        return self.calendar.selection_get()

    def clear_highlights(self):
        # Remove all calendar events
        self.calendar.calevent_remove("all")

    def highlight_full(self, date):
        # Highlight a date as "full" (e.g., red background)
        self.calendar.calevent_create(date, "Full", "full")
        self.calendar.tag_config("full", background="red", foreground="white")

    def highlight_not_full(self, date):
        # Highlight a date as "not full" (e.g., yellow background)
        self.calendar.calevent_create(date, "Not Full", "not_full")
        self.calendar.tag_config("not_full", background="yellow", foreground="black")


class ScheduleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Event Calendar")

        # Load events from the file
        self.events = scheduling.load_schedule_from_file()

        #Initialize selected and current date
        self.selected_date = datetime.now().date()
        self.current_date = datetime.now().date()

        # Calendar widget
        self.custom_calendar = CustomCalendar(
            root,
            on_date_select=self.update_selected_date,
            date_pattern="yyyy-mm-dd",
            selectmode="day",
        )


        # Highlight busy days
        self.highlight_busy_days()

        # Button to confirm event creation
        tk.Button(root, text="Create Event", command=self.create_event).pack(pady=10)

    def update_selected_date(self, date):
        # Update the selected date when the user selects a date in the calendar
        self.selected_date = date

    def highlight_busy_days(self):
        # Clear existing highlights
        self.custom_calendar.clear_highlights()

        # Highlight days based on event count
        event_counts = {}
        for event in self.events:
            event_date = event.start.date()
            event_counts[event_date] = event_counts.get(event_date, 0) + 1

        for date, count in event_counts.items():
            if count >= 5:  # Example: 5 or more events = "full"
                self.custom_calendar.highlight_full(date)
            else:  # Less than 5 events = "not full"
                self.custom_calendar.highlight_not_full(date)


    def create_event(self):
        # Open a new window for event creation
        event_window = tk.Toplevel(self.root)
        event_window.title("Create New Event")

        # Initialize the EventCreationGUI with a callback for saving the event
        EventCreationGUI(
            root=event_window,
            save_event_callback=self.save_event,
            selected_date=self.selected_date,
            current_date=self.current_date,
        )

    def save_event(self, event):
        try:
            # Load existing events
            existing_events = scheduling.load_schedule_from_file()
            # Validate for overlaps
            validation.validate_no_overlap(event, existing_events)
        except ValueError as e:
            # Show overlap error message
            messagebox.showerror("Overlap Error", str(e))
            return  # Stop further execution if there's an overlap

        # If no overlap, save the event
        self.events.append(event)
        scheduling.save_schedule_to_file(self.events)
        self.highlight_busy_days()
        messagebox.showinfo("Success", "Event saved successfully!")


