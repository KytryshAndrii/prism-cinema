import base64
import uuid
from utils.connection import get_connection

def get_movies_logic(limit=50):
    """
    Returns a list of movies with poster (base64).
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT
                m.movie_id,
                m.movie_name,
                amd.movie_poster,
                amd.movie_preview_poster
            FROM "MOVIES" m
            LEFT JOIN "ADDITIONAL_MOVIE_DATA" amd
                ON amd.movie_id = m.movie_id
            LIMIT %s
        """, (limit,))

        rows = cur.fetchall()
        movies = []

        for row in rows:
            movie_id, movie_name, poster_bytes, _ = row

            poster_base64 = (
                base64.b64encode(poster_bytes).decode("utf-8")
                if poster_bytes else None
            )

            movies.append({
                "movie_id": str(movie_id),
                "movie_name": movie_name,
                "movie_poster": poster_base64
            })

        return movies
    finally:
        cur.close()
        conn.close()


def get_movie_details_logic(movie_id):
    """
    Returns detailed info for a single movie, including genres, actors, directors.
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        # 1. Movie basic info + trailer
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
            return {"error": "Movie not found"}, 404

        description, rating, pg, release_date, trailer_url, movie_poster, movie_preview_poster = movie_data

        # 2. Genres
        cur.execute("""
            SELECT g.genre_name
            FROM "MOVIE_GENRES" mg
            JOIN "GENRES" g ON mg.genre_id = g.genre_id
            WHERE mg.movie_id = %s
        """, (str(movie_id),))
        genres = [row[0] for row in cur.fetchall()]

        # 3. Actors
        cur.execute("""
            SELECT a.first_name, a.last_name
            FROM "MOVIE_ACTORS" ma
            JOIN "ACTORS" a ON ma.actor_id = a.actor_id
            WHERE ma.movie_id = %s
        """, (str(movie_id),))
        actors = [f"{row[0]} {row[1]}" for row in cur.fetchall()]

        # 4. Directors
        cur.execute("""
            SELECT d.first_name, d.last_name
            FROM "MOVIE_DIRECTORS" md
            JOIN "DIRECTORS" d ON md.director_id = d.director_id
            WHERE md.movie_id = %s
        """, (str(movie_id),))
        directors = [f"{row[0]} {row[1]}" for row in cur.fetchall()]

        # Convert posters to base64
        poster_base64 = (
            base64.b64encode(movie_poster).decode("utf-8") if movie_poster else None
        )
        preview_poster_base64 = (
            base64.b64encode(movie_preview_poster).decode("utf-8") if movie_preview_poster else None
        )

        return {
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
        }, 200
    finally:
        cur.close()
        conn.close()


def get_user_fav_movies_logic(user_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
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
        movies = []
        for row in rows:
            movie_id, movie_name, poster_bytes = row
            poster_base64 = (
                base64.b64encode(poster_bytes).decode("utf-8") if poster_bytes else None
            )
            movies.append({
                "movie_id": str(movie_id),
                "movie_name": movie_name,
                "movie_poster": poster_base64
            })
        return movies
    finally:
        cur.close()
        conn.close()


def add_movie_to_favorites_logic(user_id, movie_id):
    if not user_id or not movie_id:
        return {"error": "Missing data"}, 400

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO "FAVOURITE_MOVIES" (user_id, movie_id)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
        """, (user_id, movie_id))
        conn.commit()
        inserted = cur.rowcount
        if inserted == 0:
            return {"message": "Already in favourites"}, 409
        return {"message": "Added to favourites"}, 200
    finally:
        cur.close()
        conn.close()


def remove_movie_from_favorites_logic(user_id, movie_id):
    if not user_id or not movie_id:
        return {"error": "Missing data"}, 400

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            DELETE FROM "FAVOURITE_MOVIES"
            WHERE user_id = %s AND movie_id = %s
        """, (user_id, movie_id))
        conn.commit()
        deleted = cur.rowcount
        if deleted == 0:
            return {"message": "Movie not found in favourites"}, 404
        return {"message": "Removed from favourites"}, 200
    finally:
        cur.close()
        conn.close()


def is_movie_favorited_logic(user_id, movie_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT 1 FROM "FAVOURITE_MOVIES"
            WHERE user_id = %s AND movie_id = %s
        """, (user_id, movie_id))
        exists = cur.fetchone() is not None
        return {"is_favorite": exists}, 200
    finally:
        cur.close()
        conn.close()


def get_movies_with_directors_logic(limit=50):
    """
    Returns movies with their directors from the MOVIES_WITH_DIRECTORS view.
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT *
            FROM MOVIES_WITH_DIRECTORS
            LIMIT %s
        """, (limit,))
        rows = cur.fetchall()

        movies = []
        for row in rows:
            movies.append({
                "movie_title": row[0],
                "directors": row[1]
            })
        return movies
    finally:
        cur.close()
        conn.close()


def add_movie_logic(data):
    """
    Adds a new movie, its actors, directors, genres, and additional movie data.
    """
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
        # Main movie table
        cur.execute("""
            INSERT INTO "MOVIES" 
            (movie_id, movie_name, movie_rating, movie_release_date, movie_pg, movie_description)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (new_movie_id, movie_name, movie_rating, movie_release_date, movie_pg, movie_description))

        # Actors
        for actor_id in actor_ids:
            cur.execute("""
                INSERT INTO "MOVIE_ACTORS" (movie_id, actor_id) VALUES (%s, %s)
            """, (new_movie_id, actor_id))

        # Directors
        for director_id in director_ids:
            cur.execute("""
                INSERT INTO "MOVIE_DIRECTORS" (movie_id, director_id) VALUES (%s, %s)
            """, (new_movie_id, director_id))

        # Genres
        for genre_id in genre_ids:
            cur.execute("""
                INSERT INTO "MOVIE_GENRES" (movie_id, genre_id) VALUES (%s, %s)
            """, (new_movie_id, genre_id))

        # Additional movie data
        cur.execute("""
            INSERT INTO "ADDITIONAL_MOVIE_DATA" (movie_id)
            VALUES (%s)
        """, (new_movie_id,))

        conn.commit()
        return {"movie_id": new_movie_id}, 200

    except Exception as e:
        conn.rollback()
        return {"error": str(e)}, 500

    finally:
        cur.close()
        conn.close()


def update_movie_logic(movie_id, data):
    """
    Updates main MOVIES table fields.
    """
    allowed_fields = ["movie_name", "movie_rating", "movie_release_date", "movie_pg", "movie_description"]
    update_fields = {k: v for k, v in data.items() if k in allowed_fields}

    if not update_fields:
        return {"error": "No valid fields to update"}, 400

    set_clause = ", ".join([f"{k} = %s" for k in update_fields.keys()])
    values = list(update_fields.values()) + [str(movie_id)]

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(f"""
            UPDATE "MOVIES"
            SET {set_clause}
            WHERE movie_id = %s
        """, values)
        conn.commit()
        return {"message": "Movie updated successfully"}, 200
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        cur.close()
        conn.close()


def update_additional_movie_data_logic(movie_id, data):
    """
    Updates fields in ADDITIONAL_MOVIE_DATA.
    """
    allowed_fields = ["movie_poster", "movie_trailer", "movie_language", "movie_preview_poster"]
    update_fields = {}

    for k, v in data.items():
        if k in allowed_fields:
            if k in ["movie_poster", "movie_preview_poster"] and v:
                try:
                    update_fields[k] = base64.b64decode(v)
                except Exception:
                    return {"error": f"Invalid Base64 data for {k}"}, 400
            else:
                update_fields[k] = v

    if not update_fields:
        return {"error": "No valid fields to update"}, 400

    set_clause = ", ".join([f"{k} = %s" for k in update_fields.keys()])
    values = list(update_fields.values()) + [str(movie_id)]

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(f"""
            UPDATE "ADDITIONAL_MOVIE_DATA"
            SET {set_clause}
            WHERE movie_id = %s
        """, values)

        if cur.rowcount == 0:
            return {"error": "Movie not found"}, 404

        conn.commit()
        return {"message": "Additional movie data updated successfully"}, 200

    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        cur.close()
        conn.close()


def get_movie_test_logic(movie_id):
    """
    Returns full movie info including actors, directors, and genres.
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        # Main movie info
        cur.execute("""
            SELECT movie_id, movie_name, movie_rating, movie_release_date, movie_pg, movie_description
            FROM "MOVIES"
            WHERE movie_id = %s
        """, (str(movie_id),))
        movie = cur.fetchone()

        if not movie:
            return None, 404

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

        # Actors
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

        # Directors
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

        # Genres
        cur.execute("""
            SELECT g.genre_id, g.genre_name
            FROM "MOVIE_GENRES" mg
            JOIN "GENRES" g ON mg.genre_id = g.genre_id
            WHERE mg.movie_id = %s
        """, (str(movie_id),))
        movie_data["genres"] = [
            {"genre_id": r[0], "name": r[1]} for r in cur.fetchall()
        ]

        return movie_data, 200

    finally:
        cur.close()
        conn.close()