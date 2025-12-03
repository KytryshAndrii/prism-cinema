from utils.uuidToString import uuid_str
from datetime import date, timedelta
import random
from db.connection import conn

# --- FUNKCJA DO GENEROWANIA ZAKRESU SUBSKRYBCJI NA 1 MIESIAC ---
def daterange_one_month():
    start = date.today()
    end = start + timedelta(days=30)
    return f'[{start},{end})'  # Postgres daterange: inclusive start, exclusive end

# --- FUNKCJA DO GENEROWANIA ZAKRESU SUBSKRYBCJI NA 6 MIESIECY ---
def daterange_six_months():
    start = date.today()
    end = start + timedelta(days=180)
    return f'[{start},{end})'


def insert_dumb_data_users_table():
    cur = conn.cursor()


    first_names = ['Anna', 'Jan', 'Katarzyna', 'Michał', 'Julia', 'Tomasz', 'Aleksandra', 'Piotr', 'Zuzanna', 'Kacper']
    last_names = ['Nowak', 'Kowalski', 'Wiśniewska', 'Wójcik', 'Kamiński', 'Lewandowski', 'Zielińska', 'Szymański', 'Woźniak', 'Dąbrowski']

    # Pobierz ID planów subskrypcji
    cur.execute("""
        SELECT subscription_plan_id, subscription_plan_type
        FROM "SERVICE_SUBSCRIPTION_PLANS";
    """)
    plans = cur.fetchall()

    # Znajdź plany po typie
    plans_dict = {plan_type: plan_id for (plan_id, plan_type) in plans}
    monthly_plan_id = plans_dict.get('Miesięczny')
    six_month_plan_id = plans_dict.get('Półroczny')

    if not monthly_plan_id or not six_month_plan_id:
        raise Exception("Nie znaleziono wszystkich wymaganych planów subskrypcji.")
    used_combinations = set()
    for i in range(10):
        user_id = uuid_str()

        # Unikalna kombinacja imienia i nazwiska
        while True:
            first =first_names[i]
            last = last_names[i]
            if (first, last) not in used_combinations:
                used_combinations.add((first, last))
                break

        login = f"{last.lower()}"
        email = f"{login}@example.com"
        password = f"{first.lower()}{random.randint(100, 999)}"

        is_admin = (i == 0)
        is_observer = (i == 1)

        if random.choice([True, False]):
            sub_id = monthly_plan_id
            sub_period = daterange_one_month()
        else:
            sub_id = six_month_plan_id
            sub_period = daterange_six_months()

        if is_observer:
            cur.execute("""
                   INSERT INTO "USERS" (
                       user_id, user_login, user_password, user_mail,
                       user_is_subscripted, user_subscription_plan_id,
                       user_subscription_period, user_is_admin, user_location_region,
                       user_date_of_birth
                   )
                   VALUES (%s, %s, %s, %s, %s, NULL, NULL, %s, %s, %s)
               """, (
                uuid_str(), login, password, email,
                False, is_admin, 'PL', date(1990 + i, 1, 1)
            ))
        else:
            cur.execute("""
                INSERT INTO "USERS" (
                    user_id, user_login, user_password, user_mail,
                    user_is_subscripted, user_subscription_plan_id,
                    user_subscription_period, user_is_admin, user_location_region,
                    user_date_of_birth
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                user_id, login, password, email,
                True, sub_id, sub_period, is_admin, 'PL', date(1990 + i, 1, 1)
            ))

        print(f"✅ Dodano: {first} {last} | login: {login} | admin: {is_admin}")

    print("✅ Wszyscy użytkownicy zostali dodani.")

    conn.commit()
    print("Przykładowe dane zostały dodane.")
    cur.close()
    conn.close()
