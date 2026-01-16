import bcrypt
import uuid
from utils.connection import get_connection
from db_backend.auth_utils import generate_token

def register_user_logic(data):
    login = data.get("login")
    email = data.get("email")
    password = data.get("password").encode("utf-8")
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")
    date_of_birth = data.get("dateOfBirth")

    conn = get_connection()
    cur = conn.cursor()

    # Check if user exists
    cur.execute("""
        SELECT 1 FROM "USERS"
        WHERE user_login = %s OR user_mail = %s
        LIMIT 1
    """, (login, email))

    if cur.fetchone():
        cur.close()
        conn.close()
        return None, 409  # Conflict

    # Create new user
    new_user_id = str(uuid.uuid4())
    cur.execute("""
        INSERT INTO "USERS" (
            user_id, user_login, user_mail,
            user_password, user_is_admin,
            user_is_subscribed, user_location_region,
            user_date_of_birth
        )
        VALUES (%s, %s, %s, %s, FALSE, FALSE, %s, %s)
    """, (new_user_id, login, email, hashed_password, "PL", date_of_birth))

    conn.commit()
    cur.close()
    conn.close()

    token = generate_token(new_user_id)

    return {
        "id": str(new_user_id),
        "login": login,
        "email": email,
        "isUserSubscribed": False,
        "isUserAdmin": False,
        "token": token
    }, 200