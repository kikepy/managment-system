import unittest
from datetime import datetime, timedelta
from events.validation import (
    validate_no_overlap,
    add_event_to_schedule,
    validate_date_and_hours,
    validate_tournament,
    validate_friendly,
    validate_official,
    validate_training,
    existing_events
)

class TestValidation(unittest.TestCase):
    def setUp(self):
        # Clear the existing events before each test
        existing_events.clear()

    def test_validate_no_overlap(self):
        start1 = datetime(2023, 12, 1, 10, 0)
        end1 = datetime(2023, 12, 1, 12, 0)
        start2 = datetime(2023, 12, 1, 11, 0)
        end2 = datetime(2023, 12, 1, 13, 0)

        existing_events.append({"name": "Event 1", "start": start1, "end": end1})

        with self.assertRaises(ValueError) as context:
            validate_no_overlap(start2, end2)
        self.assertEqual(str(context.exception), "The new event overlaps with an existing event.")

    def test_add_event_to_schedule(self):
        start = datetime(2023, 12, 1, 10, 0)
        end = datetime(2023, 12, 1, 12, 0)

        add_event_to_schedule("Event 1", start, end)
        self.assertEqual(len(existing_events), 1)
        self.assertEqual(existing_events[0]["name"], "Event 1")

    def test_validate_date_and_hours(self):
        future_date = datetime.now() + timedelta(days=1)
        validate_date_and_hours(future_date, 8)  # Should not raise an exception

        with self.assertRaises(ValueError):
            validate_date_and_hours(datetime.now() - timedelta(days=1), 8)  # Past date

        with self.assertRaises(ValueError):
            validate_date_and_hours(future_date, 25)  # Invalid hours

    def test_validate_tournament(self):
        teams = ["Team A", "Team B", "Team C", "Team D"]
        resources = {"fields": 1}
        validate_tournament(teams, "knockout", resources=resources)  # Should not raise an exception

        with self.assertRaises(ValueError):
            validate_tournament(teams, "invalid_format", resources=resources)  # Invalid format

        with self.assertRaises(ValueError):
            validate_tournament(teams[:2], "knockout", resources=resources)  # Not enough teams

        with self.assertRaises(ValueError):
            validate_tournament(teams, "knockout", resources={})  # No fields

    def test_validate_friendly(self):
        teams = ["Team A", "Team B"]
        resources = {"fields": 1}
        validate_friendly(teams=teams, resources=resources)  # Should not raise an exception

        with self.assertRaises(ValueError):
            validate_friendly(teams=["Team A"], resources=resources)  # Not enough teams

        with self.assertRaises(ValueError):
            validate_friendly(teams=teams, resources={})  # No fields

    def test_validate_official(self):
        referee = {"level": "high"}
        commentators = ["Commentator 1", "Commentator 2"]
        resources = {"fields": 1}
        validate_official(referee=referee, commentators=commentators, resources=resources)  # Should not raise an exception

        with self.assertRaises(ValueError):
            validate_official(referee={"level": "low"}, commentators=commentators, resources=resources)  # Low-level referee

        with self.assertRaises(ValueError):
            validate_official(referee=referee, commentators=["Commentator 1"], resources=resources)  # Not enough commentators

        with self.assertRaises(ValueError):
            validate_official(referee=referee, commentators=commentators, resources={})  # No fields

    def test_validate_training(self):
        trainer = {"name": "Trainer A"}
        resources = {"equipment": 1}
        validate_training(trainer=trainer, resources=resources)  # Should not raise an exception

        with self.assertRaises(ValueError):
            validate_training(trainer=None, resources=resources)  # No trainer

        with self.assertRaises(ValueError):
            validate_training(trainer=trainer, resources={})  # No equipment

if __name__ == "__main__":
    unittest.main()