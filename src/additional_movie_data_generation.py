import psycopg2

# Dane dostępowe do bazy
conn = psycopg2.connect(
    dbname="ks_bd",
    user="postgres",
    password="root",
    host="localhost",
    port="5432"
)

# Filmy + dane dodatkowe
movies = [
    {"name": "The Shawshank Redemption", "language": "eng", "poster_path": "../posters/0.jpg",
     "trailer": "https://www.youtube.com/watch?v=6hB3S9bIaco"},
    {"name": "The Godfather", "language": "eng", "poster_path": "../posters/1.jpg",
     "trailer": "https://www.youtube.com/watch?v=sY1S34973zA"},
    {"name": "The Dark Knight", "language": "eng", "poster_path": "../posters/2.jpg",
     "trailer": "https://www.youtube.com/watch?v=EXeTwQWrcwY"},
    {"name": "12 Angry Men", "language": "eng", "poster_path": "../posters/3.jpg",
     "trailer": "https://www.youtube.com/watch?v=fSG38tk6TpI"},
    {"name": "Schindler's List", "language": "eng", "poster_path": "../posters/4.jpg",
     "trailer": "https://www.youtube.com/watch?v=gG22XNhtnoY"},
    {"name": "The Lord of the Rings: The Return of the King", "language": "eng", "poster_path": "../posters/5.jpg",
     "trailer": "https://www.youtube.com/watch?v=r5X-hFf6Bwo"},
    {"name": "Pulp Fiction", "language": "eng", "poster_path": "../posters/6.jpg",
     "trailer": "https://www.youtube.com/watch?v=s7EdQ4FqbhY"},
    {"name": "Forrest Gump", "language": "eng", "poster_path": "../posters/7.jpg",
     "trailer": "https://www.youtube.com/watch?v=bLvqoHBptjg"},
    {"name": "Inception", "language": "eng", "poster_path": "../posters/8.jpg",
     "trailer": "https://www.youtube.com/watch?v=YoHD9XEInc0"},
    {"name": "Fight Club", "language": "eng", "poster_path": "../posters/9.jpg",
     "trailer": "https://www.youtube.com/watch?v=SUXWAEX2jlg"},
]


def insert_dumb_data_additional_movie_data():
    cur = conn.cursor()
    for movie in movies:
        # Pobierz ID filmu z tabeli "MOVIES"
        cur.execute("SELECT movie_id FROM \"MOVIES\" WHERE movie_name = %s", (movie["name"],))
        result = cur.fetchone()

        if not result:
            print(f"⚠️ Nie znaleziono filmu w tabeli MOVIES: {movie['name']}")
            continue

        movie_id = result[0]

        # Odczytaj plakat jako bytea
        try:
            with open(movie["poster_path"], "rb") as f:
                poster_bytes = f.read()
        except FileNotFoundError:
            print(f"❌ Brak pliku: {movie['poster_path']}")
            continue

        # Wstaw dane do tabeli ADDITIONAL_MOVIE_DATA
        cur.execute("""
            INSERT INTO "ADDITIONAL_MOVIE_DATA" (
                movie_id, movie_poster, movie_trailer, movie_language
            ) VALUES (%s, %s, %s, %s)
        """, (
            movie_id,
            psycopg2.Binary(poster_bytes),
            movie["trailer"],
            movie["language"]
        ))

        print(f"✅ Dodano dane dodatkowe: {movie['name']}")

    conn.commit()
    print("Przykładowe dane zostały dodane.")
    cur.close()
    conn.close()