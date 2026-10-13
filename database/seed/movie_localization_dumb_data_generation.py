import json
from db.connection import conn


# PRZYKŁADOWE FRAGMENTY NAPISÓW (JSON)
subtitles_samples = {
    "eng": [
        {"start": "00:00:01,000", "end": "00:00:04,000", "text": "This is an English subtitle sample."},
        {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Another example line."}
    ],
    "pol": [
        {"start": "00:00:01,000", "end": "00:00:04,000", "text": "To jest przykładowy polski napis."},
        {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Kolejna linia napisów."}
    ],
    "esp": [
        {"start": "00:00:01,000", "end": "00:00:04,000", "text": "Esto es un subtítulo en español."},
        {"start": "00:00:05,000", "end": "00:00:07,000", "text": "Otra línea de ejemplo."}
    ]
}


# FILMY Z TABELI MOVIES (tylko names)
movie_titles = [
    "The Shawshank Redemption",
    "The Godfather",
    "The Dark Knight",
    "12 Angry Men",
    "Schindler's List",
    "The Lord of the Rings: The Return of the King",
    "Pulp Fiction",
    "Forrest Gump",
    "Inception",
    "Fight Club"
]



def insert_dumb_data_movie_localizations():
    # DLA KAŻDEGO FILMU – dodaj ENG, POL, ESP
    cur = conn.cursor()
    for title in movie_titles:

        # Pobranie movie_id
        cur.execute('SELECT movie_id FROM "MOVIES" WHERE movie_name = %s', (title,))
        result = cur.fetchone()

        if not result:
            print(f"❌ Film nie znaleziony w bazie: {title}")
            continue

        movie_id = result[0]

        # Iteracja po językach
        for lang in ["eng", "pol", "esp"]:
            subtitles_json = json.dumps(subtitles_samples[lang])  # zamiana na JSON string

            cur.execute("""
                INSERT INTO "MOVIE_LOCALIZATIONS" (
                    movie_id, subtitles_language, subtitles
                )
                VALUES (%s, %s, %s)
            """, (movie_id, lang, subtitles_json))

            print(f"✅ Dodano lokalizację {lang.upper()} dla filmu: {title}")

    print("\n🎉 Wszystkie lokalizacje zostały dodane!")
    conn.commit()
    print("Przykładowe dane zostały dodane.")
    cur.close()
    conn.close()