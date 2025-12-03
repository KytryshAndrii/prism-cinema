from db.connection import conn
from utils.uuidToString import uuid_str

directors = [
    {"first_name": "Frank", "middle_name": "", "last_name": "Darabont", "birthplace": "Montbéliard, France"},
    {"first_name": "Francis", "middle_name": "Ford", "last_name": "Coppola", "birthplace": "Detroit, Michigan, USA"},
    {"first_name": "Christopher", "middle_name": "", "last_name": "Nolan", "birthplace": "London, England"},
    {"first_name": "Sidney", "middle_name": "", "last_name": "Lumet", "birthplace": "Philadelphia, Pennsylvania, USA"},
    {"first_name": "Steven", "middle_name": "", "last_name": "Spielberg", "birthplace": "Cincinnati, Ohio, USA"},
    {"first_name": "Peter", "middle_name": "", "last_name": "Jackson", "birthplace": "Pukerua Bay, New Zealand"},
    {"first_name": "Quentin", "middle_name": "", "last_name": "Tarantino", "birthplace": "Knoxville, Tennessee, USA"},
    {"first_name": "Robert", "middle_name": "", "last_name": "Zemeckis", "birthplace": "Chicago, Illinois, USA"},
    {"first_name": "Christopher", "middle_name": "", "last_name": "Nolan", "birthplace": "London, England"},
    {"first_name": "David", "middle_name": "", "last_name": "Fincher", "birthplace": "Denver, Colorado, USA"}
]


def insert_dumb_data_directors():
    cur = conn.cursor()
    for director in directors:
        director_id = uuid_str()

        cur.execute("""
            INSERT INTO "DIRECTORS" (
                director_id, first_name, middle_name, last_name, birthplace
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            director_id,
            director["first_name"],
            director["middle_name"] if director["middle_name"] else None,
            director["last_name"],
            director["birthplace"]
        ))

        print(f"✅ Dodano: {director['first_name']} {director['last_name']}")

    # Zatwierdzenie zmian
    conn.commit()
    cur.close()
    conn.close()

    print("\n🎉 Reżyserzy zostali pomyślnie dodani do bazy danych.")