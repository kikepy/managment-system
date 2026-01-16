import tkinter as tk
from config import data_file_path, events_file_path
from gui.eventcreation_gui import EventCreationGUI
from gui.item_gui import ItemGUI
from gui.staff_gui import StaffGUI

class MainGUI:
    def __init__(self, root, data_file_path, events_file_path):
        self.root = root
        self.data_file_path = data_file_path
        self.events_file_path = events_file_path
        self.root.title("Management System")
        self.root.geometry("800x600")
        self.root.resizable(True, True)


        # Main Menu Buttons
        tk.Label(root, text="Choose an option:", font=("Arial", 16)).pack(pady=20)

        tk.Button(root, text="Manage Items", width=20, command=self.open_item_gui).pack(pady=10)
        tk.Button(root, text="Manage Staff", width=20, command=self.open_staff_gui).pack(pady=10)
        tk.Button(root, text="Schedule Events", width=20, command=self.schedule_events).pack(pady=10)
        tk.Button(root, text="Search Events", width=20, command=self.open_event_search).pack(pady=10)

    def open_item_gui(self):
        item_window = tk.Toplevel(self.root)
        ItemGUI(item_window, self.data_file_path)

    def open_staff_gui(self):
        staff_window = tk.Toplevel(self.root)
        StaffGUI(staff_window, self.data_file_path)

    def schedule_events(self):
        event_window = tk.Toplevel(self.root)
        from gui.eventcreation_gui import EventCreationGUI
        EventCreationGUI(event_window, self.data_file_path, self.events_file_path)
    def open_event_search(self):
        event_window = tk.Toplevel(self.root)
        from events.scheduling import load_schedule_from_file
        from gui.events_gui import EventSelectorGUI
        events = load_schedule_from_file()
        EventSelectorGUI(event_window, events, events_file_path)
