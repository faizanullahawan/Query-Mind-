
import re

from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from schema_inspector import get_database_schema
from sql_generator import generate_sql


# ==========================================
# 1. GRAPH STATE
# ==========================================

class AgentState(TypedDict, total=False):
    question: str
    schema: dict
    sql: str
    is_valid: bool
    validation_error: str


# ==========================================
# 2. NODE: INSPECT DATABASE SCHEMA
# ==========================================

def inspect_schema_node(state: AgentState):

    print("\n[Node 1] Inspecting database schema...")

    schema = get_database_schema()

    if not schema:
        raise RuntimeError("Database schema is empty.")

    print("Schema inspection completed.")

    return {
        "schema": schema
    }


# ==========================================
# 3. NODE: GENERATE SQL
# ==========================================

def generate_sql_node(state: AgentState):

    print("\n[Node 2] Generating SQL with Groq...")

    question = state["question"]
    schema = state["schema"]

    sql = generate_sql(
        question=question,
        schema=schema
    )

    print("SQL generation completed.")

    return {
        "sql": sql
    }


# ==========================================
# 4. NODE: VALIDATE SQL
# ==========================================

def validate_sql_node(state: AgentState):

    print("\n[Node 3] Validating generated SQL...")

    sql = state.get("sql", "").strip()

    if not sql:
        return {
            "is_valid": False,
            "validation_error": "Empty SQL query."
        }

    # Only allow a SELECT statement
    if not re.match(r"^SELECT\b", sql, re.IGNORECASE):
        return {
            "is_valid": False,
            "validation_error": "Only SELECT queries are allowed."
        }

    # Remove one optional trailing semicolon
    cleaned_sql = sql.rstrip()

    if cleaned_sql.endswith(";"):
        cleaned_sql = cleaned_sql[:-1].rstrip()

    # Prevent multiple SQL statements
    if ";" in cleaned_sql:
        return {
            "is_valid": False,
            "validation_error": "Multiple SQL statements are not allowed."
        }

    # Block SQL comments
    if "--" in cleaned_sql or "/*" in cleaned_sql or "#" in cleaned_sql:
        return {
            "is_valid": False,
            "validation_error": "SQL comments are not allowed."
        }

    # Block modifying and dangerous operations
    forbidden_keywords = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "REPLACE",
        "GRANT",
        "REVOKE",
        "CALL",
        "EXECUTE",
        "LOAD_FILE",
        "INTO OUTFILE",
        "INTO DUMPFILE",
        "FOR UPDATE",
        "LOCK TABLES"
    ]

    for keyword in forbidden_keywords:

        pattern = r"\b" + re.escape(keyword) + r"\b"

        if re.search(pattern, cleaned_sql, re.IGNORECASE):
            return {
                "is_valid": False,
                "validation_error": f"Forbidden SQL operation: {keyword}"
            }

    print("SQL validation completed successfully.")

    return {
        "is_valid": True,
        "validation_error": ""
    }


# ==========================================
# 5. BUILD LANGGRAPH WORKFLOW
# ==========================================

workflow = StateGraph(AgentState)


# Register nodes
workflow.add_node("inspect_schema", inspect_schema_node)

workflow.add_node("generate_sql", generate_sql_node)

workflow.add_node("validate_sql", validate_sql_node)


# Connect edges
workflow.add_edge(START, "inspect_schema")

workflow.add_edge("inspect_schema", "generate_sql")

workflow.add_edge("generate_sql", "validate_sql")

workflow.add_edge("validate_sql", END)


# Compile graph
sql_agent = workflow.compile()


# ==========================================
# 6. TEST GRAPH
# ==========================================

if __name__ == "__main__":

    question = input("\nAsk your database: ")

    try:

        result = sql_agent.invoke({
            "question": question
        })

        print("\n========== AGENT RESULT ==========")

        print("\nGenerated SQL:")
        print(result.get("sql", "No SQL generated."))

        print("\nValidation Status:")
        print("VALID" if result.get("is_valid") else "INVALID")

        if result.get("validation_error"):
            print("\nValidation Error:")
            print(result["validation_error"])

    except Exception as error:

        print("\nAgent execution failed:")
        print(error)
