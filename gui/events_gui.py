import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class EventSelectorGUI:
    def __init__(self, root, events):
        self.root = root
        self.root.title("Event Selector")
        self.events = events
        print(events)

        # Search Bar
        tk.Label(root, text="Search Events:").pack(pady=5)
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(root, textvariable=self.search_var)
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.filter_events)

        # Treeview for Event List
        self.tree = ttk.Treeview(root, columns=("Name", "Date", "Time", "Location", "Teams"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Location", text="Location")
        self.tree.heading("Teams", text="Teams")
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        # Populate Treeview
        self.populate_tree()

        # Buttons
        tk.Button(root, text="View Event", command=self.view_event).pack(pady=5)
        tk.Button(root, text="Close", command=root.destroy).pack(pady=5)

    def populate_tree(self):
        for event in self.events:
            self.tree.insert(
                "",
                "end",
                values=(
                    event.name,  # Event name
                    event.start.strftime("%Y-%m-%d"),  # Event date
                    event.start.strftime("%H:%M"),  # Event time
                    event.location,  # Stadium name
                    ", ".join(event.teams) if hasattr(event, "teams") else "N/A",  # Teams
                ),
            )

    def filter_events(self, event=None):
        query = self.search_var.get().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for event in self.events:
            # Use dot notation to access object attributes
            if query in event.name.lower() or query in event.location.lower():
                self.tree.insert("", "end", values=(
                    event.name,
                    event.start.strftime("%Y-%m-%d"),
                    event.start.strftime("%H:%M"),
                    event.location,
                    ", ".join(event.teams) if hasattr(event, "teams") else "N/A",
                ))

    def view_event(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select an event.")
            return
        event_details = self.tree.item(selected_item, "values")
        messagebox.showinfo("Event Details", f"Name: {event_details[0]}\nDate: {event_details[1]}\nTime: {event_details[2]}\nLocation: {event_details[3]}")