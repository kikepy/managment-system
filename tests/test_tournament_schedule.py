import unittest
from datetime import datetime, timedelta
from events.tournament import Tournament

class TestCreateSchedule(unittest.TestCase):
    def setUp(self):
        self.start_date = datetime.now() + timedelta(days=1)  # Always set to tomorrow
        self.teams = ["Team A", "Team B", "Team C", "Team D"]

    def test_consecutive_schedule(self):
        tournament = Tournament(
            name="Consecutive Tournament",
            date=self.start_date,
            location="Stadium A",
            sport="soccer",
            teams=self.teams,
            format="round-robin",
            schedule_format="consecutive"
        )
        # Verifica que el calendario tenga la cantidad correcta de días consecutivos
        self.assertEqual(len(tournament.schedule), 2)  # Updated to match calculated total_days
        self.assertEqual(tournament.schedule[0], self.start_date)
        self.assertEqual(tournament.schedule[1], self.start_date + timedelta(days=1))

    def test_custom_intervals_schedule(self):
        tournament = Tournament(
            name="Custom Intervals Tournament",
            date=self.start_date,
            location="Stadium C",
            sport="soccer",
            teams=self.teams,
            format="round-robin",
            schedule_format="custom_intervals"
        )
        # Verifica que el calendario se genere con intervalos personalizados (cada 2 días)
        self.assertEqual(len(tournament.schedule), 2)  # Updated to match calculated total_days
        self.assertEqual(tournament.schedule[0], self.start_date)
        self.assertEqual(tournament.schedule[1], self.start_date + timedelta(days=2))

    def test_specific_days_schedule(self):
        tournament = Tournament(
            name="Specific Days Tournament",
            date=self.start_date,
            location="Stadium B",
            sport="soccer",
            teams=self.teams,
            format="round-robin",
            specific_days=[4, 5],  # Jueves y Viernes
            schedule_format="specific_days"
        )
        # Verifica que el calendario se genere solo en los días específicos
        self.assertGreaterEqual(len(tournament.schedule), 1)
        for day in tournament.schedule:
            self.assertIn(day.weekday(), [4, 5])  # Jueves o Viernes

    
if __name__ == "__main__":
    unittest.main()