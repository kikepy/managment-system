from resources.staff.referees import Referee

def test_referee_assign_assistants():
    # Create referees
    referees = [
        Referee("John", "futsal", "high"),
        Referee("Mike", "futsal", "mid"),
        Referee("Alice", "basketball", "mid"),
        Referee("Bob", "futsal", "low"),
        Referee("Karen", "basketball", "high"),
        Referee("Tom", "volleyball", "mid"),
        Referee("Jerry", "volleyball", "low"),
        Referee("Anna", "volleyball", "high"),
        Referee("Luis", "futsal", "low"),
        Referee("Eva", "basketball", "low"),
        Referee("Sam", "volleyball", "mid"),
        Referee("Sergio", "futsal", "low"),
    ]

    # Assign assistants
    Referee.assign_assistants(referees)

    # Verify results
    for referee in referees:
        if referee.assistants:  # Check if the referee has assistants
            print(f"Referee: {referee.name}, Sport: {referee.sport}, Certification: {referee.certification_level}")
            print(f"Assigned Assistants: {referee.assistants}")
            print(f"Required Assistants: {referee.required_assistants}")
            print("-" * 50)

if __name__ == "__main__":
    test_referee_assign_assistants()