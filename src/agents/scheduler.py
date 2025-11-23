from src.tools.calendar_tool import fetch_todays_events, calculate_free_slots
from src.utils.logger import setup_logger

logger = setup_logger("Scheduler_Agent")


class SchedulerAgent:
    def __init__(self):
        self.role = "Time Manager"

    def analyze_constraints(self, energy_level: str, simulate_busy: bool) -> dict:
        """
        Combines User Energy + Calendar Schedule to determine cooking time.
        """

        # 1. Check Calendar
        logger.info(f"Connecting to Calendar API... (Simulated: {simulate_busy})")
        events = fetch_todays_events(simulate_busy)
        calendar_minutes = calculate_free_slots(events)

        logger.info(f"Found {len(events)} events today. Max free slot: {calendar_minutes} mins.")

        # 2. Check Energy
        energy_minutes = {
            "Zombie": 10,
            "Low": 20,
            "Medium": 45,
            "High": 90
        }.get(energy_level, 30)

        # 3. The Logic: Take the LOWER of the two numbers.
        # If Energy is High (90) but Calendar is Busy (20), we only have 20.
        allowed_minutes = min(calendar_minutes, energy_minutes)

        logger.info(f"Final Decision: {allowed_minutes} minutes allowed.")

        return {
            "allowed_minutes": allowed_minutes,
            "energy_context": f"User Energy: {energy_level}. Schedule Load: {len(events)} events.",
            "schedule_summary": [e['summary'] for e in events]
        }