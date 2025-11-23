class InMemorySessionService:
    """
    Manages the conversation history and user preferences.
    """
    def __init__(self):
        self.history = []
        self.user_profile = {
            "dietary_restrictions": [],
            "dislikes": [],
            "current_energy_level": "Medium",
            "region": "Global" # Default
        }

    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "parts": [content]})

    def update_profile(self, key, value):
        self.user_profile[key] = value

    def get_context_string(self):
        """
        Compacts the profile into a string for the LLM system prompt.
        """
        # We add 'Location/Region' here so the Chef sees it automatically
        return f"""
        [USER CONTEXT]
        Location/Region: {self.user_profile['region']}
        Diet: {', '.join(self.user_profile['dietary_restrictions'])}
        Current Energy Level: {self.user_profile['current_energy_level']}
        """