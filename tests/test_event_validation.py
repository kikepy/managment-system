import unittest
from datetime import datetime, timedelta
from events.validation import add_event_to_schedule, existing_events

class TestEventValidation(unittest.TestCase):
    def setUp(self):
        # Clear the existing events before each test
        existing_events.clear()

    def test_add_non_overlapping_events(self):
        start1 = datetime(2023, 12, 1, 10, 0)
        end1 = datetime(2023, 12, 1, 12, 0)
        start2 = datetime(2023, 12, 1, 12, 30)
        end2 = datetime(2023, 12, 1, 14, 0)

        # Add first event
        add_event_to_schedule("Event 1", start1, end1)
        self.assertEqual(len(existing_events), 1)

        # Add second non-overlapping event
        add_event_to_schedule("Event 2", start2, end2)
        self.assertEqual(len(existing_events), 2)

    def test_add_overlapping_events(self):
        start1 = datetime(2023, 12, 1, 10, 0)
        end1 = datetime(2023, 12, 1, 12, 0)
        start2 = datetime(2023, 12, 1, 11, 0)
        end2 = datetime(2023, 12, 1, 13, 0)

        # Add first event
        add_event_to_schedule("Event 1", start1, end1)
        self.assertEqual(len(existing_events), 1)

        # Attempt to add overlapping event
        with self.assertRaises(ValueError) as context:
            add_event_to_schedule("Event 2", start2, end2)
        self.assertEqual(str(context.exception), "The new event overlaps with an existing event.")

    def test_add_event_with_same_time(self):
        start = datetime(2023, 12, 1, 10, 0)
        end = datetime(2023, 12, 1, 12, 0)

        # Add first event
        add_event_to_schedule("Event 1", start, end)
        self.assertEqual(len(existing_events), 1)

        # Attempt to add event with the same time
        with self.assertRaises(ValueError) as context:
            add_event_to_schedule("Event 2", start, end)
        self.assertEqual(str(context.exception), "The new event overlaps with an existing event.")

if __name__ == "__main__":
    unittest.main()