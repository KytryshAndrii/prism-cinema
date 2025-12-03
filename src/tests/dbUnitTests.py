import unittest
import psycopg2
import time
from datetime import date
import uuid


class TestDatabaseQueries(unittest.TestCase):

    # ------------------------- SETUP / TEARDOWN -------------------------

    def setUp(self):
        """Połączenie z bazą przed KAŻDYM testem."""
        self.conn = psycopg2.connect(
            dbname="ks_bd",
            user="postgres",
            password="root",
            host="localhost",
            port="5432"
        )
        self.cur = self.conn.cursor()

    def tearDown(self):
        """Zamykanie połączenia po teście."""
        self.cur.close()
        self.conn.close()

    # ------------------------- TESTY PODSTAWOWE -------------------------

    def test_users_table_not_empty(self):
        """Czy tabela USERS zawiera dane."""
        self.cur.execute('SELECT COUNT(*) FROM "USERS";')
        count = self.cur.fetchone()[0]
        self.assertGreater(count, 0)

    def test_movies_table_not_empty(self):
        """Czy tabela MOVIES zawiera dane."""
        self.cur.execute('SELECT COUNT(*) FROM "MOVIES";')
        count = self.cur.fetchone()[0]
        self.assertGreater(count, 0)

    def test_actors_table_not_empty(self):
        self.cur.execute('SELECT COUNT(*) FROM "ACTORS";')
        self.assertGreater(self.cur.fetchone()[0], 0)

    def test_directors_table_not_empty(self):
        self.cur.execute('SELECT COUNT(*) FROM "DIRECTORS";')
        self.assertGreater(self.cur.fetchone()[0], 0)

    def test_genres_table_not_empty(self):
        self.cur.execute('SELECT COUNT(*) FROM "GENRES";')
        self.assertGreater(self.cur.fetchone()[0], 0)

    def test_licenses_table_not_empty(self):
        """Czy tabela LICENSES zawiera dane."""
        self.cur.execute('SELECT COUNT(*) FROM "LICENSES";')
        self.assertGreater(self.cur.fetchone()[0], 0)

    def test_additional_movie_data_not_empty(self):
        """Czy tabela ADDITIONAL_MOVIE_DATA zawiera dane."""
        self.cur.execute('SELECT COUNT(*) FROM "ADDITIONAL_MOVIE_DATA";')
        self.assertGreater(self.cur.fetchone()[0], 0)

    def test_movie_localizations_not_empty(self):
        """Czy tabela MOVIE_LOCALIZATIONS zawiera dane."""
        self.cur.execute('SELECT COUNT(*) FROM "MOVIE_LOCALIZATIONS";')
        self.assertGreater(self.cur.fetchone()[0], 0)

    def test_subscription_plans_not_empty(self):
        """Czy tabela SERVICE_SUBSCRIPTION_PLANS zawiera dane."""
        self.cur.execute('SELECT COUNT(*) FROM "SERVICE_SUBSCRIPTION_PLANS";')
        self.assertGreater(self.cur.fetchone()[0], 0)

    # ------------------------- TESTY RELACJI -------------------------

    def test_movie_has_actor(self):
        """Czy istnieje powiązanie film–aktor."""
        self.cur.execute('SELECT COUNT(*) FROM "MOVIE_ACTORS";')
        self.assertGreater(self.cur.fetchone()[0], 0)

    def test_movie_has_director(self):
        """Czy istnieje powiązanie film–reżyser."""
        self.cur.execute('SELECT COUNT(*) FROM "MOVIE_DIRECTORS";')
        self.assertGreater(self.cur.fetchone()[0], 0)

    def test_movie_has_genre(self):
        """Czy istnieje powiązanie film–gatunek."""
        self.cur.execute('SELECT COUNT(*) FROM "MOVIE_GENRES";')
        self.assertGreater(self.cur.fetchone()[0], 0)

    def test_movie_has_license(self):
        """Czy istnieje powiązanie film–licencja."""
        self.cur.execute('SELECT COUNT(*) FROM "MOVIE_LICENSES";')
        self.assertGreater(self.cur.fetchone()[0], 0)

    def test_movie_has_license_relation(self):
        """Czy każda licencja jest powiązana z istniejącym filmem w MOVIE_LICENSES."""
        self.cur.execute("""
            SELECT COUNT(*) 
            FROM "MOVIE_LICENSES" ml
            JOIN "MOVIES" m ON m.movie_id = ml.movie_id;
        """)
        self.assertGreater(self.cur.fetchone()[0], 0)

    def test_additional_movie_data_relation(self):
        """Czy dane dodatkowe filmu wskazują na poprawne ID filmu."""
        self.cur.execute("""
            SELECT COUNT(*) 
            FROM "ADDITIONAL_MOVIE_DATA" amd
            JOIN "MOVIES" m ON m.movie_id = amd.movie_id;
        """)
        self.assertGreater(self.cur.fetchone()[0], 0)

    def test_movie_localizations_relation(self):
        """Czy lokalizacje filmu są powiązane z istniejącymi filmami."""
        self.cur.execute("""
            SELECT COUNT(*)
            FROM "MOVIE_LOCALIZATIONS" ml
            JOIN "MOVIES" m ON m.movie_id = ml.movie_id;
        """)
        self.assertGreater(self.cur.fetchone()[0], 0)

    def test_user_subscription_plan_relation(self):
        """Czy użytkownicy mają poprawnie przypisane plany subskrypcji."""
        self.cur.execute("""
            SELECT COUNT(*)
            FROM "USERS" u
            JOIN "SERVICE_SUBSCRIPTION_PLANS" sp 
            ON sp.subscription_plan_id = u.user_subscription_plan_id;
        """)
        self.assertGreater(self.cur.fetchone()[0], 0)

    # ------------------------- TESTY WIDOKÓW -------------------------

    def test_view_highest_rate_movies(self):
        """Czy widok highest_rate_movies działa i zwraca wyniki."""
        self.cur.execute('SELECT * FROM "highest_rate_movies";')
        rows = self.cur.fetchall()
        self.assertGreater(len(rows), 0)

    def test_view_movie_with_directors(self):
        """Czy widok view_movie_with_directors działa i zwraca wyniki."""
        self.cur.execute('SELECT * FROM "movies_with_directors";')
        rows = self.cur.fetchall()
        self.assertGreater(len(rows), 0)

    def test_movies_language_info(self):
        """Czy widok movies_language_info działa i zwraca wyniki."""
        self.cur.execute('SELECT * FROM "movies_language_info";')
        rows = self.cur.fetchall()
        self.assertGreater(len(rows), 0)

    def test_movies_with_actors(self):
        """Czy widok movies_with_actors działa i zwraca wyniki."""
        self.cur.execute('SELECT * FROM "movies_with_actors";')
        rows = self.cur.fetchall()
        self.assertGreater(len(rows), 0)

    def test_user_favourites_movies(self):
        """Czy widok user_favourites_movies działa i zwraca wyniki."""
        self.cur.execute('SELECT * FROM "user_favourites_movies";')
        rows = self.cur.fetchall()
        self.assertGreater(len(rows), 0)

    # ------------------------- TEST SZYBKOŚCI ZAPYTAŃ -------------------------

    def test_query_performance(self):
        """Zapytanie SELECT powinno wykonać się szybciej niż 0.3 sekundy."""
        start = time.time()
        self.cur.execute('SELECT * FROM "MOVIES";')
        _ = self.cur.fetchall()
        duration = time.time() - start
        self.assertLess(duration, 0.3)

    # ------------------------- TESTY TRIGGERÓW -------------------------

    def test_trigger_check_movie_release_year(self):
        """Trigger powinien zabronić dodania filmu z rokiem > 2025."""

        bad_id = str(uuid.uuid4())

        with self.assertRaises(psycopg2.Error):
            self.cur.execute("""
                INSERT INTO "MOVIES"(movie_id, movie_name, movie_rating, movie_release_date, movie_pg, movie_description)
                VALUES (%s, 'Bad Movie', 1.0, %s, 'PG', 'Invalid year test')
            """, (bad_id, date(2030, 1, 1)))

        self.conn.rollback()

    def test_trigger_check_movie_has_director(self):
        """Trigger powinien wymagać aby film miał przypisanego reżysera."""

        movie_id = str(uuid.uuid4())
        actor_movie_id = movie_id  # film bez reżysera → powinien wywołać trigger cleanup / constraint

        # Wstawiamy film
        self.cur.execute("""
            INSERT INTO "MOVIES"(movie_id, movie_name, movie_rating, movie_release_date, movie_pg, movie_description)
            VALUES (%s, 'Lonely Movie', 5.0, %s, 'PG', 'test')
        """, (movie_id, date(2000, 1, 1)))

        # Próba usunięcia reżysera powinna być zablokowana triggerem
        with self.assertRaises(psycopg2.Error):
            self.cur.execute("""
                DELETE FROM "MOVIES_DIRECTORS" WHERE movie_id = %s
            """, (movie_id,))

        self.conn.rollback()

    # def test_trigger_cleanup_user_dependencies(self):
    #     """Usunięcie użytkownika powinno automatycznie usunąć jego powiązania (FAVOURITE_MOVIES)."""
    #
    #     user_id = str(uuid.uuid4())
    #
    #     # Dodaj użytkownika
    #     self.cur.execute("""
    #         INSERT INTO "USERS"(user_id, user_login, user_password, user_mail, user_is_subscribed,
    #          user_subscription_plan_id, user_subscription_period, user_is_admin, user_location_region, user_date_of_birth)
    #         VALUES (%s, 'tempuser', 'pass', 'mail@mail.com', false, NULL, NULL,  false, 'PL', %s)
    #     """, (user_id, date(1990, 1, 1)))
    #
    #     # Dodaj „ulubiony film”
    #     self.cur.execute("""
    #         SELECT movie_id FROM "MOVIES" LIMIT 1;
    #     """)
    #     movie_id = self.cur.fetchone()[0]
    #
    #     self.cur.execute("""
    #         INSERT INTO "FAVOURITE_MOVIES"(user_id, movie_id) VALUES (%s, %s)
    #     """, (user_id, movie_id))
    #
    #     # Usuń użytkownika → trigger powinien automatycznie usunąć z FAVOURITE_MOVIES
    #     self.cur.execute("""DELETE FROM "USERS" WHERE user_id = %s""", (user_id,))
    #     self.cur.execute("""SELECT COUNT(*) FROM "FAVOURITE_MOVIES" WHERE user_id = %s""", (user_id,))
    #     count = self.cur.fetchone()[0]
    #
    #     self.assertEqual(count, 0)
    #
    #     self.conn.rollback()

    # ------------------------- KONIEC TESTÓW -------------------------


if __name__ == '__main__':
    unittest.main()
