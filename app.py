import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="VedaAI - Intellect, Engineering & Wisdom",
    page_icon="🔱",
    layout="centered"
)

# Custom Obsidian & Saffron styling
st.markdown("""
<style>
.stApp { background-color: #0d0f12; color: #e6edf3; }
h1 { color: #ff9933 !important; font-family: 'Segoe UI', sans-serif; text-shadow: 0 0 10px rgba(255, 153, 51, 0.3); }
.stChatMessage { border-radius: 12px; border: 1px solid #2d333b; background-color: #161b22; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

st.title("🔱 VedaAI")
st.caption("Bridging Ancient Strategy, Engineering Rigor & State-of-the-Art AI")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Core Engine Settings")
    
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        api_key = st.text_input("Gemini API Key:", type="password", key="gemini_key")
    
    persona = st.selectbox(
        "Select Architecture / Persona:",
        (
            "General Vision & Insight",
            "Engineering & First-Principles Solver",
            "Chanakya Strategic Advisor",
            "Tech Architect & Code Lead"
        )
    )
    
    model_choice = st.selectbox(
        "Model Engine:",
        ("gemini-2.5-flash", "gemini-2.5-pro")
    )
    
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

PERSONA_PROMPTS = {
    "General Vision & Insight": "You are VedaAI, an intellectual assistant blending deep analytical clarity, high ambition, and strategic intuition.",
    "Engineering & First-Principles Solver": "You are VedaAI acting as a Lead Engineer. Break down all problems to first principles, physics, mathematics, and ruthless technical precision.",
    "Chanakya Strategic Advisor": "You are VedaAI channeling the strategic intellect of Chanakya. Provide sharp, pragmatic, realistic, and highly calculating tactical guidance.",
    "Tech Architect & Code Lead": "You are VedaAI as a Principal Software Architect. Write clean, production-ready, performant, and scalable code with concise explanations."
}

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("Ask VedaAI an engineering, vision, or strategy problem..."):
    if not api_key:
        st.warning("Please enter your Gemini API key in the left sidebar first!")
        st.stop()
        
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    try:
        client = genai.Client(api_key=api_key.strip())
        
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            response = client.models.generate_content_stream(
                model=model_choice,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=PERSONA_PROMPTS[persona]
                )
            )
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
    except Exception as e:
        st.error(f"Error: {e}")
