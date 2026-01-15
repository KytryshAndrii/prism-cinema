import bcrypt
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_cors import cross_origin
from db.connection import get_connection
from search_entities import search_entities
import uuid
import base64

from db_backend.auth_utils import generate_token
from db_backend.token_validation import token_required

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Endpoint testowy /health
@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}

@app.route('/register', methods=['POST'])
@cross_origin()
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
        "isUserSubscribed": False,
        "isUserAdmin": False,
        "token": token
    }), 200


@app.route('/login', methods=['POST'])
@cross_origin()
def login_user():
    data = request.get_json()
    login = data.get("login")
    password = data.get("password").encode("utf-8")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
           SELECT user_id, user_login, user_mail, user_password, user_is_admin,
            user_is_subscribed, user_location_region, user_date_of_birth 
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
                "region": user[6],
                "birthday": user[7],
                "isUserSubscribed": user[5],
                "isUserAdmin": user[4],
                "token": token
            }), 200
        else:
            return jsonify(None), 401
    except ValueError:
        return jsonify(None), 406

@app.route("/user_update/<uuid:user_id>", methods=["POST"])
@token_required
def update_user_profile(user_id):
    data = request.get_json()

    if not data:
        return "", 400

    login = data.get("login")
    email = data.get("email")
    password = data.get("password")

    if not any([login, email, password]):
        return "", 400

    conn = get_connection()
    cur = conn.cursor()

    try:
        # sprawdz login/email conflict
        if login or email:
            cur.execute("""
                SELECT 1 FROM "USERS"
                WHERE (user_login = %s OR user_mail = %s)
                AND user_id != %s
                LIMIT 1
            """, (login, email, str(user_id)))

            if cur.fetchone():
                return "", 409

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
            hashed = bcrypt.hashpw(
                password.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            cur.execute("""
                UPDATE "USERS"
                SET user_password = %s
                WHERE user_id = %s
            """, (hashed, str(user_id)))

        conn.commit()
        return "", 200

    except Exception as e:
        conn.rollback()
        return "", 500

    finally:
        cur.close()
        conn.close()



@app.route("/users", methods=["GET"])
@token_required
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
            "id": str(row[0]),
            "login": row[1],
            "email": row[2],
            "isAdmin": row[3],
            "isSubscribed": row[4],
            "region": row[5],
            "dateOfBirth": str(row[6]) if row[6] else None
        })

    return jsonify(users)



@app.route("/movies", methods=["GET"])
# @token_required
def get_movies():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
           SELECT
               m.movie_id,
               m.movie_name,
               amd.movie_poster,
               amd.movie_preview_poster
           FROM "MOVIES" m
           LEFT JOIN "ADDITIONAL_MOVIE_DATA" amd
               ON amd.movie_id = m.movie_id
           LIMIT 50
       """)

    rows = cur.fetchall()
    cur.close()
    conn.close()
    movies = []

    for row in rows:
        movie_id = row[0]
        movie_name = row[1]
        poster_bytes = row[2]
        preview_poster_bytes = row[3]

        # BYTEA -> base64 (lub None)
        poster_base64 = (
            base64.b64encode(poster_bytes).decode("utf-8")
            if poster_bytes
            else None
        )

        movies.append({
            "movie_id": str(movie_id),
            "movie_name": movie_name,
            "movie_poster": poster_base64,
        })

    return jsonify(movies), 200

@app.route("/movie_details/<uuid:movie_id>", methods=["GET"])
def get_movie_details(movie_id):
    conn = get_connection()
    cur = conn.cursor()

    # 1. Szczegóły filmu + trailer
    cur.execute("""
        SELECT
            m.movie_description,
            m.movie_rating,
            m.movie_pg,
            m.movie_release_date,
            amd.movie_trailer,
            amd.movie_poster,
            amd.movie_preview_poster
        FROM "MOVIES" m
        LEFT JOIN "ADDITIONAL_MOVIE_DATA" amd ON amd.movie_id = m.movie_id
        WHERE m.movie_id = %s
    """, (str(movie_id),))
    movie_data = cur.fetchone()

    if not movie_data:
        cur.close()
        conn.close()
        return jsonify({"error": "Movie not found"}), 404

    description, rating, pg, release_date, trailer_url, movie_poster, movie_preview_poster = movie_data

    # 2. Gatunki
    cur.execute("""
        SELECT g.genre_name
        FROM "MOVIE_GENRES" mg
        JOIN "GENRES" g ON mg.genre_id = g.genre_id
        WHERE mg.movie_id = %s
    """, (str(movie_id),))
    genres = [row[0] for row in cur.fetchall()]

    # 3. Aktorzy
    cur.execute("""
        SELECT a.first_name, a.last_name
        FROM "MOVIE_ACTORS" ma
        JOIN "ACTORS" a ON ma.actor_id = a.actor_id
        WHERE ma.movie_id = %s
    """, (str(movie_id),))
    actors = [f"{row[0]} {row[1]}" for row in cur.fetchall()]

    # 4. Reżyserzy
    cur.execute("""
        SELECT d.first_name, d.last_name
        FROM "MOVIE_DIRECTORS" md
        JOIN "DIRECTORS" d ON md.director_id = d.director_id
        WHERE md.movie_id = %s
    """, (str(movie_id),))
    directors = [f"{row[0]} {row[1]}" for row in cur.fetchall()]

    cur.close()
    conn.close()

    poster_base64 = (
        base64.b64encode(movie_poster).decode("utf-8")
        if movie_poster
        else None
    )

    preview_poster_base64 = (
        base64.b64encode(movie_preview_poster).decode("utf-8")
        if movie_preview_poster
        else None
    )

    return jsonify({
        "description": description,
        "rating": rating,
        "pg": pg,
        "release_date": release_date.isoformat() if release_date else None,
        "trailer_url": trailer_url,
        "genres": genres,
        "actors": actors,
        "directors": directors,
        "movie_poster": poster_base64,
        "movie_preview_poster": preview_poster_base64
    }), 200

@app.route("/subscriptions/plans", methods=["GET"])
def get_subscriptions_plans():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            subscription_plan_id,
            subscription_plan_type,
            subscription_plan_cost,
            subscription_plan_description
        FROM "SERVICE_SUBSCRIPTION_PLANS"
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    users = []
    for row in rows:
        users.append({
            "id": str(row[0]),
            "sub_type": row[1],
            "sub_cost": str(row[2]),
            "sub_description": row[3],
        })

    return jsonify(users)

@app.route("/subscriptions/subscribe", methods=["POST"])
@cross_origin()
def subscribe_to_plan():
    data = request.get_json()
    user_id = data.get("user_id")
    plan_id = data.get("plan_id")

    if not user_id or not plan_id:
        return jsonify({"error": "Missing data"}), 400

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT subscription_plan_type
            FROM "SERVICE_SUBSCRIPTION_PLANS"
            WHERE subscription_plan_id = %s
        """, (plan_id,))

        plan = cur.fetchone()

        if not plan:
            return jsonify({"error": "Subscription plan not found"}), 404

        plan_type = plan[0]

        if plan_type.lower() == "free":

            cur.execute("""
                UPDATE "USERS"
                SET user_is_subscribed = FALSE,
                    user_subscription_plan_id = %s
                WHERE user_id = %s
            """, (plan_id, user_id))

        else:

            cur.execute("""
                UPDATE "USERS"
                SET user_is_subscribed = TRUE,
                    user_subscription_plan_id = %s
                WHERE user_id = %s
            """, (plan_id, user_id))

        conn.commit()
        return '', 200

    except Exception as e:
        print("Subscription error:", e)
        return jsonify({"error": "Internal server error"}), 500

    finally:
        cur.close()
        conn.close()


@app.route("/subscriptions/is_free/<uuid:user_id>", methods=["GET"])
def check_user_free(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT user_is_subscribed
        FROM "USERS"
        WHERE user_id = %s
    """, (str(user_id),))

    result = cur.fetchone()
    cur.close()
    conn.close()

    if result is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify(not result[0])


@app.route("/subscriptions/plan/<uuid:user_id>", methods=["GET"])
def get_user_subscription_plan(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT s.subscription_plan_type, s.subscription_plan_id
        FROM "USERS" u
        LEFT JOIN "SERVICE_SUBSCRIPTION_PLANS" s
        ON u.user_subscription_plan_id = s.subscription_plan_id
        WHERE u.user_id = %s
    """, (str(user_id),))

    result = cur.fetchone()
    cur.close()
    conn.close()

    if not result or result[0] is None:
        return jsonify(None), 200

    return jsonify({
        "id": str(result[1]),
        "sub_type": result[0],
    }), 200

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

# @app.route("movies/add", methods=["POST"])
# def add_movie():
#     data = request.get_json()
#
#     movie_name = data["movie_name"]
#     movie_rating = data["movie_rating"]
#     movie_release_date = data["movie_release_date"]
#     movie_pg = data["movie_pg"]
#     movie_description = data["movie_description"]
#
#     new_movie_id = str(uuid.uuid4())
#
#     actor_ids = data.get("actor_ids", "").split(";")
#     director_ids = data.get("director_ids", "").split(";")
#     genre_ids = data.get("genre_ids", "").split(";")
#
#     conn = get_connection()
#     cur = conn.cursor()
#
#     cur.execute(""" """,)
#
#

# @app.route("/search/actors", methods=["GET"])
# def get_actors():
#     return search_entities("ACTORS")

# @app.route("/search/actors", methods=["GET"])
# def

@app.route("/search/actors", methods=["GET"])
def get_search_actors():
    return search_entities("ACTORS")

@app.route("/search/directors", methods=["GET"])
def get_search_directors():
    return search_entities("DIRECTORS")

@app.route("/search/users", methods=["GET"])
def get_search_users():
    return search_entities("USERS")

@app.route("/search/movies", methods=["GET"])
def get_search_movies():
    return search_entities("MOVIES")


# Uruchomienie serwera
if __name__ == "__main__":
    app.run(debug=True)
