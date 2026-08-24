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
    api_key = st.text_input("Gemini API Key:", type="password", key="gemini_key")
    
    persona = st.selectbox(
        "Select Architecture / Persona:",
        (
            "General Vision & Insight",
            "Engineering & First-Principles Solver",
            "Chanakya Strategic Advisor",
            "Tech Architect & Code Lead",
            "Veda Scholar (Ancient Science & Math)"
        )
    )
    
    include_sanskrit = st.checkbox("Include Sanskrit Shloka / Axiom", value=True)
    uploaded_file = st.file_uploader("Upload Problem/Diagram (Optional)", type=["png", "jpg", "jpeg"])
    clear_btn = st.button("Clear Conversation")

system_prompts = {
    "General Vision & Insight": "You are a versatile, insightful AI assistant. Describe and analyze uploaded images, documents, and user queries clearly, accurately, and naturally in plain language.",
    "Engineering & First-Principles Solver": "You are a Lead Engineer and Applied Physicist. Break down problems using first-principles reasoning, clean derivations, physical constraints, and system tradeoffs.",
    "Chanakya Strategic Advisor": "You are Chanakya, the master strategist. Provide disciplined, highly tactical, analytical advice rooted in strategic execution.",
    "Tech Architect & Code Lead": "You are a Principal Software Architect. Focus on robust algorithms, distributed systems, clean code standards, and production-grade software design.",
    "Veda Scholar (Ancient Science & Math)": "You are a scholar bridging ancient Indian mathematics (Aryabhata, Bhaskara, Madhava) with modern scientific discovery."
}

chosen_instruction = system_prompts.get(persona, "You are a helpful AI assistant.")
if include_sanskrit:
    chosen_instruction += " At the very end of your response, always include a relevant Sanskrit verse/subhashita in Devanagari with an English translation and practical takeaway."

# Initialize chat history
if "messages" not in st.session_state or clear_btn:
    st.session_state.messages = []

# Display past chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Chat Input
user_input = st.chat_input("Ask VedaAI an engineering, vision, or strategy problem...")

if user_input:
    if not api_key:
        st.warning("⚠️ Please enter your Gemini API key in the left sidebar first!")
    else:
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("assistant"):
            response_container = st.empty()
            full_response = ""
            
            try:
                client = genai.Client(api_key=api_key.strip())
                
                contents_payload = [user_input]
                if uploaded_file is not None:
                    image_bytes = uploaded_file.getvalue()
                    contents_payload.append(
                        types.Part.from_bytes(data=image_bytes, mime_type=uploaded_file.type)
                    )

                config = types.GenerateContentConfig(
                    system_instruction=chosen_instruction,
                    temperature=0.7
                )
                
                response_stream = client.models.generate_content_stream(
                    model="gemini-3.6-flash",
                    contents=contents_payload,
                    config=config
                )
                
                for chunk in response_stream:
                    full_response += chunk.text
                    response_container.markdown(full_response + "▌")
                response_container.markdown(full_response)

                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                response_container.error(f"Error: {e}")