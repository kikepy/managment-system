import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json

class EventSelectorGUI:
    def __init__(self, root, events):
        self.root = root
        self.root.title("Event Selector")
        self.events = events

        # Search Bar
        tk.Label(root, text="Search Events:").pack(pady=5)
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(root, textvariable=self.search_var)
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.filter_events)

        # Treeview for Event List
        self.tree = ttk.Treeview(root, columns=("Type", "Name", "Date", "Time", "Location", "Teams"), show="headings")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Location", text="Location")
        self.tree.heading("Teams", text="Teams")
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        # Populate initial data
        self.populate_tree()

        # Buttons
        tk.Button(root, text="View Event", command=self.view_event).pack(pady=5)
        tk.Button(root, text="Close", command=root.destroy).pack(pady=5)

    def populate_tree(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            with open('events.json', 'r') as file:
                events_data = json.load(file)

            for event_type, events in events_data.items():
                for event in events:
                    start_time = datetime.fromisoformat(event['schedule']['start'])
                    teams = f"{event['teams']['home']} vs {event['teams']['away']}" if 'teams' in event else "N/A"

                    self.tree.insert("", "end", values=(
                        event_type,
                        event['event_info']['name'],
                        start_time.strftime('%Y-%m-%d'),
                        start_time.strftime('%H:%M'),
                        event['schedule']['location'],
                        teams
                    ))
        except FileNotFoundError:
            messagebox.showwarning("Warning", "No events found")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading events: {str(e)}")

    def filter_events(self, event=None):
        search_term = self.search_var.get().lower()

        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            with open('events.json', 'r') as file:
                events_data = json.load(file)

            for event_type, events in events_data.items():
                for event in events:
                    start_time = datetime.fromisoformat(event['schedule']['start'])
                    teams = f"{event['teams']['home']} vs {event['teams']['away']}" if 'teams' in event else "N/A"

                    # Check if search term matches any field
                    if (search_term in event_type.lower() or
                        search_term in event['event_info']['name'].lower() or
                        search_term in event['schedule']['location'].lower() or
                        search_term in teams.lower()):

                        self.tree.insert("", "end", values=(
                            event_type,
                            event['event_info']['name'],
                            start_time.strftime('%Y-%m-%d'),
                            start_time.strftime('%H:%M'),
                            event['schedule']['location'],
                            teams
                        ))
        except FileNotFoundError:
            pass

    def view_event(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an event to view")
            return

        values = self.tree.item(selected_item)['values']
        message = f"Event Type: {values[0]}\n"
        message += f"Name: {values[1]}\n"
        message += f"Date: {values[2]}\n"
        message += f"Time: {values[3]}\n"
        message += f"Location: {values[4]}\n"
        message += f"Teams: {values[5]}"

        messagebox.showinfo("Event Details", message)