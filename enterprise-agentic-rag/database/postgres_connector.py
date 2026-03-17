"""
PostgreSQL Connector — manages connections and query execution.
"""
import os
import psycopg2
import psycopg2.extras
from typing import Tuple, List, Any
from contextlib import contextmanager


DB_CONFIG = {
    "host":     os.getenv("POSTGRES_HOST",     "localhost"),
    "port":     int(os.getenv("POSTGRES_PORT", "5432")),
    "dbname":   os.getenv("POSTGRES_DB",       "enterprise"),
    "user":     os.getenv("POSTGRES_USER",     "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
}


@contextmanager
def get_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def execute_query(sql: str) -> Tuple[List[dict], List[str]]:
    """Execute a SQL query and return (rows, column_names)."""
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql)
            rows    = [dict(row) for row in cur.fetchall()]
            columns = [desc[0] for desc in cur.description] if cur.description else []
    return rows, columns


def get_schema() -> str:
    """Return a concise schema description for the SQL agent prompt."""
    schema_sql = """
    SELECT
        table_name,
        column_name,
        data_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
    ORDER BY table_name, ordinal_position;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(schema_sql)
            rows = cur.fetchall()

    schema_lines = []
    current_table = None
    for table, col, dtype in rows:
        if table != current_table:
            schema_lines.append(f"\nTable: {table}")
            current_table = table
        schema_lines.append(f"  {col}: {dtype}")
    return "\n".join(schema_lines)
