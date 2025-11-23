from datetime import datetime, timedelta


def fetch_todays_events(simulate_busy_day: bool = False) -> list:
    """
    Simulates fetching events from Google Calendar API.
    """
    now = datetime.now()
    events = []

    if simulate_busy_day:
        # Simulate a nightmare schedule
        events = [
            {"summary": "Team Standup", "start": now + timedelta(minutes=30), "duration": 30},
            {"summary": "Client Deep Dive", "start": now + timedelta(hours=1), "duration": 60},
            {"summary": "Project Review", "start": now + timedelta(hours=3), "duration": 45},
            {"summary": "Late Night Call", "start": now + timedelta(hours=5), "duration": 60}
        ]
    else:
        # Simulate a light day
        events = [
            {"summary": "Lunch with friend", "start": now + timedelta(hours=2), "duration": 60}
        ]

    return events


def calculate_free_slots(events: list) -> int:
    """
    Analyzes the events and calculates the largest chunk of free time in minutes.
    """
    # Simple logic for the simulation:
    # > 3 events = Busy (20 mins free)
    # < 3 events = Free (90 mins free)
    if len(events) > 3:
        return 20
    elif len(events) > 1:
        return 45
    else:
        return 90