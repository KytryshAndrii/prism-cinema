from ..db.connection import conn
from ..utils.uuidToString import uuid_str
from datetime import date

movies = [
    {
        "name": "The Shawshank Redemption",
        "rating": 9.3,
        "release_date": date(1994, 9, 23),
        "pg": "R",
        "description": "Two imprisoned men bond over a number of years, finding solace and eventual redemption."
    },
    {
        "name": "The Godfather",
        "rating": 9.2,
        "release_date": date(1972, 3, 24),
        "pg": "R",
        "description": "The aging patriarch of an organized crime dynasty transfers control of his empire to his reluctant son."
    },
    {
        "name": "The Dark Knight",
        "rating": 9.0,
        "release_date": date(2008, 7, 18),
        "pg": "PG-13",
        "description": "Batman faces the Joker, a criminal mastermind who plunges Gotham into anarchy."
    },
    {
        "name": "12 Angry Men",
        "rating": 9.0,
        "release_date": date(1957, 4, 10),
        "pg": "PG",
        "description": "A jury holdout attempts to prevent a miscarriage of justice."
    },
    {
        "name": "Schindler's List",
        "rating": 9.0,
        "release_date": date(1993, 12, 15),
        "pg": "R",
        "description": "A businessman saves hundreds of Jews during the Holocaust."
    },
    {
        "name": "The Lord of the Rings: The Return of the King",
        "rating": 8.9,
        "release_date": date(2003, 12, 17),
        "pg": "PG-13",
        "description": "The final confrontation between the forces of good and evil for the control of Middle-earth."
    },
    {
        "name": "Pulp Fiction",
        "rating": 8.9,
        "release_date": date(1994, 10, 14),
        "pg": "R",
        "description": "The lives of two mob hitmen, a boxer, and others intertwine in four tales of violence and redemption."
    },
    {
        "name": "Forrest Gump",
        "rating": 8.8,
        "release_date": date(1994, 7, 6),
        "pg": "PG-13",
        "description": "The story of Forrest Gump, a man with a low IQ but good intentions."
    },
    {
        "name": "Inception",
        "rating": 8.8,
        "release_date": date(2010, 7, 16),
        "pg": "PG-13",
        "description": "A thief steals corporate secrets through the use of dream-sharing technology."
    },
    {
        "name": "Fight Club",
        "rating": 8.8,
        "release_date": date(1999, 10, 15),
        "pg": "R",
        "description": "An insomniac office worker forms an underground fight club."
    },
]



def insert_dumb_data_movies():
    cur = conn.cursor()
    for movie in movies:
        cur.execute("""
            INSERT INTO "MOVIES" (
                movie_id, movie_name, movie_rating,
                movie_release_date, movie_pg, movie_description
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            uuid_str(),
            movie["name"],
            movie["rating"],
            movie["release_date"],
            movie["pg"],
            movie["description"]
        ))
        print(f"🎬 Dodano film: {movie['name']}")
    conn.commit()
    print("Przykładowe dane zostały dodane.")
    cur.close()
    conn.close()