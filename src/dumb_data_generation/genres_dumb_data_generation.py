from ..db.connection import conn
from ..utils.uuidToString import uuid_str

# Lista unikalnych gatunków z powyższych filmów
genres = [
    {"name": "Drama", "description": "Serious stories focusing on realistic characters and emotional themes."},
    {"name": "Crime", "description": "Stories centered around criminals, criminal acts, and their consequences."},
    {"name": "Action", "description": "High energy, big-budget physical stunts and chases."},
    {"name": "Biography", "description": "Based on the life of a real person."},
    {"name": "History", "description": "Depicts historical events or settings."},
    {"name": "Adventure", "description": "Exciting stories involving journeys or exploration."},
    {"name": "Fantasy", "description": "Includes magical, mythical, or supernatural elements."},
    {"name": "Romance", "description": "Focuses on love and romantic relationships."},
    {"name": "Sci-Fi", "description": "Speculative science, futuristic technology or space exploration."}
]

def insert_dumb_data_genres():
    cur = conn.cursor()
    for genre in genres:
        genre_id = uuid_str()
        cur.execute("""
               INSERT INTO "GENRES" (
                   genre_id, genre_name, genre_description
               ) VALUES (%s, %s, %s)
           """, (
            genre_id,
            genre["name"],
            genre["description"]
        ))

        print(f"✅ Dodano gatunek: {genre['name']}")

    conn.commit()
    cur.close()
    conn.close()
    print("\n🎉 Wszystkie gatunki zostały pomyślnie dodane do tabeli GENRES.")
