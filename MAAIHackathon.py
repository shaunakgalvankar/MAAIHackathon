import streamlit as st

# Initialize session state
if 'role' not in st.session_state:
    st.session_state['role'] = None
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Function to display chat interface
def chat_interface():
    st.sidebar.markdown(f"**Role:** {st.session_state['role']}")
    st.header("Chat")
    
    for msg in st.session_state['messages']:
        if msg['sender'] == 'user':
            st.markdown(f"**You:** {msg['text']}")
        else:
            st.markdown(f"**Bot:** {msg['text']}")
    
    user_input = st.text_input("You:", key="input")
    if user_input:
        st.session_state['messages'].append({"sender": "user", "text": user_input})
        # Placeholder for bot response
        bot_response = "This is a response."
        st.session_state['messages'].append({"sender": "bot", "text": bot_response})
    
    if st.button("Back"):
        st.session_state['role'] = None
        st.session_state['messages'] = []

# Main app
def main():
    if st.session_state['role'] is None:
        st.title("Choose Your Role")
        col1, col2 = st.columns(2)
        if col1.button("Mentor"):
            st.session_state['role'] = 'Mentor'
            st.session_state['messages'] = []
        if col2.button("Mentee"):
            st.session_state['role'] = 'Mentee'
            st.session_state['messages'] = []
    else:
        chat_interface()

if __name__ == "__main__":
    main()