# NBEDirectivesAssist

## Problem Statement:
Ethiopian banks employees frequently face challenges in staying up-to-date with the directives and regulations issued by the National Bank of Ethiopia (NBE) the central bank. These directives cover critical areas like compliance, risk management, and operational guidelines, and failing to comply results in penalties, reputational damage, and operational risks. The current method of accessing and interpreting directives is inefficient, often requiring manual searches of documents from National Bank of Ethiopia website, leading to delays, miscommunication, and inconsistent application across departments. This lack of immediate access to regulatory information exposes banks to compliance risks, reduces productivity and affects banks operational efficency.
## Solution: RAG System for Directives(NBEDirectivesAssist)
A Retrieval-Augmented Generation (RAG) system will address these challenges by providing an AI-powered question answering system that allows bank employees to ask questions about NBE directives and receive accurate, up-to-date answers instantly. This system will:
1. Centralize Regulatory Information: Create a single, accessible knowledge base for all NBE directives, making it easy for employees to find and interpret the latest regulations.
2. Improve Compliance: By delivering instant answers about regulations, the system ensures that employees stay informed about compliance requirements, reducing the risk of non-compliance and associated penalties.
3. Boost Operational Efficiency: Employees can quickly retrieve answers to complex regulatory questions without needing to search lengthy documents or depend on legal teams, saving time and resources.
4. Ensure Consistency: The system provides consistent, accurate responses across departments, preventing misinterpretation and ensuring uniform application of directives.
5. Democratize Knowledge: With easy access to directives, the RAG system reduces dependency on key personnel and ensures that every employee, from compliance officers to front-line staff, is equipped with the latest regulatory knowledge.
## Features
- **Objective**: Conduct in-depth customer segmentation using RFMS (Recency, Frequency, Monetary Value, and Standard Deviation of Amount Spent) scores.

**RAG Flow: The application employs a hybrid RAG flow that integrates both a knowledge base (Elasticsearch) and a Large Language Model (LLM) for query rewriting and response generation.
**Retrieval Evaluation: Multiple retrieval approaches are implemented and evaluated in this project:
****BM25: Traditional term-based retrieval method.
****Dense Vector Search: Semantic retrieval using sentence transformers.
****Hybrid Search: Combines BM25 and dense vector search, ensuring that the most relevant retrieval method is utilized for each query.
The application dynamically selects the best retrieval method based on query characteristics.
**RAG Evaluation: The project includes evaluations of multiple RAG approaches, such as various query rewriting techniques and prompt designs.
**Automated Ingestion Pipeline: The system includes a fully automated ingestion pipeline that ingests documents into the Elasticsearch knowledge base. Users can upload documents directly from the interface, and the pipeline automatically indexes them for retrieval.
**Monitoring and Feedback Collection: The application integrates Prometheus to monitor various metrics, including response times and retrieval performance. It also collects user feedback on response quality.
**Containerization: The entire application is containerized with Docker, including a docker-compose.yml file that orchestrates both the Streamlit application and Elasticsearch services. 
**Best Practices: The application incorporates several advanced techniques:
****Hybrid Search: Combines BM25 and dense vector search to maximize retrieval accuracy.
****Document Re-ranking: prioritizes retrieved documents based on relevance before displaying them to the user.
****User Query Rewriting: Utilizes the t5-base model to rewrite queries for improved retrieval precision and relevance.

