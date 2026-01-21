from db.connection import conn
from utils.uuidToString import uuid_str


# Lista aktorów głównych dla każdego filmu
actors = [
    {"first_name": "Tim", "middle_name": "", "last_name": "Robbins", "birthplace": "West Covina, California, USA"},  # Shawshank
    {"first_name": "Morgan", "middle_name": "", "last_name": "Freeman", "birthplace": "Memphis, Tennessee, USA"},
    {"first_name": "Marlon", "middle_name": "", "last_name": "Brando", "birthplace": "Omaha, Nebraska, USA"},  # Godfather
    {"first_name": "Al", "middle_name": "", "last_name": "Pacino", "birthplace": "New York City, New York, USA"},
    {"first_name": "Christian", "middle_name": "", "last_name": "Bale", "birthplace": "Haverfordwest, Wales"},  # Dark Knight
    {"first_name": "Heath", "middle_name": "", "last_name": "Ledger", "birthplace": "Perth, Australia"},
    {"first_name": "Henry", "middle_name": "", "last_name": "Fonda", "birthplace": "Grand Island, Nebraska, USA"},  # 12 Angry Men
    {"first_name": "Lee", "middle_name": "J.", "last_name": "Cobb", "birthplace": "New York City, New York, USA"},
    {"first_name": "Liam", "middle_name": "", "last_name": "Neeson", "birthplace": "Ballymena, Northern Ireland"},  # Schindler
    {"first_name": "Ralph", "middle_name": "", "last_name": "Fiennes", "birthplace": "Ipswich, Suffolk, England"},
    {"first_name": "Elijah", "middle_name": "", "last_name": "Wood", "birthplace": "Cedar Rapids, Iowa, USA"},  # LOTR
    {"first_name": "Viggo", "middle_name": "", "last_name": "Mortensen", "birthplace": "New York City, New York, USA"},
    {"first_name": "John", "middle_name": "", "last_name": "Travolta", "birthplace": "Englewood, New Jersey, USA"},  # Pulp Fiction
    {"first_name": "Samuel", "middle_name": "L.", "last_name": "Jackson", "birthplace": "Washington, D.C., USA"},
    {"first_name": "Tom", "middle_name": "", "last_name": "Hanks", "birthplace": "Concord, California, USA"},  # Forrest Gump
    {"first_name": "Robin", "middle_name": "", "last_name": "Wright", "birthplace": "Dallas, Texas, USA"},
    {"first_name": "Leonardo", "middle_name": "", "last_name": "DiCaprio", "birthplace": "Los Angeles, California, USA"},  # Inception
    {"first_name": "Joseph", "middle_name": "Gordon", "last_name": "Levitt", "birthplace": "Los Angeles, California, USA"},
    {"first_name": "Edward", "middle_name": "", "last_name": "Norton", "birthplace": "Boston, Massachusetts, USA"},  # Fight Club
    {"first_name": "Brad", "middle_name": "", "last_name": "Pitt", "birthplace": "Shawnee, Oklahoma, USA"},
]


def insert_dumb_data_actors():
    cur = conn.cursor()

    for actor in actors:
        cur.execute("""
              INSERT INTO "ACTORS" (
                  actor_id, first_name, middle_name, last_name, birthplace
              )
              VALUES (%s, %s, %s, %s, %s)
          """, (
            uuid_str(),
            actor["first_name"],
            actor["middle_name"] if actor["middle_name"] else None,
            actor["last_name"],
            actor["birthplace"]
        ))

        print(f"✅ Dodano aktora: {actor['first_name']} {actor['last_name']}")

    conn.commit()
    cur.close()
    conn.close()
    print("\n🎉 Wszyscy aktorzy zostali dodani.")