import sqlite3
import os

DB_FOLDER = "data"

DB_PATH = os.path.join(
    DB_FOLDER,
    "guardian.db"
)


def get_connection():

    os.makedirs(
        DB_FOLDER,
        exist_ok=True
    )

    conn = sqlite3.connect(
        DB_PATH
    )

    conn.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conn


def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            ALTER TABLE goals
            ADD COLUMN status TEXT DEFAULT 'Active'
            """
        )

    except Exception:

        pass

    # Goals
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            deadline TEXT NOT NULL,
            status TEXT DEFAULT 'Active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # Monthly Missions
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS monthly_missions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal_id INTEGER NOT NULL,
            month INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            deliverable TEXT,
            success_criteria TEXT,
            estimated_weeks INTEGER,
            status TEXT DEFAULT 'Locked',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(goal_id)
            REFERENCES goals(id)
        )
        """
    )

    # Weekly Missions
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS weekly_missions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            monthly_mission_id INTEGER NOT NULL,
            week INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            deliverable TEXT,
            success_criteria TEXT,
            estimated_days INTEGER,
            status TEXT DEFAULT 'Locked',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(monthly_mission_id)
            REFERENCES monthly_missions(id)
        )
        """
    )

    # Daily Missions
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS daily_missions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            weekly_mission_id INTEGER NOT NULL,
            day INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            deliverable TEXT,
            success_criteria TEXT,
            estimated_hours REAL,
            status TEXT DEFAULT 'Locked',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(weekly_mission_id)
            REFERENCES weekly_missions(id)
        )
        """
    )

    # Daily Tasks
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS daily_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            daily_mission_id INTEGER NOT NULL,
            task INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            deliverable TEXT,
            success_criteria TEXT,
            estimated_hours REAL,
            status TEXT DEFAULT 'Pending',
            completed_at TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(daily_mission_id)
            REFERENCES daily_missions(id)
        )
        """
    )

    conn.commit()
    conn.close()