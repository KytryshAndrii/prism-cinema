from flask import Flask, jsonify
from db.connection import get_connection

app = Flask(__name__)

# Endpoint testowy /health
@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}

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
