### Problem Statement
**The Paradox of Choice and Decision Fatigue.**

We make approximately 35,000 decisions every day. By 6:00 PM, "decision fatigue" sets in. We stare at ingredients we bought days ago, realize we are too tired to look up a recipe, and end up ordering expensive takeout. This cycle leads to financial loss, significant food waste, and poor nutrition.

Current meal planning applications are **static**. They provide recipes, but they ignore the **context** of your life. A recipe app doesn't know that you had back-to-back meetings for six hours, that you are currently in a specific region (like India) where ingredient availability differs, or that you only have 15 minutes before your next call.

I built **NourishFlow** to solve this disconnect. It is a Context-Aware Concierge Agent that acts as a bridge between *what you want to eat* and *what you actually have the time and resources to cook*.

### Why agents?
A standard LLM chatbot or a static recipe search engine is insufficient for this problem because they lack **active reasoning** and **external awareness**.

Agents are the right solution because this specific use case requires a system that can:
1.  **Negotiate Constraints:** A user might say "I want a feast," but reality says "You have 20 minutes." An agent can autonomously detect this conflict via tools and override the request to provide a realistic solution.
2.  **Perceive Reality:** Using Multimodal Agents (Vision), the system can "see" what is actually in the fridge rather than relying on the user to type out a list.
3.  **Execute Tasks:** Unlike a chatbot that just talks, a Concierge Agent performs work. In this case, it parses unstructured culinary advice into a structured, downloadable shopping list, saving the user manual effort.

### What you created
I built **NourishFlow**, a **Sequential Multi-Agent System** powered by **Gemini 2.0 Flash**. The architecture is designed as a Hub-and-Spoke model to ensure modularity and distinct separation of concerns.

**The Architecture Breakdown:**

*   **The Orchestrator (The Brain):** This is the central router. It manages the **Session State (Memory)**, ensuring that user preferences (Dietary restrictions, Dislikes) and Context (Region/Location) persist throughout the interaction.
*   **The Scheduler Agent (The Logic):** This agent is responsible for "Time Management." It utilizes a custom **Calendar Tool**. It performs a logic check: It compares the user's self-reported "Energy Level" against their simulated "Calendar Schedule." It enforces the stricter of the two constraints (e.g., High Energy + Busy Calendar = Low Cooking Time).
*   **The Chef Agent (The Creative):** This agent receives the strict time constraints from the Scheduler. It utilizes **Gemini Vision** to analyze uploaded fridge photos and uses **Search Tools (DuckDuckGo)** to verify recipe steps and ensure cultural relevance based on the user's Region (e.g., suggesting Ghee instead of Butter if the region is India).

### Demo
*Please refer to the attached video for the live walkthrough.*

**The "Busy Professional" User Journey:**
1.  **Context Setup:** The user sets their region to **"India"** and their Energy Level to **"High"**.
2.  **Calendar Integration:** The user clicks "Connect Google Calendar." The **Scheduler Agent** detects a heavy meeting load (4+ events). It proactively warns the user and overrides their "High Energy" setting, enforcing a strict **20-minute cooking limit**.
3.  **Visual Input:** The user uploads a photo of their fridge containing Paneer and Spinach.
4.  **The Result:** The **Chef Agent** recognizes the ingredients and the time limit. Instead of suggesting a time-consuming "Palak Paneer" gravy, it generates a quick **"Paneer Bhurji" (Scramble)** recipe.
5.  **Actionable Output:** The UI renders a dedicated **"Shopping List" tab** with a **Download Button**, allowing the user to grab the missing ingredients text file instantly.

### The Build
I built this application using **Python 3.13** and **Streamlit** for the frontend interface.

**Key Technologies & Course Concepts Applied:**

*   **Gemini 2.0 Flash:** I selected this model specifically for its low latency and superior capabilities in Tool Calling and Vision processing.
*   **Multi-Agent System:** I implemented a class-based structure where the `Orchestrator` instance manages `Scheduler` and `Chef` sub-agents.
*   **Tooling:** Developed a custom Python-based Calendar Simulator to demonstrate logic flow without requiring judges to have OAuth credentials, and integrated `duckduckgo-search` for real-time recipe validation.
*   **Context Engineering:** Implemented "Context Compaction" in the `InMemorySessionService` to inject user profiles and regional settings invisibly into the system prompt.
*   **Observability:** Integrated `colorlog` to provide real-time, color-coded terminal logs, allowing visibility into the inter-agent communication and decision-making process.

### If I had more time, this is what I'd do
1.  **Production OAuth:** I would replace the Calendar Simulation tool with the actual Google Calendar API using a secure OAuth flow for live personal data integration.
2.  **Delivery Integration:** I would connect the "Shopping List" output to an API like Instacart or Blinkit, allowing the agent to not just *write* the list, but *order* the groceries for the user.
3.  **Voice Mode:** I would implement the Gemini Live API to create a "Hands-Free Cooking Mode," where the agent reads instructions step-by-step and listens for "Next step" commands while the user's hands are dirty.
