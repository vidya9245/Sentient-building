import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "archon.db"

SAMPLE_ROOMS = [
    ("Living Room", 1, 28.0),
    ("Kitchen", 1, 14.0),
    ("Bedroom 1", 2, 16.0),
    ("Bedroom 2", 2, 12.0),
    ("Bathroom", 2, 6.0),
    ("Home Office", 1, 10.0),
]


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


def add_sample_rooms():
    # INSERT OR IGNORE means: skip a room if it is already there.
    # So running this file many times never makes duplicates.
    conn = get_connection()
    conn.executemany(
        "INSERT OR IGNORE INTO rooms (name, floor, area_sqm) VALUES (?, ?, ?)",
        SAMPLE_ROOMS,
    )
    conn.commit()
    conn.close()


def get_all_rooms():
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, name, floor, area_sqm FROM rooms ORDER BY id"
    ).fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    create_rooms_table()
    add_sample_rooms()
    for room in get_all_rooms():
        print(room)