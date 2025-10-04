import tkinter as tk
from gui.item_gui import ItemGUI
from gui.staff_gui import StaffGUI

class MainGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Management System")

        # Main Menu Buttons
        tk.Label(root, text="Choose an option:", font=("Arial", 16)).pack(pady=20)

        tk.Button(root, text="Manage Items", width=20, command=self.open_item_gui).pack(pady=10)
        tk.Button(root, text="Manage Staff", width=20, command=self.open_staff_gui).pack(pady=10)
        tk.Button(root, text="Schedule Events", width=20, command=self.schedule_events).pack(pady=10)

    def open_item_gui(self):
        item_window = tk.Toplevel(self.root)
        ItemGUI(item_window)

    def open_staff_gui(self):
        staff_window = tk.Toplevel(self.root)
        StaffGUI(staff_window)

    def schedule_events(self):
        event_window = tk.Toplevel(self.root)
        event_window.title("Schedule Events")
        tk.Label(event_window, text="Event scheduling functionality coming soon!", font=("Arial", 14)).pack(pady=20)

# Run the Main GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = MainGUI(root)
    root.mainloop()