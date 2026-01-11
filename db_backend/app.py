import bcrypt
from flask import Flask, jsonify, request
from db.connection import get_connection
import uuid
import secrets

from db_backend.auth_utils import generate_token
from db_backend.token_validation import token_required


app = Flask(__name__)

# Endpoint testowy /health
@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}

@app.route('/register', methods=['GET'])
def register_user():
    data = request.get_json()
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

    existing = cur.fetchone()
    if existing:
        cur.close()
        conn.close()
        return jsonify(None), 409  # Conflict

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
    return jsonify({
        "id": str(new_user_id),
        "login": login,
        "email": email,
        "token": token
    }), 200

@app.route('/login', methods=['GET'])
def login_user():
    data = request.get_json()
    login = data.get("login")
    password = data.get("password").encode("utf-8")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
           SELECT user_id, user_login, user_mail, user_password
           FROM "USERS"
           WHERE user_login = %s
       """, (login,))

    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user:
        return jsonify(None), 401
    try:
        if bcrypt.checkpw(password, user[3].encode("utf-8")):
            token = generate_token(str(user[0]))
            return jsonify({
                "id": user[0],
                "login": user[1],
                "email": user[2],
                "token": token
            }), 200
        else:
            return jsonify(None), 401
    except ValueError:
        return jsonify(None), 406

@app.route("/users", methods=["GET"])
def get_users():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            user_id,
            user_login,
            user_mail,
            user_is_admin,
            user_is_subscribed,
            user_location_region,
            user_date_of_birth
        FROM "USERS"
        LIMIT 50
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    users = []
    for row in rows:
        users.append({
            "id": str(row[0]),                   # UUID → string
            "login": row[1],
            "email": row[2],
            "isAdmin": row[3],
            "isSubscribed": row[4],
            "region": row[5],
            "dateOfBirth": str(row[6]) if row[6] else None
        })

    return jsonify(users)


@app.route("/movies", methods=["GET"])
@token_required
def get_movies():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
           *
        FROM "MOVIES"
        LIMIT 50
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    users = []
    for row in rows:
        users.append({
            "movie_id": str(row[0]),                   # UUID → string
            "movie_name": row[1],
            "movie_rating": row[2],
            "movie_release_date": row[3],
            "movie_pg": row[4],
            "movie_description": row[5],
        })

    return jsonify(users)

# Endpoint /movies-with-directors
@app.route("/api/views/movies_with_directors", methods=["GET"])
def movies_with_directors():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
           *
        FROM MOVIES_WITH_DIRECTORS
        LIMIT 50
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    movies = []
    for row in rows:
        movies.append({
            "movie_title": row[0],
            "directors": row[1]
        })

    return jsonify(movies)

# Uruchomienie serwera
if __name__ == "__main__":
    app.run(debug=True)
