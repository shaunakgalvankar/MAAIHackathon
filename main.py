# streamlit run main.py
import streamlit as st
from chat import ingest, start_chat
import openai

# Initialize session state
if 'role' not in st.session_state:
    st.session_state['role'] = None
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

st.set_page_config(
    page_title="Chat with MAAI",
    page_icon="🦙",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None
)

# Set OpenAI API key
openai.api_key = st.secrets.openai_key

# Set page title and info
st.title("Find right mentor/Mentee💬🦙")
st.info("We connect you with the right mentor/Mentee", icon="📃")

# Initialize session state for messages if not exists
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I can help you find the right mentor or mentee. What are you looking for?"
        }
    ]
# Main app
def main(index ):
    if st.session_state['role'] is None:
        st.title("Choose Your Role")
        col1, col2 = st.columns(2)
        if col1.button("Mentor"):
            st.session_state['role'] = 'Mentor'
            st.session_state['messages'] = []
        if col2.button("Mentee"):
            st.session_state['role'] = 'Mentee'
            st.session_state['messages'] = []

if __name__ == "__main__":
    index = ingest()
    start_chat(index)
