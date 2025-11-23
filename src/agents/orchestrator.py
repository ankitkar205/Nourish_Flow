from src.utils.memory import InMemorySessionService
from src.agents.scheduler import SchedulerAgent
from src.agents.chef import ChefAgent


class OrchestratorAgent:
    def __init__(self):
        self.scheduler = SchedulerAgent()
        self.chef = ChefAgent()
        self.memory = InMemorySessionService()

    def process_request(self, user_input: str, image_parts=None, simulate_busy=False):
        """
        Orchestrates the flow: Scheduler -> Chef
        """

        # 1. Retrieve Context
        current_energy = self.memory.user_profile["current_energy_level"]
        user_context = self.memory.get_context_string()

        # 2. Call Scheduler Agent (Pass the busy flag)
        time_constraints = self.scheduler.analyze_constraints(current_energy, simulate_busy)

        # 3. Call Chef Agent
        response_text = self.chef.suggest_meal(
            time_constraints=time_constraints,
            user_context=user_context,
            user_request=user_input,
            image_part=image_parts
        )

        # 4. Update History
        self.memory.add_message("user", user_input)
        self.memory.add_message("assistant", response_text)

        return response_text

    def update_user_state(self, energy_level, diet, region):
        """Called by the UI to update state"""
        self.memory.update_profile("current_energy_level", energy_level)
        self.memory.update_profile("dietary_restrictions", diet)
        self.memory.update_profile("region", region) # Save the region