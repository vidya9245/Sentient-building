# config.py
# All settings and constants for Archon live here.

# --- Energy maths ---
CO2_KG_PER_KWH = 0.71      # kg of CO2e per kWh of electricity
COST_INR_PER_KWH = 9       # price in rupees per kWh

# --- Light targets (lux = how bright a surface is) ---
TARGET_LUX_MIN = 300
TARGET_LUX_MAX = 500

# --- Security settings (used in the login phase later) ---
OTP_EXPIRY_MINUTES = 5
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_MINUTES = 10
SESSION_TIMEOUT_MINUTES = 15

# --- Storage ---
DB_PATH = "data/archon.db"

# --- Typical power of each device, in kilowatts (kW) ---
DEVICE_KW = {
    "light": 0.02,
    "ac": 1.5,
    "fan": 0.075,
    "heater": 1.0,
    "screen": 0.1,
    "projector": 0.3,
}


def kwh_to_cost(kwh):
    """Turn kWh into rupees."""
    return kwh * COST_INR_PER_KWH


def kwh_to_co2(kwh):
    """Turn kWh into kg of CO2e."""
    return kwh * CO2_KG_PER_KWH


if __name__ == "__main__":
    print("Config loaded OK")
    print("1 kWh costs", kwh_to_cost(1), "INR")
    print("1 kWh makes", kwh_to_co2(1), "kg CO2e")