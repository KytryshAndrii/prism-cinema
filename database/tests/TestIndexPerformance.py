import unittest
import psycopg2
import time


class TestIndexPerformance(unittest.TestCase):

    def setUp(self):
        self.conn = psycopg2.connect(
            dbname="ks_bd",
            user="postgres",
            password="root",
            host="localhost",
            port="5432"
        )
        self.cur = self.conn.cursor()

    def tearDown(self):
        self.cur.close()
        self.conn.close()

    # ---------------------
    # Helper: check if EXPLAIN uses an index
    # ---------------------
    def assertIndexUsed(self, query):
        self.cur.execute(query)
        plan = "\n".join(row[0] for row in self.cur.fetchall())
        self.assertIn("Index", plan, f"INDEX NOT USED!\nPlan:\n{plan}")

    # ---------------------
    # Helper: get ID from table
    # ---------------------
    def any_value(self, table, column):
        self.cur.execute(f'SELECT {column} FROM "{table}" LIMIT 1;')
        return self.cur.fetchone()[0]

    # ============================================================
    #  INDEX TESTS FOR ALL TABLES (BASED ON YOUR PGADMIN SCREEN)
    # ============================================================

    # ==================== ACTORS ====================
    def test_index_actors_actor_id(self):
        self.assertIndexUsed("""
            EXPLAIN ANALYZE SELECT * FROM "ACTORS" WHERE actor_id = (SELECT actor_id FROM "ACTORS" LIMIT 1);
        """)

    def test_index_actors_first_last_name(self):
        self.assertIndexUsed("""
            EXPLAIN ANALYZE SELECT * FROM "ACTORS"
            WHERE first_name = (SELECT first_name FROM "ACTORS" LIMIT 1)
              AND last_name = (SELECT last_name FROM "ACTORS" LIMIT 1);
        """)

    def test_index_actors_birthplace(self):
        self.assertIndexUsed("""
            EXPLAIN ANALYZE SELECT * FROM "ACTORS"
            WHERE birthplace = (SELECT birthplace FROM "ACTORS" LIMIT 1);
        """)

    # ==================== ADDITIONAL_MOVIE_DATA ====================
    def test_index_additional_movie_data_movie_id(self):
        self.assertIndexUsed("""
            EXPLAIN ANALYZE SELECT * FROM "ADDITIONAL_MOVIE_DATA"
            WHERE movie_id = (SELECT movie_id FROM "ADDITIONAL_MOVIE_DATA" LIMIT 1);
        """)

    def test_index_additional_movie_data_language(self):
        self.assertIndexUsed("""
            EXPLAIN ANALYZE SELECT * FROM "ADDITIONAL_MOVIE_DATA"
            WHERE movie_language = (SELECT movie_language FROM "ADDITIONAL_MOVIE_DATA" LIMIT 1);
        """)

    # ==================== DIRECTORS ====================
    def test_index_directors_director_id(self):
        self.assertIndexUsed("""
            EXPLAIN ANALYZE SELECT * FROM "DIRECTORS"
            WHERE director_id = (SELECT director_id FROM "DIRECTORS" LIMIT 1);
        """)

    def test_index_directors_birthplace(self):
        self.assertIndexUsed("""
            EXPLAIN ANALYZE SELECT * FROM "DIRECTORS"
            WHERE birthplace = (SELECT birthplace FROM "DIRECTORS" LIMIT 1);
        """)

    def test_index_directors_first_last_name(self):
        self.assertIndexUsed("""
            EXPLAIN ANALYZE SELECT * FROM "DIRECTORS"
            WHERE first_name = (SELECT first_name FROM "DIRECTORS" LIMIT 1)
              AND last_name = (SELECT last_name FROM "DIRECTORS" LIMIT 1);
        """)

    # ==================== FAVOURITE_MOVIES (COMPOSITE INDEX) ====================
    def test_index_fav_movies(self):
        self.assertIndexUsed("""
            EXPLAIN ANALYZE SELECT * FROM "FAVOURITE_MOVIES"
            WHERE user_id = (SELECT user_id FROM "FAVOURITE_MOVIES" LIMIT 1);
        """)

    # ==================== GENRES ====================
    def test_index_genres_name(self):
        self.assertIndexUsed("""
            EXPLAIN ANALYZE SELECT * FROM "GENRES"
            WHERE genre_name = (SELECT genre_name FROM "GENRES" LIMIT 1);
        """)

    def test_index_genres_id(self):
        self.assertIndexUsed("""
            EXPLAIN ANALYZE SELECT * FROM "GENRES"
            WHERE genre_id = (SELECT genre_id FROM "GENRES" LIMIT 1);
        """)

    # ==================== LICENSES ====================
    def test_index_licenses_id(self):
        self.assertIndexUsed("""
            EXPLAIN ANALYZE SELECT * FROM "LICENSES"
            WHERE license_id = (SELECT license_id FROM "LICENSES" LIMIT 1);
        """)

    # ==================== MOVIES ====================
    def test_index_movies_pg(self):
        self.assertIndexUsed("""
            EXPLAIN ANALYZE SELECT * FROM "MOVIES"
            WHERE movie_pg = (SELECT movie_pg FROM "MOVIES" LIMIT 1);
        """)

    def test_index_movies_id(self):
        self.assertIndexUsed("""
            EXPLAIN ANALYZE SELECT * FROM "MOVIES"
            WHERE movie_id = (SELECT movie_id FROM "MOVIES" LIMIT 1);
        """)

    def test_index_movies_rating(self):
        self.assertIndexUsed("""
            EXPLAIN ANALYZE SELECT * FROM "MOVIES"
            WHERE movie_rating = (SELECT movie_rating FROM "MOVIES" LIMIT 1);
        """)

    # ==================== MOVIE_ACTORS ====================
    def test_index_movie_actors_actor_movie(self):
        self.assertIndexUsed("""
            EXPLAIN ANALYZE SELECT * FROM "MOVIE_ACTORS"
            WHERE actor_id = (SELECT actor_id FROM "MOVIE_ACTORS" LIMIT 1);
        """)

    def test_index_movie_actors_movie_actor(self):
        self.assertIndexUsed("""
            EXPLAIN ANALYZE SELECT * FROM "MOVIE_ACTORS"
            WHERE movie_id = (SELECT movie_id FROM "MOVIE_ACTORS" LIMIT 1);
        """)

    # ==================== MOVIE_DIRECTORS ====================
    def test_index_movie_directors_director_movie(self):
        self.assertIndexUsed("""
            EXPLAIN ANALYZE SELECT * FROM "MOVIE_DIRECTORS"
            WHERE director_id = (SELECT director_id FROM "MOVIE_DIRECTORS" LIMIT 1);
        """)

    def test_index_movie_directors_movie_director(self):
        self.assertIndexUsed("""
            EXPLAIN ANALYZE SELECT * FROM "MOVIE_DIRECTORS"
            WHERE movie_id = (SELECT movie_id FROM "MOVIE_DIRECTORS" LIMIT 1);
        """)

    # ==================== MOVIE_GENRES ====================
    def test_index_movie_genres_genre_movie(self):
        self.assertIndexUsed("""
            EXPLAIN ANALYZE SELECT * FROM "MOVIE_GENRES"
            WHERE genre_id = (SELECT genre_id FROM "MOVIE_GENRES" LIMIT 1);
        """)

    def test_index_movie_genres_movie_genre(self):
        self.assertIndexUsed("""
            EXPLAIN ANALYZE SELECT * FROM "MOVIE_GENRES"
            WHERE movie_id = (SELECT movie_id FROM "MOVIE_GENRES" LIMIT 1);
        """)

    # ==================== MOVIE_LICENSES ====================
    def test_index_movie_licenses_license(self):
        self.assertIndexUsed("""
            EXPLAIN ANALYZE SELECT * FROM "MOVIE_LICENSES"
            WHERE license_id = (SELECT license_id FROM "MOVIE_LICENSES" LIMIT 1);
        """)

    # ==================== MOVIE_LOCALIZATIONS ====================
    def test_index_movie_localization_language(self):
        lang = self.any_value("MOVIE_LOCALIZATIONS", "subtitles_language")

        # WYŁĄCZAMY seqscan
        self.cur.execute("SET enable_seqscan = OFF;")

        query = self.cur.mogrify("""
               EXPLAIN ANALYZE
               SELECT * FROM "MOVIE_LOCALIZATIONS"
               WHERE subtitles_language = %s;
           """, (lang,)).decode()

        self.assertIndexUsed(query)

        # PRZYWRACAMY seqscan
        self.cur.execute("SET enable_seqscan = ON;")

    def test_index_movie_localization_movie_id(self):
        self.assertIndexUsed("""
            EXPLAIN ANALYZE SELECT * FROM "MOVIE_LOCALIZATIONS"
            WHERE movie_id = (SELECT movie_id FROM "MOVIE_LOCALIZATIONS" LIMIT 1);
        """)

    # ==================== USERS ====================
    def test_index_users_user_id(self):
        self.assertIndexUsed("""
            EXPLAIN ANALYZE SELECT * FROM "USERS"
            WHERE user_id = (SELECT user_id FROM "USERS" LIMIT 1);
        """)

    def test_index_user_password_mail(self):
        self.assertIndexUsed("""
            EXPLAIN ANALYZE SELECT * FROM "USERS"
            WHERE user_mail = (SELECT user_mail FROM "USERS" LIMIT 1);
        """)

# END OF TESTS

if __name__ == '__main__':
    unittest.main()
