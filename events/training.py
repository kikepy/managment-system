from .event import Event
from .validation import validate_training

class TrainingSession(Event):
    def __init__(self, name, date, location, sport, trainer):
        validate_training(date=date, coach=trainer)  # Update the argument passed to validation
        super().__init__(name, date, location, sport)
        self.trainer = trainer  # Update the attribute name