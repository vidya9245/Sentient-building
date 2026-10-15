"""Database helpers for Archon: tables, sample data and simple reads."""
import sqlite3
from pathlib import Path

import config

# 6 sample rooms across 3 floors. All numbers are SIMULATED.
# Each device is (type, how many exist, how many are ON).
SAMPLE_ROOMS = [
    {"name": "Reception 101", "floor": 1, "area_m2": 60, "seats": 10,
     "people": 3, "daylight_pct": 85, "lux": 520, "booked": 0,
     "devices": [("light", 8, 8), ("ac", 1, 1), ("fan", 2, 1)]},
    {"name": "Meeting Room 102", "floor": 1, "area_m2": 40, "seats": 12,
     "people": 0, "daylight_pct": 70, "lux": 380, "booked": 1,
     "devices": [("light", 6, 6), ("ac", 1, 1), ("projector", 1, 1),
                 ("screen", 1, 1)]},
    {"name": "Office 201", "floor": 2, "area_m2": 120, "seats": 24,
     "people": 18, "daylight_pct": 40, "lux": 350, "booked": 0,
     "devices": [("light", 12, 12), ("ac", 2, 2), ("fan", 6, 4)]},
    {"name": "Training Hall 202", "floor": 2, "area_m2": 90, "seats": 30,
     "people": 2, "daylight_pct": 60, "lux": 400, "booked": 0,
     "devices": [("light", 14, 14), ("ac", 2, 2), ("fan", 8, 8)]},
    {"name": "Open Workspace 301", "floor": 3, "area_m2": 110, "seats": 24,
     "people": 20, "daylight_pct": 45, "lux": 380, "booked": 0,
     "devices": [("light", 12, 12), ("ac", 2, 2), ("fan", 6, 3)]},
    {"name": "Lab 302", "floor": 3, "area_m2": 100, "seats": 24,
     "people": 0, "daylight_pct": 30, "lux": 420, "booked": 0,
     "devices": [("light", 12, 12), ("ac", 2, 2), ("screen", 24, 24),
                 ("fan", 4, 4)]},
]


def get_connection():
    """Open the database. Creates the data folder and file if missing."""
    Path(config.DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    """Make the rooms and devices tables if they don't exist yet."""
    conn = get_connection()
    conn.execute(
        """CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            floor INTEGER NOT NULL,
            area_m2 REAL NOT NULL,
            seats INTEGER NOT NULL,
            people INTEGER NOT NULL,
            daylight_pct INTEGER NOT NULL,
            lux INTEGER NOT NULL,
            booked INTEGER NOT NULL,
            data_source TEXT NOT NULL DEFAULT 'Simulated'
        )"""
    )
    conn.execute(
        """CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id INTEGER NOT NULL,
            device_type TEXT NOT NULL,
            count INTEGER NOT NULL,
            on_count INTEGER NOT NULL,
            FOREIGN KEY (room_id) REFERENCES rooms (id)
        )"""
    )
    conn.commit()
    conn.close()


def seed_sample_data():
    """Add the 6 sample rooms once. Returns True if it added them."""
    conn = get_connection()
    already = conn.execute("SELECT COUNT(*) FROM rooms").fetchone()[0]
    if already > 0:
        conn.close()
        return False
    for room in SAMPLE_ROOMS:
        # The ? marks keep data safe from SQL injection (a common attack).
        cursor = conn.execute(
            """INSERT INTO rooms (name, floor, area_m2, seats, people,
               daylight_pct, lux, booked) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (room["name"], room["floor"], room["area_m2"], room["seats"],
             room["people"], room["daylight_pct"], room["lux"],
             room["booked"]),
        )
        room_id = cursor.lastrowid
        for device_type, count, on_count in room["devices"]:
            conn.execute(
                """INSERT INTO devices (room_id, device_type, count, on_count)
                   VALUES (?, ?, ?, ?)""",
                (room_id, device_type, count, on_count),
            )
    conn.commit()
    conn.close()
    return True


def room_power_kw(conn, room_id):
    """Energy = sum of kW of the devices that are ON."""
    rows = conn.execute(
        "SELECT device_type, on_count FROM devices WHERE room_id = ?",
        (room_id,),
    ).fetchall()
    return sum(config.DEVICE_KW[r["device_type"]] * r["on_count"]
               for r in rows)


def get_rooms_summary():
    """Return every room as a dictionary, with its live kW added."""
    conn = get_connection()
    rooms = []
    for row in conn.execute("SELECT * FROM rooms ORDER BY floor, name"):
        room = dict(row)
        room["kw"] = room_power_kw(conn, room["id"])
        rooms.append(room)
    conn.close()
    return rooms


if __name__ == "__main__":
    create_tables()
    if seed_sample_data():
        print("Created tables. Added 6 sample rooms.")
    else:
        print("Sample data already there (no changes).")
    total = 0
    for r in get_rooms_summary():
        print(f"{r['name']:<20} floor {r['floor']}  "
              f"people {r['people']}/{r['seats']}  {r['kw']:.3f} kW")
        total += r["kw"]
    print(f"Total power now: {total:.3f} kW")