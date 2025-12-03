# insert_sample_data.py
import psycopg2
import uuid
from datetime import date, timedelta
import random

# Dane dostępowe do bazy
conn = psycopg2.connect(
    dbname="ks_bd",
    user="postgres",
    password="root",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# --- FUNKCJA DO GENEROWANIA UUID JAKO STRING ---
def uuid_str():
    return str(uuid.uuid4())




conn.commit()
print("Przykładowe dane zostały dodane.")
cur.close()
conn.close()
