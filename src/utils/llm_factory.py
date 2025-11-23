import google.generativeai as genai
from config import Config

class LLMFactory:
    @staticmethod
    def create_model(tools=None):
        """
        Initializes the Gemini Model with optional tools.
        """
        if not Config.API_KEY:
            raise ValueError("API Key not found! Check your .env file.")

        genai.configure(api_key=Config.API_KEY)

        model = genai.GenerativeModel(
            model_name=Config.MODEL_NAME,
            system_instruction=Config.SYSTEM_INSTRUCTION,
            tools=tools # Inject tools here for the agent to use
        )
        return model