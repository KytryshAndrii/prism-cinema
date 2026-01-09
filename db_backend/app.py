from flask import Flask, jsonify
from db.connection import get_connection

app = Flask(__name__)

# Endpoint testowy /health
@app.route("/api/health", methods=["GET"])
def health():
    return {"status": "ok"}

# Endpoint /users
@app.route("/api/users", methods=["GET"])
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

# Endpoint /movies-with-directors
@app.route("/api/views/movies-with-directors", methods=["GET"])
def movies_with_directors():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            movie_id,
            movie_name,
            movie_release_date,
            director_name
        FROM movies_with_directors
        LIMIT 50
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    movies = []
    for row in rows:
        movies.append({
            "movieId": str(row[0]),
            "title": row[1],
            "releaseDate": str(row[2]) if row[2] else None,
            "director": row[3]
        })

    return jsonify(movies)

# Uruchomienie serwera
if __name__ == "__main__":
    app.run(debug=True)
