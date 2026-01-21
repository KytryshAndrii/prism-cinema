import bcrypt
import uuid
from utils.connection import get_connection
from auth_utils import generate_token


def register_user_logic(data):
    """
    Handles register logic for user.
    """
    login = data.get("login")
    email = data.get("email")
    password = data.get("password").encode("utf-8")
    date_of_birth = data.get("dateOfBirth")
    region = data.get("region") or " "

    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT 1 FROM "USERS"
            WHERE user_login = %s OR user_mail = %s
            LIMIT 1
        """, (login, email))

        if cur.fetchone():
            return None, 409

        cur.execute("""
            SELECT subscription_plan_id
            FROM "SERVICE_SUBSCRIPTION_PLANS"
            WHERE subscription_plan_type = 'Free'
            LIMIT 1
        """)

        free_plan = cur.fetchone()
        if not free_plan:
            return {"error": "No Free plan found"}, 500

        free_plan_id = free_plan[0]

        new_user_id = str(uuid.uuid4())

        cur.execute("""
            INSERT INTO "USERS" (
                user_id, user_login, user_mail,
                user_password, user_is_admin,
                user_is_subscribed, user_subscription_plan_id,
                user_location_region, user_date_of_birth
            )
            VALUES (%s, %s, %s, %s, FALSE, FALSE, %s, %s, %s)
        """, (
            new_user_id,
            login,
            email,
            hashed_password,
            free_plan_id,
            region,
            date_of_birth
        ))

        conn.commit()

        token = generate_token(new_user_id)

        return {
            "id": new_user_id,
            "login": login,
            "email": email,
            "isUserSubscribed": False,
            "isUserAdmin": False,
            "token": token
        }, 200

    finally:
        cur.close()
        conn.close()


def login_user_logic(login, password):
    """
    Handles login logic for a user.
    Returns (response_data, status_code)
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT user_id, user_login, user_mail, user_password, user_is_admin,
                   user_is_subscribed, user_location_region, user_date_of_birth
            FROM "USERS"
            WHERE user_login = %s
        """, (login,))

        user = cur.fetchone()
        if not user:
            return None, 401  # Unauthorized

        if bcrypt.checkpw(password.encode("utf-8"), user[3].encode("utf-8")):
            token = generate_token(str(user[0]))
            return {
                "id": user[0],
                "login": user[1],
                "email": user[2],
                "region": user[6],
                "birthday": user[7],
                "isUserSubscribed": user[5],
                "isUserAdmin": user[4],
                "token": token
            }, 200
        else:
            return None, 401
    finally:
        cur.close()
        conn.close()


def update_user_profile_logic(user_id, data):
    """
    Updates user profile. Returns status code only.
    """
    if not data or not any([data.get("login"), data.get("email"), data.get("password")]):
        return 400

    login = data.get("login")
    email = data.get("email")
    password = data.get("password")

    conn = get_connection()
    cur = conn.cursor()

    try:
        if login or email:
            cur.execute("""
                SELECT 1 FROM "USERS"
                WHERE (user_login = %s OR user_mail = %s)
                AND user_id != %s
                LIMIT 1
            """, (login, email, str(user_id)))

            if cur.fetchone():
                return 409  # Conflict

        if login:
            cur.execute("""
                UPDATE "USERS"
                SET user_login = %s
                WHERE user_id = %s
            """, (login, str(user_id)))

        if email:
            cur.execute("""
                UPDATE "USERS"
                SET user_mail = %s
                WHERE user_id = %s
            """, (email, str(user_id)))

        if password:
            hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            cur.execute("""
                UPDATE "USERS"
                SET user_password = %s
                WHERE user_id = %s
            """, (hashed, str(user_id)))

        conn.commit()
        return 200
    except Exception:
        conn.rollback()
        return 500
    finally:
        cur.close()
        conn.close()


def get_users_logic(limit=50):
    """
    Returns a list of users (limited by `limit`).
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(f"""
            SELECT
                user_id,
                user_login,
                user_mail,
                user_is_admin,
                user_is_subscribed,
                user_location_region,
                user_date_of_birth
            FROM "USERS"
            LIMIT %s
        """, (limit,))

        rows = cur.fetchall()
        users = []
        for row in rows:
            users.append({
                "id": str(row[0]),
                "login": row[1],
                "email": row[2],
                "isAdmin": row[3],
                "isSubscribed": row[4],
                "region": row[5],
                "dateOfBirth": str(row[6]) if row[6] else None
            })

        return users
    finally:
        cur.close()
        conn.close()
