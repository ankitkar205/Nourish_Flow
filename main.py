import streamlit as st
from PIL import Image
from src.agents.orchestrator import OrchestratorAgent

# --- Page Config ---
st.set_page_config(
    page_title="NourishFlow Agent",
    page_icon="🥑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
    <style>
    .stChatMessage {border-radius: 15px; padding: 10px;}
    .stButton button {width: 100%; border-radius: 8px;}
    div[data-testid="stExpander"] {border: none; box-shadow: none;}
    </style>
    """, unsafe_allow_html=True)


# --- Helper Function ---
def parse_response(text):
    if "=== RECIPE ===" in text and "=== SHOPPING LIST ===" in text:
        parts = text.split("=== SHOPPING LIST ===")
        recipe_part = parts[0].replace("=== RECIPE ===", "").strip()
        shopping_part = parts[1].strip()
        return recipe_part, shopping_part
    return None, None


# --- Initialization ---
if "agent" not in st.session_state:
    st.session_state.agent = OrchestratorAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/avocado.png", width=80)
    st.title("NourishFlow")
    st.caption("Concierge Meal Planning Agent")

    st.divider()

    # 1. Profile
    st.subheader("👤 User Profile")

    # --- NEW: Region Selection ---
    region = st.text_input("🌍 Location / Region", value="India", help="Helps with local ingredients & measurements")

    energy_level = st.select_slider(
        "Current Energy Level",
        options=["Zombie", "Low", "Medium", "High"],
        value="Medium"
    )

    diet = st.multiselect(
        "Dietary Restrictions",
        ["Vegetarian", "Vegan", "Gluten-Free", "Keto", "Dairy-Free", "Nut-Free"],
        default=[]
    )

    # Update Agent Memory with Region
    st.session_state.agent.update_user_state(energy_level, diet, region)

    st.divider()

    # 2. Integrations
    st.subheader("🔌 Integrations")

    if "google_calendar_connected" not in st.session_state:
        st.session_state.google_calendar_connected = False

    simulate_busy = False

    if not st.session_state.google_calendar_connected:
        st.write("Connect your calendar to sync meal prep times.")
        if st.button("🗓️ Connect Google Calendar"):
            st.session_state.google_calendar_connected = True
            st.rerun()
    else:
        st.success("✅ Google Calendar Linked")
        with st.expander("⚙️ Connection Settings"):
            simulate_busy = st.toggle("Test Mode: Simulate Busy Day", value=False)
            if st.button("❌ Disconnect"):
                st.session_state.google_calendar_connected = False
                st.rerun()

    if simulate_busy:
        st.warning("⚠️ Heavy schedule detected. Cooking time reduced.")

    st.divider()

    st.caption(f"**Status:** Agent Active\n**Region:** {region}")
    if st.button("🧹 Clear History"):
        st.session_state.messages = []
        st.rerun()

# --- Main Interface ---

st.title("🥑 What's for dinner?")
st.markdown(f"Suggesting meals for **{region}** based on your energy & fridge.")

# Image Uploader
uploaded_file = st.file_uploader("📸 Snap your fridge (Optional)", type=["jpg", "jpeg", "png"])
image_part = None

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Fridge Context Uploaded", width=300)
    image_part = image

# Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        recipe, shopping = parse_response(message["content"])
        if recipe and shopping and message["role"] == "assistant":
            tab1, tab2 = st.tabs(["🍽️ Recipe", "🛒 Shopping List"])
            with tab1:
                st.markdown(recipe)
            with tab2:
                st.markdown(shopping)
                st.download_button(
                    label="📥 Download List",
                    data=shopping,
                    file_name="shopping_list.txt",
                    mime="text/plain",
                    key=f"btn_{hash(message['content'])}"
                )
        else:
            st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ex: I have paneer and 20 minutes..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("💡 Analyzing schedule & ingredients..."):
            try:
                response_text = st.session_state.agent.process_request(
                    prompt,
                    image_parts=image_part,
                    simulate_busy=simulate_busy
                )

                recipe, shopping = parse_response(response_text)

                if recipe and shopping:
                    tab1, tab2 = st.tabs(["🍽️ Recipe", "🛒 Shopping List"])
                    with tab1:
                        st.markdown(recipe)
                    with tab2:
                        st.markdown(shopping)
                        st.download_button(
                            label="📥 Download List",
                            data=shopping,
                            file_name="shopping_list.txt",
                            mime="text/plain"
                        )
                else:
                    st.markdown(response_text)

                st.session_state.messages.append({"role": "assistant", "content": response_text})

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")