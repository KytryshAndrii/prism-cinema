import unittest
import psycopg2
import uuid
import time
from datetime import date

class TestDatabasePerformanceExtended(unittest.TestCase):
    def setUp(self):
        self.conn = psycopg2.connect(
            dbname="ks_bd", user="postgres", password="root",
            host="localhost", port="5432"
        )
        self.cur = self.conn.cursor()
        self.temp_users = []
        self.temp_movies = []
        self.temp_actors = []
        self.temp_directors = []
        self.temp_genres = []
        self.temp_licenses = []

    def tearDown(self):
        try:
            def delete_temp(table, key, values):
                if values:
                    self.cur.execute(f'DELETE FROM "{table}" WHERE {key} = ANY(%s::uuid[])', (values,))
                    self.conn.commit()

            delete_temp("USERS", "user_id", self.temp_users)
            delete_temp("MOVIES", "movie_id", self.temp_movies)
            delete_temp("ACTORS", "actor_id", self.temp_actors)
            delete_temp("DIRECTORS", "director_id", self.temp_directors)
            delete_temp("GENRES", "genre_id", self.temp_genres)
            delete_temp("LICENSES", "license_id", self.temp_licenses)

        except psycopg2.Error as e:
            print("ROLLBACK due to error in tearDown:", e)
            self.conn.rollback()

        self.cur.close()
        self.conn.close()

    # ----------------------- INSERT + SELECT -----------------------

    def insert_bulk(self, table, generator, store_list, n):
        start_insert = time.time()
        try:
            for _ in range(n):
                values = generator()
                store_list.append(values[0])  # UUID
                self.cur.execute(values[1], values[2])
            self.conn.commit()
        except psycopg2.Error as e:
            print(f"ERROR during INSERT {n} → {table}:", e)
            self.conn.rollback()
        end_insert = time.time()
        print(f"INSERT {n} → {table} → {end_insert - start_insert:.4f} seconds")

        # SELECT immediately after INSERT
        start_select = time.time()
        self.cur.execute(f'SELECT * FROM "{table}";')
        self.cur.fetchall()
        end_select = time.time()
        print(f"SELECT {n} → {table} → {end_select - start_select:.4f} seconds\n")

    def generate_user(self):
        uid = str(uuid.uuid4())
        query = """
        INSERT INTO "USERS"(user_id, user_login, user_password, user_mail, user_is_subscribed,
            user_subscription_plan_id, user_subscription_period, user_is_admin,
            user_location_region, user_date_of_birth)
        VALUES (%s, %s, 'pass', 'temp@test.com', false, NULL, NULL, false, 'PL', '1990-01-01')
        """
        return uid, query, (uid, f"user_{uid[:8]}")

    def generate_movie(self):
        mid = str(uuid.uuid4())
        query = """
        INSERT INTO "MOVIES"(movie_id, movie_name, movie_rating, movie_release_date, movie_pg, movie_description)
        VALUES (%s, %s, 5.0, '2000-01-01', 'PG', 'Test movie')
        """
        return mid, query, (mid, f"Movie_{mid[:6]}")

    def generate_actor(self):
        aid = str(uuid.uuid4())
        query = """
        INSERT INTO "ACTORS"(actor_id, first_name, last_name, birthplace)
        VALUES (%s, 'John', 'Doe', 'Poland')
        """
        return aid, query, (aid,)

    def generate_director(self):
        did = str(uuid.uuid4())
        query = """
        INSERT INTO "DIRECTORS"(director_id, first_name, last_name, birthplace)
        VALUES (%s, 'Jane', 'Smith', 'Germany')
        """
        return did, query, (did,)

    def generate_genre(self):
        gid = str(uuid.uuid4())
        query = """
        INSERT INTO "GENRES"(genre_id, genre_name)
        VALUES (%s, 'Drama')
        """
        return gid, query, (gid,)

    def generate_license(self):
        lid = str(uuid.uuid4())
        query = """
        INSERT INTO "LICENSES"(license_id, license_region, license_expiration_date)
        VALUES (%s, %s, %s)
        """
        return lid, query, (lid, 'PL', '2030-01-01')

    def insert_and_select_tests(self, name, generator, store):
        for n in [10, 100, 1000, 10000]:
            with self.subTest(table=name, rows=n):
                self.insert_bulk(name, generator, store, n)

    # ----------------------- TESTS -----------------------

    def test_users(self): self.insert_and_select_tests("USERS", self.generate_user, self.temp_users)
    def test_movies(self): self.insert_and_select_tests("MOVIES", self.generate_movie, self.temp_movies)
    def test_actors(self): self.insert_and_select_tests("ACTORS", self.generate_actor, self.temp_actors)
    def test_directors(self): self.insert_and_select_tests("DIRECTORS", self.generate_director, self.temp_directors)
    def test_genres(self): self.insert_and_select_tests("GENRES", self.generate_genre, self.temp_genres)
    def test_licenses(self): self.insert_and_select_tests("LICENSES", self.generate_license, self.temp_licenses)

if __name__ == '__main__':
    unittest.main()
