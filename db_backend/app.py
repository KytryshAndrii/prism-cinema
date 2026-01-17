import bcrypt
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_cors import cross_origin
from utils.connection import get_connection
from search_entities import search_entities
import uuid
import base64

from auth_utils import generate_token
from token_validation import token_required
from service.user import register_user_logic

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Endpoint testowy /health
@app.route("/health", methods=["GET"])
@cross_origin()
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
    region = data.get("region") or " "

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

    cur.execute("""
                SELECT subscription_plan_id FROM "SERVICE_SUBSCRIPTION_PLANS"
                WHERE subscription_plan_type = 'Free'
                LIMIT 1
            """)
    free_plan = cur.fetchone()
    if not free_plan:
        return jsonify({"error": "No Free plan found"}), 500

    free_plan_id = free_plan[0]

    # Create new user
    new_user_id = str(uuid.uuid4())

    cur.execute("""
            INSERT INTO "USERS" (
                user_id, user_login, user_mail,
                user_password, user_is_admin,
                user_is_subscribed, user_subscription_plan_id,
                user_location_region,
                user_date_of_birth
            )
            VALUES (%s, %s, %s, %s, FALSE, FALSE, %s, %s, %s)
        """, (new_user_id, login, email, hashed_password, free_plan_id, str(region), date_of_birth))

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
    result, status_code = register_user_logic(data)
    return jsonify(result), status_code


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

@app.route("/update/user/<uuid:user_id>", methods=["POST"])
@token_required
@cross_origin()
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
@cross_origin()
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
@cross_origin()
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
@cross_origin()
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
@cross_origin()
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
@cross_origin()
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
@cross_origin()
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

@app.route("/movies/fav/<uuid:user_id>", methods=["GET"])
@token_required
@cross_origin()
def get_user_fav_movies(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            m.movie_id,
            m.movie_name,
            amd.movie_poster
        FROM "FAVOURITE_MOVIES" fm
        JOIN "MOVIES" m ON fm.movie_id = m.movie_id
        LEFT JOIN "ADDITIONAL_MOVIE_DATA" amd ON amd.movie_id = m.movie_id
        WHERE fm.user_id = %s
    """, (str(user_id),))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    movies = []
    for row in rows:
        movie_id, movie_name, poster_bytes = row
        poster_base64 = base64.b64encode(poster_bytes).decode("utf-8") if poster_bytes else None
        movies.append({
            "movie_id": str(movie_id),
            "movie_name": movie_name,
            "movie_poster": poster_base64,
        })

    return jsonify(movies), 200

@app.route("/movies/fav/add", methods=["POST"])
@token_required
@cross_origin()
def add_movie_to_favorites():
    data = request.get_json()
    user_id = data.get("user_id")
    movie_id = data.get("movie_id")

    if not user_id or not movie_id:
        return jsonify({"error": "Missing data"}), 400

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO "FAVOURITE_MOVIES" (user_id, movie_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """, (user_id, movie_id))

    conn.commit()

    inserted = cur.rowcount

    cur.close()
    conn.close()

    if inserted == 0:
        return jsonify({"message": "Already in favourites"}), 409

    return jsonify({"message": "Added to favourites"}), 200

@app.route("/movies/fav/remove", methods=["POST"])
@token_required
@cross_origin()
def remove_movie_from_favorites():
    data = request.get_json()
    user_id = data.get("user_id")
    movie_id = data.get("movie_id")

    if not user_id or not movie_id:
        return jsonify({"error": "Missing data"}), 400

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM "FAVOURITE_MOVIES"
        WHERE user_id = %s AND movie_id = %s
    """, (user_id, movie_id))

    conn.commit()

    deleted = cur.rowcount   # how many rows deleted

    cur.close()
    conn.close()

    if deleted == 0:
        return jsonify({"message": "Movie not found in favourites"}), 404

    return jsonify({"message": "Removed from favourites"}), 200

@app.route("/movies/fav/check", methods=["POST"])
@cross_origin()
def is_movie_favorited():
    data = request.get_json()
    user_id = data.get("user_id")
    movie_id = data.get("movie_id")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 1 FROM "FAVOURITE_MOVIES"
        WHERE user_id = %s AND movie_id = %s
    """, (user_id, movie_id))

    exists = cur.fetchone() is not None

    cur.close()
    conn.close()

    return jsonify({"is_favorite": exists}), 200


# Endpoint /movies-with-directors
@app.route("/api/views/movies_with_directors", methods=["GET"])
@cross_origin()
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

@app.route("/add/movies", methods=["POST"])
@cross_origin()
def add_movie():
    data = request.get_json()

    movie_name = data.get("movie_name")
    movie_rating = data.get("movie_rating")
    movie_release_date = data.get("movie_release_date")
    movie_pg = data.get("movie_pg")
    movie_description = data.get("movie_description")

    new_movie_id = str(uuid.uuid4())

    actor_ids = list(filter(None, (data.get("actor_ids") or "").split(";")))
    director_ids = list(filter(None, (data.get("director_ids") or "").split(";")))
    genre_ids = list(filter(None, (data.get("genre_ids") or "").split(";")))

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO "MOVIES" 
            (movie_id, movie_name, movie_rating, movie_release_date, movie_pg, movie_description)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (new_movie_id, movie_name, movie_rating, movie_release_date, movie_pg, movie_description))

        for actor_id in actor_ids:
            cur.execute("""INSERT INTO "MOVIE_ACTORS" (movie_id, actor_id) VALUES (%s, %s)""",
                        (new_movie_id, actor_id))

        for director_id in director_ids:
            cur.execute("""INSERT INTO "MOVIE_DIRECTORS" (movie_id, director_id) VALUES (%s, %s)""",
                        (new_movie_id, director_id))

        for genre_id in genre_ids:
            cur.execute("""INSERT INTO "MOVIE_GENRES" (movie_id, genre_id) VALUES (%s, %s)""",
                        (new_movie_id, genre_id))

        cur.execute("""
                    INSERT INTO "ADDITIONAL_MOVIE_DATA"
                    (movie_id, movie_poster, movie_trailer, movie_language, movie_preview_poster)
                    VALUES (%s, %s, %s, %s, %s)
                    """, (new_movie_id,))

        conn.commit()
        return "", 200

    except Exception as e:
        conn.rollback()
        return "", 406

    finally:
        cur.close()
        conn.close()


@app.route("/update/movies/<uuid:movie_id>", methods=["POST"])
@cross_origin()
def update_movie(movie_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400


    allowed_fields = ["movie_name", "movie_rating", "movie_release_date", "movie_pg", "movie_description"]

    update_fields = {k: v for k, v in data.items() if k in allowed_fields}

    if not update_fields:
        return jsonify({"error": "No valid fields to update"}), 400

    set_clause = ", ".join([f"{k} = %s" for k in update_fields.keys()])
    values = list(update_fields.values())
    values.append(str(movie_id))

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(f"""
            UPDATE "MOVIES"
            SET {set_clause}
            WHERE movie_id = %s
        """, values)

        # if cur.rowcount == 0:
        #     return jsonify({"error": "Movie not found"}), 404

        conn.commit()
        cur.close()
        conn.close()

        return "", 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/update/additional_movie_data/<uuid:movie_id>", methods=["POST"])
@cross_origin()
def update_additional_movie_data(movie_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Allowed fields for updating
    allowed_fields = ["movie_poster", "movie_trailer", "movie_language", "movie_preview_poster"]

    update_fields = {}
    for k, v in data.items():
        if k in allowed_fields:
            if k in ["movie_poster", "movie_preview_poster"] and v:
                try:
                    update_fields[k] = base64.b64decode(v)
                except Exception:
                    return jsonify({"error": f"Invalid Base64 data for {k}"}), 400
            else:
                update_fields[k] = v

    if not update_fields:
        return jsonify({"error": "No valid fields to update"}), 400

    set_clause = ", ".join([f"{k} = %s" for k in update_fields.keys()])
    values = list(update_fields.values())
    values.append(str(movie_id))

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(f"""
            UPDATE "ADDITIONAL_MOVIE_DATA"
            SET {set_clause}
            WHERE movie_id = %s
        """, values)

        if cur.rowcount == 0:
            return jsonify({"error": "Movie not found"}), 404

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Additional movie data updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/movie_test/<uuid:movie_id>", methods=["GET"])
@cross_origin()
def movie_test(movie_id):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT movie_id, movie_name, movie_rating, movie_release_date, movie_pg, movie_description
            FROM "MOVIES"
            WHERE movie_id = %s
        """, (str(movie_id),))
        movie = cur.fetchone()

        if not movie:
            return "", 404

        movie_data = {
            "movie_id": movie[0],
            "movie_name": movie[1],
            "movie_rating": movie[2],
            "movie_release_date": movie[3],
            "movie_pg": movie[4],
            "movie_description": movie[5],
            "actors": [],
            "directors": [],
            "genres": []
        }

        cur.execute("""
            SELECT a.actor_id, a.first_name, a.middle_name, a.last_name
            FROM "MOVIE_ACTORS" ma
            JOIN "ACTORS" a ON ma.actor_id = a.actor_id
            WHERE ma.movie_id = %s
        """, (str(movie_id),))
        movie_data["actors"] = [
            {"actor_id": r[0], "name": " ".join(filter(None, [r[1], r[2], r[3]]))}
            for r in cur.fetchall()
        ]

        cur.execute("""
            SELECT d.director_id, d.first_name, d.middle_name, d.last_name
            FROM "MOVIE_DIRECTORS" md
            JOIN "DIRECTORS" d ON md.director_id = d.director_id
            WHERE md.movie_id = %s
        """, (str(movie_id),))
        movie_data["directors"] = [
            {"director_id": r[0], "name": " ".join(filter(None, [r[1], r[2], r[3]]))}
            for r in cur.fetchall()
        ]

        cur.execute("""
            SELECT g.genre_id, g.genre_name
            FROM "MOVIE_GENRES" mg
            JOIN "GENRES" g ON mg.genre_id = g.genre_id
            WHERE mg.movie_id = %s
        """, (str(movie_id),))
        movie_data["genres"] = [
            {"genre_id": r[0], "name": r[1]} for r in cur.fetchall()
        ]

        return jsonify(movie_data), 200

    finally:
        cur.close()
        conn.close()

@app.route("/entity/actor/<string:name>", methods=["GET"])
@cross_origin()
def get_actor_with_movies(name):
    conn = get_connection()
    cur = conn.cursor()

    # actor info
    cur.execute("""
        SELECT actor_id, first_name, last_name, birthplace
        FROM "ACTORS"
        WHERE CONCAT(first_name, ' ', last_name) = %s
        LIMIT 1
    """, (name,))

    actor = cur.fetchone()
    if not actor:
        return jsonify(None), 404

    actor_id, first_name, last_name, birthplace = actor

    # movies
    cur.execute("""
        SELECT m.movie_id, m.movie_name
        FROM "MOVIE_ACTORS" ma
        JOIN "MOVIES" m ON m.movie_id = ma.movie_id
        WHERE ma.actor_id = %s
    """, (actor_id,))

    movies = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify({
        "id": str(actor_id),
        "name": f"{first_name} {last_name}",
        "birthplace": birthplace,
        "movies": [
            {
                "movie_id": str(m[0]),
                "movie_name": m[1]
            } for m in movies
        ]
    }), 200

@app.route("/entity/director/<string:name>", methods=["GET"])
@cross_origin()
def get_director_with_movies(name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT director_id, first_name, last_name, birthplace
        FROM "DIRECTORS"
        WHERE CONCAT(first_name, ' ', last_name) = %s
        LIMIT 1
    """, (name,))

    director = cur.fetchone()
    if not director:
        return jsonify(None), 404

    director_id, first_name, last_name, birthplace = director

    cur.execute("""
        SELECT m.movie_id, m.movie_name
        FROM "MOVIE_DIRECTORS" md
        JOIN "MOVIES" m ON m.movie_id = md.movie_id
        WHERE md.director_id = %s
    """, (director_id,))

    movies = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify({
        "id": str(director_id),
        "name": f"{first_name} {last_name}",
        "birthplace": birthplace,
        "movies": [
            {
                "movie_id": str(m[0]),
                "movie_name": m[1]
            } for m in movies
        ]
    }), 200

@app.route("/entity/genre/<string:name>", methods=["GET"])
@cross_origin()
def get_genre_with_movies(name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT genre_id, genre_name, genre_description
        FROM "GENRES"
        WHERE genre_name = %s
        LIMIT 1
    """, (name,))

    genre = cur.fetchone()
    if not genre:
        return jsonify(None), 404

    genre_id, genre_name, genre_description = genre

    cur.execute("""
        SELECT m.movie_id, m.movie_name
        FROM "MOVIE_GENRES" mg
        JOIN "MOVIES" m ON m.movie_id = mg.movie_id
        WHERE mg.genre_id = %s
    """, (genre_id,))

    movies = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify({
        "id": str(genre_id),
        "name": genre_name,
        "description": genre_description,
        "movies": [
            {
                "movie_id": str(m[0]),
                "movie_name": m[1]
            } for m in movies
        ]
    }), 200





@app.route("/search/actors", methods=["GET"])
@cross_origin()
def get_search_actors():
    return search_entities("ACTORS")

@app.route("/search/directors", methods=["GET"])
@cross_origin()
def get_search_directors():
    return search_entities("DIRECTORS")

@app.route("/search/users", methods=["GET"])
@token_required
@cross_origin()
def get_search_users():
    return search_entities("USERS")

@app.route("/search/movies", methods=["GET"])
@cross_origin()
def get_search_movies():
    return search_entities("MOVIES")

# Uruchomienie serwera
if __name__ == "__main__":
    app.run(debug=True)
