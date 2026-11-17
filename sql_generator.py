
# import json

# from llm import llm
# from schema_inspector import get_database_schema


# def generate_sql(question: str):
#     if not question.strip():
#         raise ValueError("Please provide a question.")

#     # Get the actual database structure
#     schema = get_database_schema()

#     if not schema:
#         raise RuntimeError("No database schema found.")

#     schema_text = json.dumps(schema, indent=2)

#     # Instructions for the AI model
#     prompt = f"""
# You are an expert MySQL query generator.

# Your task is to convert the user's natural language
# question into a valid MySQL SQL query.

# DATABASE SCHEMA:
# {schema_text}

# USER QUESTION:
# {question}

# RULES:
# 1. Use only tables and columns present in the schema.
# 2. Never invent table or column names.
# 3. Generate MySQL-compatible SQL.
# 4. Generate only SELECT queries.
# 5. Never generate INSERT, UPDATE, DELETE, DROP,
#    ALTER, TRUNCATE, CREATE, or other modifying queries.
# 6. Use appropriate JOIN, GROUP BY, ORDER BY,
#    and aggregate functions when required.
# 7. Return only the SQL query.
# 8. Do not include explanations or Markdown code blocks.
# """

#     response = llm.invoke(prompt)

#     sql_query = response.content.strip()

#     # Remove Markdown formatting if the model adds it
#     if sql_query.startswith("```"):
#         lines = sql_query.splitlines()

#         if lines[-1].strip() == "```":
#             lines = lines[1:-1]

#         sql_query = "\n".join(lines).strip()

#     return sql_query


# if __name__ == "__main__":

#     user_question = input("\nEnter your question: ")

#     try:
#         sql = generate_sql(user_question)

#         print("\n========== GENERATED SQL ==========\n")
#         print(sql)

#     except Exception as error:
#         print(f"\nSQL generation failed: {error}")


#Updated Code 

import json

from llm import llm
from schema_inspector import get_database_schema


def generate_sql(question: str, schema=None):

    if not question.strip():
        raise ValueError("Please provide a question.")

    if schema is None:
        schema = get_database_schema()

    if not schema:
        raise RuntimeError("No database schema found.")

    schema_text = json.dumps(schema, indent=2)

    prompt = f"""
You are an expert MySQL query generator.

Convert the user's natural language question
into a valid MySQL SQL query.

DATABASE SCHEMA:
{schema_text}

USER QUESTION:
{question}

RULES:
1. Use only tables and columns present in the schema.
2. Never invent table or column names.
3. Generate MySQL-compatible SQL.
4. Generate only SELECT queries.
5. Never generate INSERT, UPDATE, DELETE, DROP,
   ALTER, TRUNCATE, CREATE or other modifying queries.
6. Use appropriate JOIN, GROUP BY, ORDER BY,
   and aggregate functions when required.
7. Return only the SQL query.
8. Do not include explanations or Markdown code blocks.
"""

    response = llm.invoke(prompt)

    sql_query = response.content.strip()

    if sql_query.startswith("```"):
        lines = sql_query.splitlines()

        if lines[-1].strip() == "```":
            lines = lines[1:-1]

        sql_query = "\n".join(lines).strip()

    return sql_query


if __name__ == "__main__":

    user_question = input("\nEnter your question: ")

    try:
        sql = generate_sql(user_question)

        print("\n========== GENERATED SQL ==========\n")
        print(sql)

    except Exception as error:
        print(f"\nSQL generation failed: {error}")
