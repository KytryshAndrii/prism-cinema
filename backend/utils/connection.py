import os
import psycopg2

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "ks_bd"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASS", "root")
    )
