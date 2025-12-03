from ..db.connection import conn


user_id = "1446e48b-6951-43ed-bc83-73f5f85f57ca"

# Lista nazw ulubionych filmów tego użytkownika
favorite_movie_titles = [
    "The Shawshank Redemption",
    "The Godfather",
    "Inception",
    "Fight Club"
]



def insert_dumb_data_join_tables():
    cur = conn.cursor()
    for title in favorite_movie_titles:
        # Pobierz movie_id z tabeli MOVIES na podstawie tytułu
        cur.execute("""
                SELECT movie_id FROM "MOVIES" WHERE name = %s
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