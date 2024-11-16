# main.py


# ingest.py
import streamlit as st
import openai
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.openai import OpenAI

def ingest():
    # Set up Streamlit page configuration
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
    
    @st.cache_resource(show_spinner=False)
    def load_data():
        # Load and process documents
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        
        # Configure LLM settings
        Settings.llm = OpenAI(
            model="gpt-3.5-turbo",
            temperature=0.2,
            system_prompt="""You are an expert mentor matching assistant. 
            Your role is to help connect mentors and mentees based on their 
            skills, interests, and goals. Provide detailed, relevant matches 
            and maintain a professional and supportive tone throughout the 
            conversation."""
        )
        
        # Create and return index
        index = VectorStoreIndex.from_documents(docs)
        return index
    
    index = load_data()
    return index

# chat.py
import streamlit as st

def start_chat(index):
    # Initialize chat engine if not in session state
    if "chat_engine" not in st.session_state:
        st.session_state.chat_engine = index.as_chat_engine(
            chat_mode="condense_question",
            verbose=True,
            streaming=True
        )
    
    # Get user input
    prompt = st.chat_input("How can I help you find a mentor/mentee?")
    
    # Process user input if provided
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Generate and display assistant response if last message was from user
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            response_stream = st.session_state.chat_engine.stream_chat(prompt)
            st.write_stream(response_stream.response_gen)
            message = {"role": "assistant", "content": response_stream.response}
            st.session_state.messages.append(message)