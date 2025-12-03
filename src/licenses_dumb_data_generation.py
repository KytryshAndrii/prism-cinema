import psycopg2
import uuid
from datetime import date


# Dane dostępowe do bazy
conn = psycopg2.connect(
    dbname="ks_bd",
    user="postgres",
    password="root",
    host="localhost",
    port="5432"
)


# --- FUNKCJA DO GENEROWANIA UUID JAKO STRING ---
def uuid_str():
    return str(uuid.uuid4())



# Dane do wstawienia
licenses = [
    ("USA", date(2026, 12, 31)),
    ("CAN", date(2025, 9, 30)),
    ("GBR", date(2027, 5, 15)),
    ("POL", date(2025, 12, 1)),
    ("DEU", date(2026, 6, 20)),
    ("FRA", date(2026, 7, 1)),
    ("ESP", date(2025, 11, 10)),
    ("ITA", date(2026, 3, 25)),
    ("JPN", date(2027, 1, 1)),
    ("AUS", date(2026, 9, 9)),
]

def insert_dumb_data_licenses():
    cur = conn.cursor()
    # Wstawianie danych
    for region, exp_date in licenses:
        uniqueId = uuid_str()
        cur.execute("""
            INSERT INTO "LICENSES" (license_id, license_region, license_expiration_date)
            VALUES (%s, %s, %s)
        """, (uniqueId, region, exp_date))

        print(f"✅ Dodano licencję: {region} ({uniqueId})")

    conn.commit()
    print("Przykładowe dane zostały dodane.")
    cur.close()
    conn.close()

