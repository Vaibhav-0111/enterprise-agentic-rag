"""
SQL Agent — generates and executes SQL queries on PostgreSQL.
"""
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from database.postgres_connector import execute_query, get_schema
from typing import Any, Dict
import re


SQL_SYSTEM_PROMPT = """You are a SQL expert agent. Given a business question and the database schema,
generate a single, correct PostgreSQL query that answers the question.

Schema:
{schema}

Rules:
- Return ONLY the SQL query, no explanation, no markdown.
- Always use table aliases for clarity.
- Prefer CTEs for complex multi-step logic.
- Never use SELECT *; always name columns explicitly.
- Add LIMIT 50 unless the question requires all rows."""

SQL_USER_PROMPT = "Business question: {question}"


def run_sql_agent(question: str, llm: ChatOpenAI = None) -> Dict[str, Any]:
    """Generate SQL from a business question, execute it, return results."""
    if llm is None:
        llm = ChatOpenAI(model="gpt-4o", temperature=0)

    schema = get_schema()

    prompt = ChatPromptTemplate.from_messages([
        ("system", SQL_SYSTEM_PROMPT),
        ("human",  SQL_USER_PROMPT),
    ])
    chain  = prompt | llm
    result = chain.invoke({"schema": schema, "question": question})

    # Strip markdown fences if model adds them
    sql = re.sub(r"```(?:sql)?|```", "", result.content).strip()

    rows, columns = execute_query(sql)
    return {
        "sql":     sql,
        "rows":    rows,
        "columns": columns,
        "count":   len(rows),
    }
