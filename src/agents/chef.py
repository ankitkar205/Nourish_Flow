from src.utils.llm_factory import LLMFactory
from src.tools.search_tool import search_recipes
from src.utils.logger import setup_logger  # Import Logger

logger = setup_logger("Chef_Agent")


class ChefAgent:
    def __init__(self):
        self.tools = [search_recipes]
        self.model = LLMFactory.create_model(tools=self.tools)
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def suggest_meal(self, time_constraints: dict, user_context: str, user_request: str, image_part=None) -> str:

        logger.info(f"Received request. Time limit: {time_constraints['allowed_minutes']}m")

        chef_prompt = f"""
        You are an expert Chef. 

        [CONSTRAINTS]
        Max Cooking Time: {time_constraints['allowed_minutes']} minutes.
        Energy Vibe: {time_constraints['energy_context']}
        User Profile: {user_context}

        [REQUEST]
        User wants: {user_request}

        TASK:
        1. Analyze ingredients (if image provided) and constraints.
        2. Suggest a meal. Use 'search_recipes' tool if needed.
        3. FORMATTING IS CRITICAL. You must use the following separators:

        === RECIPE ===
        (Put the recipe title, time, and instructions here)

        === SHOPPING LIST ===
        (Put a bulleted list of ingredients user needs to buy or use)
        """

        logger.info("Thinking about recipes...")
        if image_part:
            response = self.chat.send_message([chef_prompt, image_part])
        else:
            response = self.chat.send_message(chef_prompt)

        logger.info("Recipe generated.")
        return response.text