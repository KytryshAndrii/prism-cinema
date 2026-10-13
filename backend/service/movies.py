import base64
import json
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

    movie_poster = data.get("movie_poster")
    movie_trailer = data.get("movie_trailer")
    movie_language = data.get("movie_language")
    movie_preview_poster = data.get("movie_preview_poster")

    movie_subtitles_language = data.get("movie_subtitles_language")
    movie_subtitles = data.get("movie_subtitles")

    movie_license_id = data.get("license_id")

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
                INSERT INTO "ADDITIONAL_MOVIE_DATA" (movie_id, movie_poster, movie_trailer,
                                                 movie_language, movie_preview_poster)
                VALUES (%s, %s, %s, %s, %s)
        """, (new_movie_id, movie_poster, movie_trailer,
              movie_language, movie_preview_poster))

        cur.execute("""
                    INSERT INTO "MOVIE_LOCALIZATIONS" (movie_id, subtitles_language, subtitles)
                    VALUES (%s, %s, %s)
                    """, (
                        new_movie_id,
                        movie_subtitles_language,
                        json.dumps(movie_subtitles)
                    ))

        cur.execute("""
                    INSERT INTO "MOVIE_LICENSES" (movie_id, license_id)
                    VALUES (%s, %s)
                    """, (new_movie_id, movie_license_id))

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
    Updates main MOVIES table fields. Only updates provided fields.
    """
    fields = {
        "movie_name": data.get("movie_name"),
        "movie_rating": data.get("movie_rating"),
        "movie_release_date": data.get("movie_release_date"),
        "movie_pg": data.get("movie_pg"),
        "movie_description": data.get("movie_description"),
    }

    # Filter out None values to avoid overwriting
    fields_to_update = {k: v for k, v in fields.items() if v is not None}
    if not fields_to_update:
        return {"message": "No fields to update"}, 400

    set_clause = ", ".join(f'{k} = %s' for k in fields_to_update.keys())
    values = list(fields_to_update.values())
    values.append(movie_id)

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(f"""
            UPDATE "MOVIES"
            SET {set_clause}
            WHERE movie_id = %s
        """, values)
        conn.commit()
        return {"message": "Movie updated"}, 200
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}, 500
    finally:
        cur.close()
        conn.close()



def update_movie_actors_logic(movie_id, data):
    movie_id_str = str(movie_id)

    new_actor_ids = set(filter(None, (data.get("actor_ids") or "").split(";")))
    if not new_actor_ids:
        return {"message": "No actors provided"}, 400

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""SELECT actor_id FROM "MOVIE_ACTORS" WHERE movie_id = %s""", (movie_id_str,))
        existing_actor_ids = set(row[0] for row in cur.fetchall())

        to_add = new_actor_ids - existing_actor_ids
        to_remove = existing_actor_ids - new_actor_ids

        for actor_id in to_add:
            cur.execute("""INSERT INTO "MOVIE_ACTORS" (movie_id, actor_id) VALUES (%s, %s)""", (movie_id_str, actor_id))

        for actor_id in to_remove:
            cur.execute("""DELETE FROM "MOVIE_ACTORS" WHERE movie_id = %s AND actor_id = %s""", (movie_id_str, actor_id))

        conn.commit()
        return {"message": "Movie actors updated"}, 200
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}, 500
    finally:
        cur.close()
        conn.close()



def update_movie_directors_logic(movie_id, data):
    movie_id_str = str(movie_id)
    new_director_ids = set(filter(None, (data.get("director_ids") or "").split(";")))
    if not new_director_ids:
        return {"message": "No directors provided"}, 400

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""SELECT director_id FROM "MOVIE_DIRECTORS" WHERE movie_id = %s""", (movie_id_str,))
        existing_director_ids = set(row[0] for row in cur.fetchall())

        to_add = new_director_ids - existing_director_ids
        to_remove = existing_director_ids - new_director_ids

        for director_id in to_add:
            cur.execute("""INSERT INTO "MOVIE_DIRECTORS" (movie_id, director_id) VALUES (%s, %s)""",
                        (movie_id_str, director_id))
        for director_id in to_remove:
            cur.execute("""DELETE FROM "MOVIE_DIRECTORS" WHERE movie_id = %s AND director_id = %s""",
                        (movie_id_str, director_id))

        conn.commit()
        return {"message": "Movie directors updated"}, 200
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}, 500
    finally:
        cur.close()
        conn.close()



def update_movie_genres_logic(movie_id, data):
    movie_id_str = str(movie_id)
    new_genre_ids = set(filter(None, (data.get("genre_ids") or "").split(";")))
    if not new_genre_ids:
        return {"message": "No genres provided"}, 400

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""SELECT genre_id FROM "MOVIE_GENRES" WHERE movie_id = %s""", (movie_id_str,))
        existing_genre_ids = set(row[0] for row in cur.fetchall())

        to_add = new_genre_ids - existing_genre_ids
        to_remove = existing_genre_ids - new_genre_ids

        for genre_id in to_add:
            cur.execute("""INSERT INTO "MOVIE_GENRES" (movie_id, genre_id) VALUES (%s, %s)""",
                        (movie_id_str, genre_id))
        for genre_id in to_remove:
            cur.execute("""DELETE FROM "MOVIE_GENRES" WHERE movie_id = %s AND genre_id = %s""",
                        (movie_id_str, genre_id))

        conn.commit()
        return {"message": "Movie genres updated"}, 200
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}, 500
    finally:
        cur.close()
        conn.close()



def update_additional_movie_data_logic(movie_id, data):
    movie_id_str = str(movie_id)  # convert UUID to string
    fields = {
        "movie_poster": data.get("movie_poster"),
        "movie_trailer": data.get("movie_trailer"),
        "movie_language": data.get("movie_language"),
        "movie_preview_poster": data.get("movie_preview_poster"),
    }

    fields_to_update = {k: v for k, v in fields.items() if v is not None}
    if not fields_to_update:
        return {"message": "No additional data to update"}, 400

    set_clause = ", ".join(f'{k} = %s' for k in fields_to_update.keys())
    values = list(fields_to_update.values())
    values.append(movie_id_str)

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(f"""
            UPDATE "ADDITIONAL_MOVIE_DATA"
            SET {set_clause}
            WHERE movie_id = %s
        """, values)
        conn.commit()
        return {"message": "Additional movie data updated"}, 200
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}, 500
    finally:
        cur.close()
        conn.close()



def update_movie_localizations_logic(movie_id, data):
    movie_id_str = str(movie_id)  # convert UUID to string
    localizations = data.get("localizations")
    if not localizations:
        return {"message": "No localizations provided"}, 400

    new_languages = {loc["subtitles_language"] for loc in localizations}

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT subtitles_language
            FROM "MOVIE_LOCALIZATIONS"
            WHERE movie_id = %s
        """, (movie_id_str,))
        existing_languages = {row[0] for row in cur.fetchall()}

        to_add = new_languages - existing_languages
        to_update = new_languages & existing_languages
        to_remove = existing_languages - new_languages

        for loc in localizations:
            if loc["subtitles_language"] in to_add:
                cur.execute("""
                    INSERT INTO "MOVIE_LOCALIZATIONS"
                    (movie_id, subtitles_language, subtitles)
                    VALUES (%s, %s, %s)
                """, (
                    movie_id_str,
                    loc["subtitles_language"],
                    json.dumps(loc["subtitles"])  # convert dict to JSON
                ))

        for loc in localizations:
            if loc["subtitles_language"] in to_update:
                cur.execute("""
                    UPDATE "MOVIE_LOCALIZATIONS"
                    SET subtitles = %s
                    WHERE movie_id = %s AND subtitles_language = %s
                """, (
                    json.dumps(loc["subtitles"]),  # convert dict to JSON
                    movie_id_str,
                    loc["subtitles_language"]
                ))

        for language in to_remove:
            cur.execute("""
                DELETE FROM "MOVIE_LOCALIZATIONS"
                WHERE movie_id = %s AND subtitles_language = %s
            """, (movie_id_str, language))

        conn.commit()
        return {"message": "Movie localizations updated"}, 200

    except Exception as e:
        conn.rollback()
        return {"error": str(e)}, 500
    finally:
        cur.close()
        conn.close()


def update_movie_licenses_logic(movie_id, data):
    """
    Syncs MOVIE_LICENSES table.
    """
    movie_id_str = str(movie_id)  # convert UUID to string
    new_license_ids = set(filter(None, (data.get("license_ids") or "").split(";")))
    if not new_license_ids:
        return {"message": "No licenses provided"}, 400

    conn = get_connection()
    cur = conn.cursor()
    try:
        # Get existing licenses
        cur.execute("""
            SELECT license_id
            FROM "MOVIE_LICENSES"
            WHERE movie_id = %s
        """, (movie_id_str,))
        existing_license_ids = {row[0] for row in cur.fetchall()}

        to_add = new_license_ids - existing_license_ids
        to_remove = existing_license_ids - new_license_ids

        # Insert new licenses
        for license_id in to_add:
            cur.execute("""
                INSERT INTO "MOVIE_LICENSES" (movie_id, license_id)
                VALUES (%s, %s)
            """, (movie_id_str, str(license_id)))  # convert license_id if UUID

        # Remove old licenses
        for license_id in to_remove:
            cur.execute("""
                DELETE FROM "MOVIE_LICENSES"
                WHERE movie_id = %s AND license_id = %s
            """, (movie_id_str, str(license_id)))  # convert license_id if UUID

        conn.commit()
        return {"message": "Movie licenses updated"}, 200

    except Exception as e:
        conn.rollback()
        return {"error": str(e)}, 500
    finally:
        cur.close()
        conn.close()


def delete_movie_logic(movie_id):
    """
    Hard-deletes a movie and all related data via ON DELETE CASCADE.
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""DELETE FROM "MOVIES" WHERE movie_id = %s""", (str(movie_id),))

        if cur.rowcount == 0:
            conn.rollback()
            return {"message": "Movie not found"}, 404

        conn.commit()
        return {"message": "Movie deleted successfully"}, 200

    except Exception as e:
        conn.rollback()
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

        return movie_data, 200

    finally:
        cur.close()
        conn.close()