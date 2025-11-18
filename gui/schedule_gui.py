import json
import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime
from gui.eventcreation_gui import EventCreationGUI

class CustomCalendar(Calendar):
    def __init__(self, parent, **kwargs):
        kwargs['selectmode'] = 'day'
        kwargs['showweeknumbers'] = False
        super().__init__(parent, **kwargs)

        # Configure the tag appearance
        self.tag_config('has_events', background='yellow', foreground='black')
        self.tag_config('tournament_day', background='red', foreground='white')
        self.load_events()

    def load_events(self):
        # Clear existing calendar events
        for date, tags in self.get_calevents():
            self.calevent_remove(date)

        try:
            with open('events.json', 'r') as file:
                events_data = json.load(file)

            # Preprocess events into a flat structure
            tournament_days = set()
            other_events = []

            for event_type, events in events_data.items():
                for event in events:
                    if event_type == "Tournament":
                        for match in event.get('schedule', []):
                            if isinstance(match, dict) and 'schedule' in match:
                                start = match['schedule'].get('start')
                                if start and start != "TBD":
                                    try:
                                        match_date = datetime.fromisoformat(start).date()
                                        tournament_days.add(match_date)
                                        self.calevent_create(
                                            date=match_date,
                                            text=f"Tournament: {event['event_info']['name']}",
                                            tags='tournament_day'
                                        )
                                    except ValueError:
                                        print(f"Invalid date format in match: {match}")
                    else:
                        start = event['schedule'].get('start')
                        if start and start != "TBD":
                            try:
                                event_date = datetime.fromisoformat(start).date()
                                other_events.append((event_date, event_type, event['event_info']['name']))
                            except ValueError:
                                print(f"Invalid date format in event: {event}")

            # Add other events only if they are not on tournament days
            for event_date, event_type, event_name in other_events:
                if event_date not in tournament_days:
                    self.calevent_create(
                        date=event_date,
                        text=f"{event_type}: {event_name}",
                        tags='has_events'
                    )

        except FileNotFoundError:
            print("Events file not found.")
        except Exception as e:
            print(f"Error loading events: {e}")

class ScheduleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Event Calendar")

        #Initialize selected and current date
        self.selected_date = datetime.now().date()
        self.current_date = datetime.now().date()

        # Calendar widget
        self.custom_calendar = CustomCalendar(
            root,
            date_pattern="yyyy-mm-dd",
            selectmode="day",
        )
        self.custom_calendar.pack(pady=10)

        # Bind date selection event
        self.custom_calendar.bind("<<CalendarSelected>>", self.update_selected_date)

        # Button to confirm event creation
        tk.Button(root, text="Create Event", command=self.create_event).pack(pady=10)

    def update_selected_date(self, event=None):
        # Update the selected date when the user selects a date in the calendar
        self.selected_date = self.custom_calendar.selection_get()

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
            with open('events.json', 'r') as file:
                events_data = json.load(file)

            # Add new event to events data
            event_type = event.event_type.capitalize()
            if event_type not in events_data:
                events_data[event_type] = []
            events_data[event_type].append(event.to_dict())

            # Save updated events
            with open('events.json', 'w') as file:
                json.dump(events_data, file, indent=4)

            # Reload calendar events
            self.custom_calendar.load_events()
            messagebox.showinfo("Success", "Event saved successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save event: {str(e)}")


