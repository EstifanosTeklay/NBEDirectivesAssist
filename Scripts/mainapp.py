import os
import json
import streamlit as st
import time
from elasticsearch import Elasticsearch
from tqdm import tqdm
from streamlit.components.v1 import html
from groq import Groq

# Function to authenticate users
def authenticate_user(username, password):
    # Simple authentication logic, replace with a more secure mechanism
    # Can check against a database or API for user credentials
    if username == "awashuser" and password == "password123":
        return True
    else:
        return False

# Define Elasticsearch settings
es_client = Elasticsearch('http://localhost:9200')

def elastic_search(query):
    search_query = {
        "size": 5,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["content^10", "title", "section_title", "document_id"],
                        "type": "best_fields"
                    }
                }
            }
        }
    }

    response = es_client.search(index="directivesanalyi", body=search_query)
    result_docs = [hit['_source'] for hit in response['hits']['hits']]
    return result_docs

def build_prompt(query, search_results):
    prompt_template = """
You're National Bank of Ethiopia Directives assistant. Answer the QUESTION based on the CONTEXT from the directive document.
Use facts from the CONTEXT when answering the QUESTION.
If the CONTEXT does not contain the answer, Answer from your general knowledge.

QUESTION: {question}
CONTEXT: {context}
""".strip()

    context = ""
    for doc in search_results:
        context += f"section_id: {doc['section_id']}\nsection_title: {doc['section_title']}\npage_number: {doc['page_number']}\ncontent: {doc['content']}\ndocument_id: {doc['document_id']}\ntitle: {doc['title']}\n\n"

    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt

def llm(prompt):
    # Initialize Groq client
    client = Groq(api_key="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")

    # Get the answer from the LLM model
    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": prompt,
        }],
        model="llama3-8b-8192",
    )
    llm_answer = chat_completion.choices[0].message.content
    return llm_answer

def rag(query):
    search_results = elastic_search(query)
    prompt = build_prompt(query, search_results)
    answer = llm(prompt)
    return answer

# Streamlit app
def main():
    st.set_page_config(page_title="Awash Bank RAG Assistant", page_icon="🏦")
    
    # Define a logo for Awash Bank, you can use different logos for different pages
    st.sidebar.image("awash_bank_logo.png", width=200)
    
    # Authentication page
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.title("Awash Bank RAG Assistant Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate_user(username, password):
                st.session_state.authenticated = True
                st.success("Login successful!")
            else:
                st.error("Invalid credentials.")
        return
    
    # Main page after authentication
    st.title("Awash Bank RAG Assistant")
    
    # Display a different logo for the main page
    st.image(r"D:\NBEDirectivesAssist\awash_bank_main_logo.png", width=200)
    
    # User input for the query
    user_query = st.text_input("Ask a question about National Bank of Ethiopia directives:")
    
    # Button to ask the question
    if st.button("Ask"):
        if user_query:
            with st.spinner('Processing your query...'):
                # Call the RAG function and display the result
                result = rag(user_query)
                st.success("Here is the result:")
                st.write(result)
        else:
            st.error("Please enter a question.")

if __name__ == "__main__":
    main()
