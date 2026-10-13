from utils.connection import get_connection


def get_actor_with_movies_logic(name):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT actor_id, first_name, last_name, birthplace
            FROM "ACTORS"
            WHERE CONCAT(first_name, ' ', last_name) = %s
            LIMIT 1
        """, (name,))
        actor = cur.fetchone()
        if not actor:
            return None, 404
        actor_id, first_name, last_name, birthplace = actor

        cur.execute("""
            SELECT m.movie_id, m.movie_name
            FROM "MOVIE_ACTORS" ma
            JOIN "MOVIES" m ON m.movie_id = ma.movie_id
            WHERE ma.actor_id = %s
        """, (actor_id,))
        movies = [{"movie_id": str(m[0]), "movie_name": m[1]} for m in cur.fetchall()]

        return {
            "id": str(actor_id),
            "name": f"{first_name} {last_name}",
            "birthplace": birthplace,
            "movies": movies
        }, 200
    finally:
        cur.close()
        conn.close()


def get_director_with_movies_logic(name):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT director_id, first_name, last_name, birthplace
            FROM "DIRECTORS"
            WHERE CONCAT(first_name, ' ', last_name) = %s
            LIMIT 1
        """, (name,))
        director = cur.fetchone()
        if not director:
            return None, 404
        director_id, first_name, last_name, birthplace = director

        cur.execute("""
            SELECT m.movie_id, m.movie_name
            FROM "MOVIE_DIRECTORS" md
            JOIN "MOVIES" m ON m.movie_id = md.movie_id
            WHERE md.director_id = %s
        """, (director_id,))
        movies = [{"movie_id": str(m[0]), "movie_name": m[1]} for m in cur.fetchall()]

        return {
            "id": str(director_id),
            "name": f"{first_name} {last_name}",
            "birthplace": birthplace,
            "movies": movies
        }, 200
    finally:
        cur.close()
        conn.close()


def get_genre_with_movies_logic(name):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT genre_id, genre_name, genre_description
            FROM "GENRES"
            WHERE genre_name = %s
            LIMIT 1
        """, (name,))
        genre = cur.fetchone()
        if not genre:
            return None, 404
        genre_id, genre_name, genre_description = genre

        cur.execute("""
            SELECT m.movie_id, m.movie_name
            FROM "MOVIE_GENRES" mg
            JOIN "MOVIES" m ON m.movie_id = mg.movie_id
            WHERE mg.genre_id = %s
        """, (genre_id,))
        movies = [{"movie_id": str(m[0]), "movie_name": m[1]} for m in cur.fetchall()]

        return {
            "id": str(genre_id),
            "name": genre_name,
            "description": genre_description,
            "movies": movies
        }, 200
    finally:
        cur.close()
        conn.close()
