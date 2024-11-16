# main.py


# ingest.py
import streamlit as st
import os

import openai
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext, load_index_from_storage
from llama_index.llms.openai import OpenAI

def ingest():
    # Check if index already exists
    if os.path.exists("./storage"):
        # Load existing index
        storage_context = StorageContext.from_defaults(persist_dir="./storage")
        index = load_index_from_storage(storage_context)
    else:
        # Load and process documents
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        
        # Configure LLM settings
        Settings.llm = OpenAI(
            model="gpt-3.5-turbo",
            temperature=0.2,
            system_prompt="""Role:
You are an expert in matching VCs with startups.  You are given a information about startups. You will always be truthful about the response, if you do not know, you should say I don’t know. Do not use information that is not provided in the startup information.

Action:
You will think step by step and explain your choices.

Problem:

            You are an expert in matching VCs with startups. 
            You are given a startup and a VC and you need to match them based on their interests and expertise."""
        )
        
        # Create new index
        index = VectorStoreIndex.from_documents(docs)
        
        # Save index to disk
        index.storage_context.persist("./storage")
    
    return index
    
# chat.py

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