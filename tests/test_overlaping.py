from datetime import datetime, timedelta
from events.tournament import Tournament

def check_tournament_overlap(tournaments):
    schedules = {}  # Dictionary to store schedules by location
    for tournament in tournaments:
        print(f"Tournament: {tournament.name}, Schedule: {tournament.schedule}")  # Debugging
        location = tournament.location
        if location not in schedules:
            schedules[location] = set()
        for day in tournament.schedule:
            if day in schedules[location]:
                raise ValueError(f"Overlap detected for tournament '{tournament.name}' at '{location}' on {day}.")
            schedules[location].add(day)

def test_tournament_overlap():
    start_date = datetime.now() + timedelta(days=1)  # Set start date to tomorrow

    # Tournament 1: Consecutive days
    tournament1 = Tournament(
        name="Tournament 1",
        date=start_date,
        location="Stadium A",
        sport="volleyball",
        teams=["Team A", "Team B", "Team C", "Team D"],
        format="round-robin",
        schedule_format="consecutive"
    )

    # Tournament 2: Specific days (weekends)
    tournament2 = Tournament(
        name="Tournament 2",
        date=start_date,
        location="Stadium B",
        sport="basketball",
        teams=["Team E", "Team F", "Team G", "Team H"],
        format="knockout",
        specific_days=[5, 6],  # Saturdays and Sundays
        schedule_format="specific_days"
    )

    # Tournament 3: Overlapping with Tournament 1 at the same location
    tournament3 = Tournament(
        name="Tournament 3",
        date=start_date + timedelta(days=1),  # Overlaps with Tournament 1
        location="Stadium A",  # Same location as Tournament 1
        sport="soccer",
        teams=["Team I", "Team J", "Team K", "Team L"],
        format="knockout",
        schedule_format="consecutive"
    )

    try:
        check_tournament_overlap([tournament1, tournament2, tournament3])
        print("Test failed: Overlapping tournaments were not detected.")
    except ValueError as e:
        print(f"Test passed: {e}")

if __name__ == "__main__":
    test_tournament_overlap()