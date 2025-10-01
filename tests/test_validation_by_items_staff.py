import unittest
from datetime import datetime
from events.validation import validate_no_overlap, existing_events

class TestValidationByItemsAndStaff(unittest.TestCase):
    def setUp(self):
        # Clear the existing events before each test
        existing_events.clear()

    def test_overlap_by_items(self):
        print("Test: Adding an event that overlaps by items...")

        # Add an existing event with specific items
        existing_events.append({
            "name": "Event 1",
            "start": datetime(2023, 12, 1, 10, 0),
            "end": datetime(2023, 12, 1, 12, 0),
            "items": ["Projector", "Room A"],
            "staff": ["Staff A"]
        })

        # Define an overlapping event using the same item
        start = datetime(2023, 12, 1, 11, 0)
        end = datetime(2023, 12, 1, 13, 0)
        items = ["Projector"]
        staff = ["Staff B"]

        with self.assertRaises(ValueError) as context:
            validate_no_overlap(start, end, items, staff)

        print(f"Exception raised as expected for items: {context.exception}")

    def test_overlap_by_staff(self):
        print("Test: Adding an event that overlaps by staff...")

        # Add an existing event with specific staff
        existing_events.append({
            "name": "Event 1",
            "start": datetime(2023, 12, 1, 10, 0),
            "end": datetime(2023, 12, 1, 12, 0),
            "items": ["Room B"],
            "staff": ["Staff A"]
        })

        # Define an overlapping event using the same staff
        start = datetime(2023, 12, 1, 11, 0)
        end = datetime(2023, 12, 1, 13, 0)
        items = ["Room C"]
        staff = ["Staff A"]

        with self.assertRaises(ValueError) as context:
            validate_no_overlap(start, end, items, staff)

        print(f"Exception raised as expected for staff: {context.exception}")

if __name__ == "__main__":
    unittest.main()