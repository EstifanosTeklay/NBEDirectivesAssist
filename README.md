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
## NBE Directives Assist Project Features
- RAG Flow: The application employs a hybrid RAG flow that integrates both a knowledge base (Elasticsearch) and a Large Language Model (LLM) for query rewriting and response generation.
- Retrieval Evaluation: Multiple retrieval approaches are implemented and evaluated in this project:
  1. BM25: Traditional term-based retrieval method.
  2. Dense Vector Search: Semantic retrieval using sentence transformers.
  3. Hybrid Search: Combines BM25 and dense vector search, ensuring that the most relevant retrieval method is utilized for each query.
The application dynamically selects the best retrieval method based on query characteristics.
- RAG Evaluation: The project includes evaluations of multiple RAG approaches, such as various query rewriting techniques and prompt designs.
- Automated Ingestion Pipeline: The system includes a fully automated ingestion pipeline that ingests documents into the Elasticsearch knowledge base. Users can upload documents directly from the interface, and the pipeline automatically indexes them for retrieval.
- Monitoring and Feedback Collection: The application integrates Prometheus to monitor various metrics, including response times and retrieval performance. It also collects user feedback on response quality.
- Containerization: The entire application is containerized with Docker, including a docker-compose.yml file that orchestrates both the Streamlit application and Elasticsearch services. 
- Best Practices: The application incorporates several advanced techniques:
  1. Hybrid Search: Combines BM25 and dense vector search to maximize retrieval accuracy.
  2. Document Re-ranking: prioritizes retrieved documents based on relevance before displaying them to the user.
  3. User Query Rewriting: Utilizes the t5-base model to rewrite queries for improved retrieval precision and relevance.
## Project Strcture
### Directories
- National Bank of Ethiopia Directive- Contains Source Documents of National Bank of Ethiopia in PDF format.
- ConvertedToJson-containes Json files of the Converted PDF Files.
- Notebooks-containes notebook files for different tasks specified below.
  1. minsearchimplementation.ipynb- Implementation of the RAG system using minsearch search engine
  2. minsearchmodularcode.ipynb- Modular Implementation of the RAG system using minsearch search engine
  3. PdfToJsonConversion.ipynb- Converts The source PDF files to Json files
  4. RagImplementationelasticsearch.ipynb-Implementation of the RAG system using ElasticSearch Vector Database
  5. RAGSemanticsearchImplementation.ipynb-Semantic Search Implementation of the RAG system.
 - Scripts- containes python scripts for main applications.
   1. mainapp.py - streamlit app with out contenerization
   2. finalized_mainapp.py - Contenerized application that contains all tasks.
## How to run the project
### Prerequisites
- Docker and Docker Compose installed on your system
- Download and run Elastic Search Vector DB
- Generate API keys from GROQ website and replace the API keys with your newly created APIS

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/EstifanosTeklay/NBEDirectivesAssist.git
   ```

2. Navigate to the project directory:
   ```bash
   cd NBEDirectivesAssist
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
#### Method 1(runing the mainapp with out contenerization)
4. run Elastic search and start the streamlit app:
   ```bash
  # CD Scripts
  # streamlit run mainapp.py
  # use username-bankuser and password-password123 and enjoy the Assistant.
   ```

 #### Method 2(running the Contenerized finlized main app)
Steps 
  ```bash
  # docker-compose up --build
  # docker-compose up
  # Go to the Streamlit app at http://localhost:8501
  # Open http://localhost:8000 in your browser to access the Prometheus dashboard
   ```
Running the Application
Method 1: Running the Main App without Containerization
Start Elasticsearch and the Streamlit application:

bash
Copy code
# Navigate to the project directory
cd Scripts
# Run the Streamlit app
streamlit run mainapp.py
Use the following credentials to access the Assistant:

Username: bankuser
Password: password123
Method 2: Running the Containerized Application
Build and run the application using Docker Compose:

bash
Copy code
docker-compose up --build
Alternatively, if the images are already built, start the application directly:

bash
Copy code
docker-compose up
Access the application:

Streamlit App: http://localhost:8501
Prometheus Dashboard: http://localhost:8000
### Troubleshooting Tips
- Elasticsearch Issues: If Elasticsearch fails to start, ensure Docker has sufficient memory allocated (at least 4GB).
- Port Conflicts: Make sure ports 9200, 8501, and 8000 are available. If not, update docker-compose.yml to use different ports.
- Document Ingestion Errors: Confirm the presence of documents in the ./documents folder and check file permissions.
 
