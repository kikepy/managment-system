import unittest
from datetime import datetime, timedelta
from events.friendly_match import FriendlyMatch
from events.official import OfficialMatch
from events.tournament import Tournament

class TestEventTypes(unittest.TestCase):
    def test_friendly_match(self):
        start = datetime.now() + timedelta(days=1)
        teams = ["Team A", "Team B"]
        match = FriendlyMatch("Friendly Match", start, "Stadium A", "futsal", teams)
        self.assertEqual(match.teams, teams)

    def test_official_match(self):
        start = datetime.now() + timedelta(days=1)
        referee = {"level": "high"}
        commentators = ["Commentator 1", "Commentator 2"]
        match = OfficialMatch("Official Match", start, "Stadium B", "basketball", referee, "League", commentators)
        self.assertEqual(match.referee, referee)

    def test_tournament(self):
        start = datetime.now() + timedelta(days=1)
        teams = ["Team A", "Team B", "Team C", "Team D"]
        tournament = Tournament("Tournament", start, "Stadium C", "volleyball", teams, "knockout")
        self.assertEqual(tournament.format, "knockout")

if __name__ == "__main__":
    unittest.main()