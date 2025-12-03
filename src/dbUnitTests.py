# test_queries.py

import unittest
import psycopg2

class TestDatabaseQueries(unittest.TestCase):
    def setUp(self):
        # Nawiązanie połączenia z bazą danych PostgreSQL przed każdym testem
        self.conn = psycopg2.connect(
            dbname="ks_bd",      # <-- Zmień na swoją nazwę bazy
            user="postgres",         # <-- Twój użytkownik bazy
            password="root",         # <-- Hasło do bazy
            host="localhost",
            port="5432"
        )
        self.cur = self.conn.cursor()

    def tearDown(self):
        # Zamknięcie połączenia po każdym teście
        self.cur.close()
        self.conn.close()

    def test_user_exists(self):
        """
        Test sprawdza, czy istnieje przynajmniej jeden użytkownik o loginie 'jdoe' w tabeli USERS.

        Uruchamiaj ten test po dodaniu przykładowych danych (np. przez insert_sample_data.py),
        które tworzą użytkownika o loginie 'jdoe'. Jeśli rekord nie istnieje — test się nie powiedzie.
        """
        self.cur.execute("""SELECT COUNT(*) FROM "USERS" WHERE user_login = 'jdoe';""")
        count = self.cur.fetchone()[0]
        self.assertGreaterEqual(count, 1)  # Test przechodzi, jeśli znaleziono >=1 rekord

    def test_actor_movie_relation(self):
        """
        Test sprawdza, czy istnieje jakiekolwiek powiązanie między aktorami a filmami w tabeli MOVIE_ACTORS.

        Upewnij się, że wcześniej zostały dodane dane do tabeli MOVIE_ACTORS.
        Jeśli tabela jest pusta, test się nie powiedzie.
        """
        self.cur.execute("""SELECT COUNT(*) FROM "MOVIE_ACTORS";""")
        count = self.cur.fetchone()[0]
        self.assertGreaterEqual(count, 1)  # Test przechodzi, jeśli istnieje co najmniej jedno powiązanie

if __name__ == '__main__':
    unittest.main()
