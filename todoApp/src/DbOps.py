import sqlite3
import os
from pathlib import Path
from ToDO.AppLogging import app_logger

DB_PATH = os.path.join(Path(__file__).resolve().parent.parent.parent, "tasks.sqlite3")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            status TEXT DEFAULT 'pending'
        )
    """)
    conn.commit()
    conn.close()


def fetch_all_tasks():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def ensure_tasks_table_exists():
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                due_date TEXT,
                status TEXT DEFAULT 'pending'
            )
        """)
        conn.commit()
    except Exception as e:
        app_logger.error(f"Failed to ensure tasks table exists: {e}")
        raise
    finally:
        conn.close()


def create_todo_task(title, description=None, due_date=None, status="pending"):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tasks (title, description, due_date, status) VALUES (?, ?, ?, ?)",
            (title, description, due_date, status)
        )
        conn.commit()
        return cur.lastrowid
    except Exception as e:
        app_logger.error(f"Failed to create task: {e}")
        raise
    finally:
        conn.close()


def get_task_by_id(task_id):
    conn = get_conn()
    row = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def modify_task(task_id, title=None, description=None, due_date=None, status=None):
    conn = get_conn()
    cursor = conn.cursor()

    fields = []
    values = []

    if title is not None:
        fields.append("title=?")
        values.append(title)

    if description is not None:
        fields.append("description=?")
        values.append(description)

    if due_date is not None:
        fields.append("due_date=?")
        values.append(due_date)

    if status is not None:
        fields.append("status=?")
        values.append(status)

    # No fields to update
    if not fields:
        conn.close()
        return False

    # Build SQL query dynamically
    sql = f"UPDATE tasks SET {', '.join(fields)} WHERE id=?"
    values.append(task_id)

    cursor.execute(sql, tuple(values))
    conn.commit()
    conn.close()
    return True


def remove_task(task_id):
    conn = get_conn()
    conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
