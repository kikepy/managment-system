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
        print("populate_tree called")
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            with open('events.json', 'r') as file:
                events_data = json.load(file)
                print("Loaded events data:", events_data)  # Debugging line
                print("Event types in data:", events_data.keys())  # Debugging line

            for event_type, events in events_data.items():
                for event in events:
                    try:
                        if event_type == "Tournament":
                            # Process each match in the tournament schedule
                            for match in event['schedule']:
                                start_time = datetime.fromisoformat(match['schedule']['start'])
                                teams = f"{match['teams']['home']} vs {match['teams']['away']}"
                                self.tree.insert("", "end", values=(
                                    event_type,
                                    match['event_info']['name'],
                                    start_time.strftime('%Y-%m-%d'),
                                    start_time.strftime('%H:%M'),
                                    match['schedule'].get('location', 'N/A'),
                                    teams
                                ))
                        else:
                            # Process non-tournament events
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
                    except Exception as e:
                        print(f"Error processing event: {event}. Error: {e}")
        except FileNotFoundError:
            messagebox.showwarning("Warning", "No events found")
        except Exception as e:
            print("Error in populate_tree:", e)
            messagebox.showerror("Error", f"Error loading events: {str(e)}")

    def filter_events(self, event=None):
        print("filter_events called")
        search_term = self.search_var.get().lower()

        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            with open('events.json', 'r') as file:
                events_data = json.load(file)
                print("Loaded events data:", events_data)
                print("Event types in data:", events_data.keys())

            for event_type, events in events_data.items():
                if event_type == "Tournament":
                    for tournament in events:
                        # Validate schedule
                        schedule = tournament.get('schedule', [])
                        print(f"Schedule: {schedule}")
                        if isinstance(schedule, list) and len(schedule) > 0:
                            first_match = schedule[0]
                            print(f"First Match: {first_match}")
                            if isinstance(first_match, dict) and 'schedule' in first_match:
                                start_date = first_match['schedule'].get('start')
                                print(f"Start Date: {start_date}")
                                if start_date:
                                    try:
                                        start_date = datetime.fromisoformat(start_date).strftime('%Y-%m-%d')
                                        teams = ', '.join(tournament.get('teams', []))
                                        if search_term in tournament['event_info']['name'].lower() or search_term in start_date:
                                            self.tree.insert("", "end", values=(
                                                "Tournament",
                                                f"Tournament starts on {start_date}. Teams participating: {teams}",
                                                start_date,
                                                "N/A",
                                                "N/A",
                                                "Click to view matches"
                                            ), tags=("tournament",))
                                    except ValueError:
                                        print(f"Invalid date format: {start_date}")
                else:
                    self._process_general_events(event_type, events, search_term)
        except FileNotFoundError:
            messagebox.showwarning("Warning", "Events file not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error filtering events: {str(e)}")
    def _process_general_events(self, event_type, events, search_term):
        for event in events:
            if isinstance(event, dict):
                start_time = event['schedule'].get('start')
                if start_time:
                    start_time = datetime.fromisoformat(start_time)
                    teams = f"{event['teams']['home']} vs {event['teams']['away']}" if 'teams' in event else "N/A"

                    # Check if the search term matches
                    if (search_term in event_type.lower() or
                            search_term in event['event_info']['name'].lower() or
                            search_term in teams.lower()):
                        self.tree.insert("", "end", values=(
                            event_type,
                            event['event_info']['name'],
                            start_time.strftime('%Y-%m-%d'),
                            start_time.strftime('%H:%M'),
                            event['schedule'].get('location', 'N/A'),
                            teams
                        ))

    def view_event(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an event to view")
            return

        values = self.tree.item(selected_item)['values']
        print("Selected item values:", values)  # Debugging line

        if values[0] == "Tournament":
            # Open a new window to display tournament matches
            tournament_window = tk.Toplevel(self.root)
            tournament_window.title(f"Tournament Matches")

            tree = ttk.Treeview(tournament_window, columns=("Round", "Name", "Date", "Time", "Location", "Teams"),
                                show="headings")
            tree.heading("Round", text="Round")
            tree.heading("Name", text="Name")
            tree.heading("Date", text="Date")
            tree.heading("Time", text="Time")
            tree.heading("Location", text="Location")
            tree.heading("Teams", text="Teams")
            tree.pack(pady=10, fill=tk.BOTH, expand=True)

            try:
                with open('events.json', 'r') as file:
                    events_data = json.load(file)
                    print("Loaded events data:", events_data)  # Debugging line

                # Find the tournament that contains the selected match
                for tournament in events_data.get("Tournament", []):
                    for match in tournament.get('schedule', []):
                        if match['event_info']['name'] == values[1]:  # Match the selected match name
                            print("Tournament matched:", tournament['event_info']['name'])  # Debugging line
                            # Display all matches of the tournament
                            for match in tournament.get('schedule', []):
                                start_time = datetime.fromisoformat(match['schedule']['start'])
                                teams = f"{match['teams']['home']} vs {match['teams']['away']}"
                                tree.insert("", "end", values=(
                                    match['round'],
                                    match['event_info']['name'],
                                    start_time.strftime('%Y-%m-%d'),
                                    start_time.strftime('%H:%M'),
                                    match['schedule'].get('location', 'N/A'),
                                    teams
                                ))
                            return  # Exit after displaying the matches
            except FileNotFoundError:
                messagebox.showwarning("Warning", "No tournaments found")
            except Exception as e:
                print("Error in view_event:", e)  # Debugging line
                messagebox.showerror("Error", f"Error loading tournament matches: {str(e)}")
        else:
            # Show details of a non-tournament event
            message = f"Event Type: {values[0]}\n"
            message += f"Name: {values[1]}\n"
            message += f"Date: {values[2]}\n"
            message += f"Time: {values[3]}\n"
            message += f"Location: {values[4]}\n"
            message += f"Teams: {values[5]}"
            messagebox.showinfo("Event Details", message)