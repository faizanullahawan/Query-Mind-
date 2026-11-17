# AI SQL Agent (QUERY MIND):

An AI-powered SQL agent that converts natural-language questions into MySQL queries using **Groq LLM, LangGraph, LangChain, and FastAPI**.

Ask questions about your database in plain English and receive generated SQL queries without manually writing SQL.

## Project Overview

AI SQL Agent connects to a MySQL database, inspects its schema, and uses an LLM to generate SQL queries based on the user's questions.

For example:

**User question:**
```text
Show the best-selling products.
```

**Generated SQL:**
```sql
SELECT product_name, SUM(quantity) AS total_sold
FROM sales_data
GROUP BY product_name
ORDER BY total_sold DESC;
```

*Example output only. The actual generated query depends on your database schema.*

## Features

- Natural-language-to-SQL generation
- MySQL database connectivity
- Automatic database schema inspection
- Groq-powered LLM integration
- LangGraph workflow orchestration
- SQL validation before returning results
- FastAPI backend
- HTML, CSS, and JavaScript frontend
- Interactive SQL generation interface
- Database schema inspection endpoint

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core development |
| Groq API | LLM inference |
| LangChain | LLM integration |
| LangGraph | Agent workflow |
| MySQL | Database |
| SQLAlchemy | Database connectivity |
| FastAPI | Backend API |
| HTML | Frontend structure |
| CSS | Frontend styling |
| JavaScript | Frontend functionality |

## Architecture

```text
User
  |
  v
Frontend (HTML, CSS, JavaScript)
  |
  v
FastAPI Backend
  |
  v
LangGraph Workflow
  |
  +--> Inspect Database Schema
  |
  +--> Generate SQL using Groq
  |
  +--> Validate Generated SQL
  |
  v
Return SQL Query to Frontend
```

## Project Structure

```text
AI-SQL-Agent/
│
├── connection.py
├── schema_inspector.py
├── llm.py
├── sql_generator.py
├── graph.py
├── main.py
│
├── index.html
├── style.css
├── script.js
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-sql-agent.git
cd ai-sql-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

Use `.env.example` as a template:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=Companydata

GROQ_API_KEY=your_groq_api_key
```

Replace the example values with your own database credentials and Groq API key.

**Never upload your actual `.env` file to GitHub.**

### 5. Start the application

Run the FastAPI server:

```bash
uvicorn main:app --reload
```

Open the application:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

## How It Works

1. The user enters a question in natural language.
2. FastAPI receives the question.
3. LangGraph starts the agent workflow.
4. The schema inspector retrieves the database schema.
5. Groq generates an SQL query using the question and schema.
6. The validation node checks the generated SQL.
7. The backend returns the generated query and validation status.
8. The frontend displays the result.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Opens the frontend |
| GET | `/api/schema` | Retrieves database schema |
| POST | `/api/generate-sql` | Generates and validates SQL |
| GET | `/docs` | FastAPI API documentation |

### Example API Request

`POST /api/generate-sql`

```json
{
  "question": "Show the best-selling products"
}
```

### Example API Response

```json
{
  "question": "Show the best-selling products",
  "sql": "SELECT ...",
  "is_valid": true,
  "validation_error": null
}
```

## Current Limitations

- The current version generates and validates SQL but does not execute queries.
- SQL validation is basic and should be strengthened before production use.
- Database credentials and API keys must be configured locally.
- The application currently supports MySQL.

## Future Improvements

- Safe SQL query execution
- Display database results in the frontend
- Interactive charts and visualizations
- Query history
- Improved SQL security and validation
- Support for additional databases
- AI-powered data analysis

## Author

**Muhammad Faizan Ullah**

Computer Science Student | AI Engineer in Progress

GitHub: https://github.com/faizanullahawan

---

**Project:** AI SQL Agent  
**Status:** Development
