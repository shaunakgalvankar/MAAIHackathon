from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

documents = SimpleDirectoryReader("./pdfs").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("Tell me about the project")
print(response)