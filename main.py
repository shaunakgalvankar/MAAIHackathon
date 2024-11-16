# streamlit run main.py
import streamlit as st
from chat import ingest, start_chat

# Initialize session state
if 'role' not in st.session_state:
    st.session_state['role'] = None
if 'messages' not in st.session_state:
    st.session_state['messages'] = []


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
