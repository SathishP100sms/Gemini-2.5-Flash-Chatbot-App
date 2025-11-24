from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
import os

# --- Configuration and Initialization ---

# 1. Load environment variables from .env file
load_dotenv()

# 2. Configure Streamlit page settings
# Note: You need a modern Streamlit version (>=0.65.0) for st.set_page_config
st.set_page_config(
    page_title="Gemini 2.5 Flash Chatbot",
    page_icon=":gem:", # Title Emojis
    layout="centered"
)

# --- Functions ---

# Helper function to clear the chat history
def clear_chat_history():
    # Reset the history in the chat session
    st.session_state.chat_session.history = []
    # Reinitialize the chat session
    st.session_state.chat_session = model.start_chat(history=[])

# Maps the Gemini SDK role ('model') to the Streamlit role ('assistant')
def role(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# --- Main App Logic ---

# Get the API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY environment variable not found. Please set it in your .env file.")
    st.stop()

# Configure the Generative AI client
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    MODEL_NAME = "gemini-2.5-flash"
    model = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
    st.error(f"Error configuring Google GenAI: {e}")
    st.stop()

# --- HEADER and CONTROLS (Column Layout) ---

# Use columns for a centered and modern header look
col1, col2 = st.columns([3, 1])

with col1:
    st.title(":sparkles: Gemini 2.5 Flash Chat")

with col2:
    # Clear Button: Adding a stylized button to clear the chat
    st.button("Clear Chat :broom:", on_click=clear_chat_history)

st.markdown("---") # Visual separator

# --- Chat Session Management ---

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# --- Display History ---

for message in st.session_state.chat_session.history:
    with st.chat_message(role(message.role)):
        st.markdown(message.parts[0].text)

# --- User Input and Response Generation ---

# Clean Input Prompt: Setting the friendly prompt text
prompt = st.chat_input("Ask anything! I'm Gemini 2.5 Flash.")

if prompt:
    st.chat_message("user").markdown(prompt)
    
    with st.spinner("🤖 Thinking..."):
        try:
            gemini_response = st.session_state.chat_session.send_message(prompt)
            
            with st.chat_message("assistant"):
                st.markdown(gemini_response.text)
                
        except Exception as e:
            st.error(f"An error occurred while getting the response: {e}")