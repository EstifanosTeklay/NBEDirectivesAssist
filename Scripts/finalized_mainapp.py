import os
import time
import streamlit as st
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from prometheus_client import start_http_server, Summary

# Prometheus metric to track response times
RESPONSE_TIME = Summary('response_time_seconds', 'Time spent generating RAG response')

# Start Prometheus metric server on port 8000
start_http_server(8000)

# Elasticsearch client
es_client = Elasticsearch('http://localhost:9200')

# Load models
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')  # Dense model for vector search
query_rewriter = pipeline('text2text-generation', model='t5-base')     # Query rewriting model

# Evaluate multiple retrieval approaches
def elastic_search_bm25(query):
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
    return es_client.search(index="documents", body=search_query)

def elastic_search_tfidf(query):
    search_query = {
        "size": 5,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["content", "title", "section_title"],
                        "type": "most_fields"
                    }
                }
            }
        }
    }
    return es_client.search(index="documents", body=search_query)

def vector_search(query):
    query_vector = model.encode([query])[0]
    search_query = {
        "size": 5,
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                    "params": {"query_vector": query_vector}
                }
            }
        }
    }
    return es_client.search(index="documents", body=search_query)

# Hybrid search that combines BM25 and Dense vector search
def hybrid_search(query):
    bm25_results = elastic_search_bm25(query)
    dense_results = vector_search(query)
    combined_results = bm25_results['hits']['hits'] + dense_results['hits']['hits']
    return combined_results

# Re-rank documents (based on relevance score)
def re_rank_documents(documents):
    return sorted(documents, key=lambda x: x['_score'], reverse=True)

# Evaluate retrieval methods and return the best results
def evaluate_retrieval_methods(query):
    bm25_results = elastic_search_bm25(query)
    tfidf_results = elastic_search_tfidf(query)
    dense_results = vector_search(query)
    hybrid_results = hybrid_search(query)

    retrieval_evaluation = {
        'BM25': bm25_results,
        'TF-IDF': tfidf_results,
        'Dense': dense_results,
        'Hybrid': hybrid_results
    }

    # Choose the retrieval method with the most relevant results (highest number of hits)
    best_method = max(retrieval_evaluation, key=lambda x: retrieval_evaluation[x]['hits']['total']['value'])
    return retrieval_evaluation[best_method], best_method

# Rewrite user query for better relevance
def rewrite_query(query):
    rewritten_query = query_rewriter(f"paraphrase: {query}", max_length=50, num_return_sequences=1)
    return rewritten_query[0]['generated_text']

# Generate response with different prompts
def generate_response_with_prompt(prompt, retrieved_documents):
    context = " ".join([doc['_source']['content'] for doc in retrieved_documents['hits']['hits']])
    return f"{prompt}: {context}"

# Evaluate multiple RAG methods and return the best response
def evaluate_rag_methods(retrieved_documents):
    prompts = [
        "Summarize the key points from the retrieved documents",
        "Explain the topic in detail based on the documents",
        "Answer the question using the information from the documents"
    ]

    responses = [generate_response_with_prompt(prompt, retrieved_documents) for prompt in prompts]

    # For simplicity, we'll return the first response, but you can evaluate or rank them based on logic
    return responses[0] if responses else None

# Automated ingestion pipeline
def ingest_documents(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), 'r') as file:
                content = file.read()
                doc = {
                    'title': filename,
                    'content': content,
                    'timestamp': time.time()
                }
                es_client.index(index="documents", body=doc)
    print(f"Documents from {folder_path} ingested successfully.")

# Streamlit app
def main():
    st.title("Retrieval Augmented Generation (RAG) System with Hybrid Search")

    # Automated document ingestion
    if st.button("Ingest Documents"):
        ingest_documents('./documents')
        st.success("Documents ingested successfully!")

    # Query input
    query = st.text_input("Enter your search query")
    if st.button("Search"):
        start_time = time.time()

        # Step 1: Rewrite the query
        rewritten_query = rewrite_query(query)
        st.write(f"Rewritten Query: {rewritten_query}")

        # Step 2: Evaluate retrieval methods and select the best one
        best_retrieval, best_method = evaluate_retrieval_methods(rewritten_query)
        st.write(f"Best Retrieval Method: {best_method}")

        # Step 3: Re-rank documents
        re_ranked_documents = re_rank_documents(best_retrieval['hits']['hits'])

        # Step 4: Evaluate RAG methods and get the best response
        best_response = evaluate_rag_methods(best_retrieval)

        end_time = time.time()
        RESPONSE_TIME.observe(end_time - start_time)

        # Display the best response
        st.write(f"Best Response: {best_response}")
        st.write(f"Search took: {end_time - start_time:.2f} seconds")

        # Step 5: Collect user feedback
        feedback = st.radio("How satisfied are you with this response?", options=["1", "2", "3", "4", "5"], index=4)
        if st.button("Submit Feedback"):
            feedback_data = {
                'query': query,
                'response': best_response,
                'feedback': feedback,
                'timestamp': time.time()
            }
            es_client.index(index="feedback", body=feedback_data)
            st.success("Thank you for your feedback!")

if __name__ == "__main__":
    main()
