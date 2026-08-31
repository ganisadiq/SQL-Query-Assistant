# SQL Query Assistant

An AI-powered **Text-to-SQL assistant** that converts natural-language business questions into SQL queries using database schemas, documentation, **Retrieval-Augmented Generation (RAG)**, FAISS, Azure OpenAI, and Azure AI Foundry Agents.

The application allows users to interact with a database using natural language while retrieving relevant schema context before generating SQL, helping the LLM produce more accurate and schema-aware queries.

---

## Overview

Traditional SQL querying requires users to understand database schemas, table relationships, column names, and SQL syntax.

This project provides a natural-language interface for querying databases. Instead of manually writing SQL, users can ask questions such as:

> "Show me the top 5 customers by total order value."

The system retrieves the most relevant database schema and documentation using semantic search and provides that context to an Azure AI Agent, which generates the corresponding SQL query.

### Key Features

* Natural-language to SQL generation
* Retrieval-Augmented Generation (RAG)
* Semantic search using FAISS
* Embedding-based schema retrieval
* Azure OpenAI integration
* Azure AI Foundry Agents
* Function calling
* SQL Server schema integration
* Streamlit-based user interface
* Modular document ingestion and retrieval pipeline

---

## Architecture

                         ┌──────────────────────┐
                         │       User           │
                         │ Natural Language     │
                         │       Query          │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     Streamlit UI     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Azure AI Agent     │
                         │   + Function Calling │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Query Embedding    │
                         │   Azure Embeddings   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    FAISS Index       │
                         │ Semantic Retrieval   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │ Relevant Schema & Documentation│
                    │ Tables • Columns • Relationships│
                    │ Business Rules • SQL Guidance │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Azure AI Agent     │
                         │ Context-Aware SQL    │
                         │      Generation      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Generated SQL     │
                         └──────────────────────┘

---

## How It Works

### 1. User submits a question

The user enters a natural-language business question through the Streamlit interface.

Example:

```text
Show me the top 5 customers by total order value.
```

### 2. Query is converted into an embedding

The natural-language query is converted into a vector representation using an embedding model.

### 3. Relevant context is retrieved

The embedding is compared against the FAISS vector index to retrieve the most relevant schema and documentation chunks.

The retrieved context can contain information such as:

* Table names
* Column names
* Data types
* Relationships
* Business rules
* SQL usage guidelines

### 4. Context is provided to the Azure AI Agent

The retrieved information is passed to the Azure AI Agent through a function tool.

The agent is instructed to use the retrieved schema context when generating SQL and avoid using tables or columns that are not present in the available context.

### 5. SQL is generated

The Azure OpenAI model generates a SQL query based on:

* User's question
* Retrieved database schema
* Relevant documentation
* SQL generation instructions

### 6. SQL is displayed

The generated SQL query is returned to the Streamlit application and displayed to the user.

---

## Tech Stack

### Programming & Data

* **Python**
* **SQL**
* **SQL Server**
* **Pandas**
* **NumPy**

### AI & Machine Learning

* **Azure OpenAI**
* **Azure AI Foundry**
* **AI Agents**
* **Large Language Models (LLMs)**
* **Embeddings**
* **Retrieval-Augmented Generation (RAG)**
* **FAISS**
* **Semantic Search**

### Application

* **Streamlit**
* **Function Calling**

### Development

* **Git**
* **GitHub**
* **python-dotenv**

---

## Project Structure

```text
SQL-Query-Assistant/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── ...
│
├── storage/
│   └── faiss/
│       └── ...
│
└── src/
    │
    ├── agent.py
    ├── config.py
    ├── functions.py
    │
    ├── database/
    │   └── ...
    │
    ├── loaders/
    │   └── ...
    │
    ├── chunker/
    │   └── ...
    │
    ├── embeddings/
    │   └── ...
    │
    ├── indexing/
    │   └── ...
    │
    ├── retrieval/
    │   └── ...
    │
    └── models/
        └── ...
```

### Main Components

**`app.py`**
Streamlit application and user interface.

**`agent.py`**
Creates and configures the Azure AI Agent responsible for SQL generation.

**`functions.py`**
Contains the function tool used by the agent to retrieve relevant schema and documentation.

**`database/`**
Handles SQL Server connectivity and database schema operations.

**`loaders/`**
Loads documents and database-related information for the RAG pipeline.

**`chunker/`**
Splits source content into smaller chunks for embedding and retrieval.

**`embeddings/`**
Generates vector embeddings for documents and user queries.

**`indexing/`**
Builds the FAISS vector index from embedded documents.

**`retrieval/`**
Performs similarity search against the FAISS index.

---

## Example

### User Question

```text
Show me the top 5 customers by total order value.
```

### Retrieved Context

```text
Customers
- CustomerID
- CustomerName

Orders
- OrderID
- CustomerID
- OrderDate
- TotalAmount
```

### Generated SQL

```sql
SELECT TOP 5
    c.CustomerName,
    SUM(o.TotalAmount) AS TotalOrderValue
FROM Customers c
JOIN Orders o
    ON c.CustomerID = o.CustomerID
GROUP BY c.CustomerName
ORDER BY TotalOrderValue DESC;
```

The generated query is based on the schema information retrieved by the RAG pipeline rather than relying solely on the model's internal knowledge.

---

## RAG Pipeline

The project uses a Retrieval-Augmented Generation architecture to provide database-specific context to the language model.

```text
Database Schema / Documentation
              │
              ▼
          Load Data
              │
              ▼
          Chunk Data
              │
              ▼
      Generate Embeddings
              │
              ▼
        FAISS Vector Index
              │
              │
        User Question
              │
              ▼
      Generate Query Embedding
              │
              ▼
       Similarity Search
              │
              ▼
      Retrieve Top-K Chunks
              │
              ▼
       Azure AI Agent + LLM
              │
              ▼
         Generated SQL
```

This approach allows the model to use relevant database-specific information during SQL generation and reduces reliance on assumptions about the database schema.

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/ganisadiq/SQL-Query-Assistant.git
cd SQL-Query-Assistant
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

```text
PROJECT_ENDPOINT=your_azure_ai_project_endpoint
MODEL_DEPLOYMENT_NAME=your_model_deployment
EMBEDDING_MODEL=your_embedding_model
EMBEDDING_MODEL_ENDPOINT=your_embedding_endpoint
SQL_SERVER_CONNECTION_STRING=your_sql_server_connection_string
```

Replace the values with your own Azure and SQL Server configuration.

**Never commit your `.env` file or API keys to GitHub.**

### 5. Build the FAISS index

Before running the application, generate the embeddings and build the FAISS index using the project's indexing pipeline.

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## Environment Variables

| Variable                       | Description                                           |
| ------------------------------ | ----------------------------------------------------- |
| `PROJECT_ENDPOINT`             | Azure AI Foundry project endpoint                     |
| `MODEL_DEPLOYMENT_NAME`        | Azure OpenAI model deployment used for SQL generation |
| `EMBEDDING_MODEL`              | Embedding model used for vector generation            |
| `EMBEDDING_MODEL_ENDPOINT`     | Endpoint used for generating embeddings               |
| `SQL_SERVER_CONNECTION_STRING` | Connection string for SQL Server                      |

For public repositories, use placeholder values only.

---

## Limitations

* The current system focuses on **SQL generation** rather than automatically executing generated queries.
* SQL accuracy depends on the quality and completeness of the retrieved schema and documentation.
* The system may generate incorrect SQL for highly complex business logic or ambiguous questions.
* FAISS provides local vector similarity search and does not provide the full feature set of managed vector databases.
* The application currently requires Azure AI services and appropriate model deployments.
* Generated SQL should be reviewed before execution in a production environment.

---

## Future Improvements

* Add safe, read-only SQL execution against SQL Server.
* Implement SQL validation before execution.
* Add query result visualization using Pandas and Plotly.
* Add automated evaluation of SQL generation accuracy.
* Implement schema-aware semantic chunking.
* Add conversation history for multi-turn queries.
* Add support for multiple database systems.
* Add query explanation and optimization suggestions.
* Add automated testing for retrieval and SQL generation.
* Improve retrieval using hybrid search and metadata filtering.
* Add monitoring and logging for production usage.

---

## Skills Demonstrated

This project demonstrates practical experience with:

* SQL and relational databases
* Python-based data applications
* Natural Language Processing
* Large Language Models
* Retrieval-Augmented Generation
* Vector embeddings
* Semantic search
* FAISS
* AI agents
* Function calling
* Azure OpenAI
* Azure AI Foundry
* Streamlit
* Database schema retrieval
* Modular software architecture

---

## Author

**Gani Sadiq**

Data Analyst | Python | SQL | Power BI | AI/ML

GitHub:
https://github.com/ganisadiq

---

## License

This project is intended for educational and portfolio purposes.
