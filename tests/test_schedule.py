import unittest
from datetime import datetime
from events.validation import validate_no_overlap, existing_events

class TestValidationOverlap(unittest.TestCase):
    def setUp(self):
        # Clear the existing events before each test
        existing_events.clear()

    def test_no_overlap_validation(self):
        print("Test: Adding an event that overlaps with an existing one...")

        # Add an existing event
        existing_events.append({
            "name": "Event 1",
            "start": datetime(2023, 12, 1, 10, 0),
            "end": datetime(2023, 12, 1, 12, 0)
        })

        # Define an overlapping event
        start = datetime(2023, 12, 1, 11, 0)
        end = datetime(2023, 12, 1, 13, 0)

        # Assert that a ValueError is raised for overlapping events
        with self.assertRaises(ValueError) as context:
            validate_no_overlap(start, end)

        print(f"Exception raised as expected: {context.exception}")

if __name__ == "__main__":
    unittest.main()