import sqlite3
from pathlib import Path

# SQLite is a small database that lives in one file.
# Python already has it built in, so we install nothing.
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "archon.db"


def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


def create_rooms_table():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            floor INTEGER NOT NULL,
            area_sqm REAL NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_rooms_table()
    print("Rooms table is ready.")