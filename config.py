import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    API_KEY = os.getenv("GOOGLE_API_KEY")

    # We use Flash for speed and tool calling, Pro is available if we need deep reasoning
    MODEL_NAME = "gemini-2.0-flash"

    # System instructions for the main agent
    SYSTEM_INSTRUCTION = """
    You are NourishFlow, an elite Concierge Meal Planning Agent.
    Your goal is to plan meals based on the user's ENERGY LEVEL and AVAILABLE INGREDIENTS.

    1. Analyze the user's request and context.
    2. If they are 'Low Energy', suggest quick, minimal-cleanup meals (under 15 mins).
    3. If they are 'High Energy', suggest adventurous, gourmet meals.
    4. ALWAYS prioritize ingredients they already have (reduce waste).
    5. You have access to tools. Use them when necessary.
    """