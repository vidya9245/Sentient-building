"""Archon app: first simple dashboard page."""
import pandas as pd
import streamlit as st

import config
from core import database

st.set_page_config(page_title="Archon", page_icon="🏢", layout="wide")

# Make sure the database and sample rooms exist.
database.create_tables()
database.seed_sample_data()

rooms = database.get_rooms_summary()
df = pd.DataFrame(rooms)

total_people = int(df["people"].sum())
total_seats = int(df["seats"].sum())
total_kw = float(df["kw"].sum())

st.title("🏢 Archon")
st.caption("Green Building Digital Twin. All data here is Simulated.")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Occupancy", f"{total_people} / {total_seats}")
col2.metric("Power now", f"{total_kw:.2f} kW")
col3.metric("Cost per hour", f"{config.kwh_to_cost(total_kw):.0f} INR")
col4.metric("CO2e per hour", f"{config.kwh_to_co2(total_kw):.1f} kg")

st.subheader("Rooms")
table = df[["name", "floor", "people", "seats", "kw", "lux",
            "daylight_pct", "data_source"]]
table.columns = ["Room", "Floor", "People", "Seats", "Power (kW)",
                 "Light (lux)", "Daylight %", "Source"]
st.dataframe(table, hide_index=True, use_container_width=True)