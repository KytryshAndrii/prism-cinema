from db.connection import conn
import random

user_id = "1446e48b-6951-43ed-bc83-73f5f85f57ca" # must be actual user id

# Lista nazw ulubionych filmów tego użytkownika
favorite_movie_titles = [
    "The Shawshank Redemption",
    "The Godfather",
    "Inception",
    "Fight Club"
]

movie_director_map = {
    "The Shawshank Redemption": ("Frank", "", "Darabont"),
    "The Godfather": ("Francis", "Ford", "Coppola"),
    "The Dark Knight": ("Christopher", "", "Nolan"),
    "12 Angry Men": ("Sidney", "", "Lumet"),
    "Schindler's List": ("Steven", "", "Spielberg"),
    "The Lord of the Rings: The Return of the King": ("Peter", "", "Jackson"),
    "Pulp Fiction": ("Quentin", "", "Tarantino"),
    "Forrest Gump": ("Robert", "", "Zemeckis"),
    "Inception": ("Christopher", "", "Nolan"),
    "Fight Club": ("David", "", "Fincher"),
}

movie_actor_map = {
    "The Shawshank Redemption": [("Tim", "", "Robbins"), ("Morgan", "", "Freeman")],
    "The Godfather": [("Marlon", "", "Brando"), ("Al", "", "Pacino")],
    "The Dark Knight": [("Christian", "", "Bale"), ("Heath", "", "Ledger")],
    "12 Angry Men": [("Henry", "", "Fonda"), ("Lee", "J.", "Cobb")],
    "Schindler's List": [("Liam", "", "Neeson"), ("Ralph", "", "Fiennes")],
    "The Lord of the Rings: The Return of the King": [("Elijah", "", "Wood"), ("Viggo", "", "Mortensen")],
    "Pulp Fiction": [("John", "", "Travolta"), ("Samuel", "L.", "Jackson")],
    "Forrest Gump": [("Tom", "", "Hanks"), ("Robin", "", "Wright")],
    "Inception": [("Leonardo", "", "DiCaprio"), ("Joseph", "Gordon", "Levitt")],
    "Fight Club": [("Edward", "", "Norton"), ("Brad", "", "Pitt")],
}

movie_genre_map = {
    "The Shawshank Redemption": ["Drama", "Crime"],
    "The Godfather": ["Drama", "Crime"],
    "The Dark Knight": ["Action", "Crime", "Drama"],
    "12 Angry Men": ["Drama"],
    "Schindler's List": ["Drama", "Biography", "History"],
    "The Lord of the Rings: The Return of the King": ["Action", "Adventure", "Fantasy"],
    "Pulp Fiction": ["Crime", "Drama"],
    "Forrest Gump": ["Drama", "Romance"],
    "Inception": ["Action", "Sci-Fi"],
    "Fight Club": ["Drama"],
}


def insert_dumb_data_fav_movies_join_tables():
    cur = conn.cursor()
    for title in favorite_movie_titles:
        # Pobierz movie_id z tabeli MOVIES na podstawie tytułu
        cur.execute("""
                SELECT movie_id FROM "MOVIES" WHERE movie_name = %s
            """, (title,))
        result = cur.fetchone()

        if result:
            movie_id = result[0]

            # Dodaj wpis do FAVOURITE_MOVIES
            cur.execute("""
                    INSERT INTO "FAVOURITE_MOVIES" (user_id, movie_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING;
                """, (str(user_id), str(movie_id)))

            print(f"✅ Dodano do ulubionych: {title}")
        else:
            print(f"⚠️ Film nie znaleziony w bazie: {title}")

    conn.commit()
    cur.close()
    conn.close()
    print("\n🎉 Ukończono przypisanie ulubionych filmów.")


def insert_dumb_data_directors_join_tables():
    cur = conn.cursor()

    for movie_title, (first, middle, last) in movie_director_map.items():
        # Pobierz movie_id
        cur.execute("""
            SELECT movie_id FROM "MOVIES" WHERE movie_name = %s
        """, (movie_title,))
        movie_result = cur.fetchone()

        if not movie_result:
            print(f"⚠️ Film nie znaleziony: {movie_title}")
            continue

        movie_id = movie_result[0]

        # Pobierz director_id
        cur.execute("""
            SELECT director_id FROM "DIRECTORS"
            WHERE first_name = %s AND last_name = %s
        """, (first, last))
        director_result = cur.fetchone()

        if not director_result:
            print(f"⚠️ Reżyser nie znaleziony: {first} {middle} {last}")
            continue

        director_id = director_result[0]

        # Wstaw do tabeli MOVIE_DIRECTORS
        cur.execute("""
            INSERT INTO "MOVIE_DIRECTORS" (movie_id, director_id)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING;
        """, (movie_id, director_id))

        print(f"✅ Dodano powiązanie: {movie_title} → {first} {middle} {last}")

    conn.commit()
    cur.close()
    conn.close()
    print("\n🎉 Ukończono przypisanie reżyserów do filmów.")

def insert_dumb_data_actors_join_tables():
    cur = conn.cursor()

    for movie_title, actors in movie_actor_map.items():
        # Pobierz movie_id
        cur.execute("""SELECT movie_id FROM "MOVIES" WHERE movie_name = %s""", (movie_title,))
        movie_result = cur.fetchone()

        if not movie_result:
            print(f"⚠️ Film nie znaleziony: {movie_title}")
            continue

        movie_id = movie_result[0]

        for first, middle, last in actors:
            # Pobierz actor_id
            cur.execute("""
                   SELECT actor_id FROM "ACTORS"
                   WHERE first_name = %s AND last_name = %s
               """, (first, last))
            actor_result = cur.fetchone()

            if not actor_result:
                print(f"⚠️ Aktor nie znaleziony: {first} {middle} {last}")
                continue

            actor_id = actor_result[0]

            # Dodaj powiązanie do tabeli pośredniej MOVIE_ACTORS
            cur.execute("""
                   INSERT INTO "MOVIE_ACTORS" (movie_id, actor_id)
                   VALUES (%s, %s)
                   ON CONFLICT DO NOTHING;
               """, (movie_id, actor_id))

            print(f"✅ Dodano aktora do filmu: {movie_title} ← {first} {middle} {last}")

    conn.commit()
    cur.close()
    conn.close()
    print("\n🎉 Ukończono przypisanie aktorów do filmów.")


def insert_dumb_data_genres_join_tables():
    cur = conn.cursor()

    for movie_title, genres in movie_genre_map.items():
        # Pobierz movie_id
        cur.execute("""SELECT movie_id FROM "MOVIES" WHERE movie_name = %s""", (movie_title,))
        movie_result = cur.fetchone()

        if not movie_result:
            print(f"⚠️ Film nie znaleziony: {movie_title}")
            continue

        movie_id = movie_result[0]

        for genre_name in genres:
            # Pobierz genre_id
            cur.execute("""SELECT genre_id FROM "GENRES" WHERE genre_name = %s""", (genre_name,))
            genre_result = cur.fetchone()

            if not genre_result:
                print(f"⚠️ Gatunek nie znaleziony: {genre_name}")
                continue

            genre_id = genre_result[0]

            # Dodaj powiązanie do tabeli MOVIE_GENRES
            cur.execute("""
                   INSERT INTO "MOVIE_GENRES" (movie_id, genre_id)
                   VALUES (%s, %s)
                   ON CONFLICT DO NOTHING;
               """, (movie_id, genre_id))

            print(f"✅ Przypisano gatunek {genre_name} → {movie_title}")

    conn.commit()
    cur.close()
    conn.close()
    print("\n🎉 Ukończono przypisanie gatunków do filmów.")


def insert_dumb_data_licenses_join_tables():
    cur = conn.cursor()

    # Pobierz wszystkie ID filmów
    cur.execute("""SELECT movie_id, movie_name FROM "MOVIES";""")
    movies = cur.fetchall()  # lista krotek (movie_id, name)

    # Pobierz wszystkie ID licencji
    cur.execute("""SELECT license_id, license_region FROM "LICENSES";""")
    licenses = cur.fetchall()  # lista krotek (license_id, region)

    for movie_id, name in movies:
        # Wybierz losową liczbę licencji (1 do 3) dla filmu
        random_licenses = random.sample(licenses, k=random.randint(1, 3))

        for license_id, region in random_licenses:
            cur.execute("""
                    INSERT INTO "MOVIE_LICENSES" (movie_id, license_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING;
                """, (movie_id, license_id))

        print(f"🎞️ Przypisano licencje do filmu: {name}")

    conn.commit()
    cur.close()
    conn.close()
    print("\n✅ Ukończono przypisywanie licencji do filmów.")