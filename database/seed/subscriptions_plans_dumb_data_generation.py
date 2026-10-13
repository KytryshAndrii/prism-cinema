from db.connection import conn
from utils.uuidToString import uuid_str

#Dodanie planów subskrypcji
# --- Wygeneruj UUID dla dwóch planów ---
monthly_plan_id =  uuid_str()
semiannual_plan_id = uuid_str()

def insert_dumb_data_subscriptions_plans():
    cur = conn.cursor()
    # --- Dodanie planu miesięcznego ---
    cur.execute("""
        INSERT INTO "SERVICE_SUBSCRIPTION_PLANS" (
            subscription_plan_id,
            subscription_plan_type,
            subscription_plan_cost
        )
        VALUES (%s, %s, %s)
    """, (
        monthly_plan_id,
        'Miesięczny',
        97  # koszt w zł
    ))

    # --- Dodanie planu półrocznego ---
    cur.execute("""
        INSERT INTO "SERVICE_SUBSCRIPTION_PLANS" (
            subscription_plan_id,
            subscription_plan_type,
            subscription_plan_cost
        )
        VALUES (%s, %s, %s)
    """, (
        semiannual_plan_id,
        'Półroczny',
        244  # koszt w zł
    ))

    conn.commit()
    print("Przykładowe dane zostały dodane.")
    cur.close()
    conn.close()