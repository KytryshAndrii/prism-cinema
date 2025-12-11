import unittest
import psycopg2

class TestTablePermissions(unittest.TestCase):
    def setUp(self):
        self.conn = psycopg2.connect(
            dbname="ks_bd",
            user="member",  # <- tu wpisz użytkownika, którego testujesz
            password="member",
            host="localhost",
            port="5432"
        )
        self.cur = self.conn.cursor()

    def tearDown(self):
        self.cur.close()
        self.conn.close()

    def check_permission(self, sql, expect_success=True):
        try:
            self.cur.execute(sql)
            if sql.strip().upper().startswith("SELECT"):
                self.cur.fetchall()
            if not expect_success:
                self.fail(f"Expected failure, but query succeeded: {sql}")
        except psycopg2.Error as e:
            if expect_success:
                self.fail(f"Expected success, but got error: {e.pgerror}")

    def test_select_permission(self):
        self.check_permission('SELECT * FROM "USERS";', expect_success=True)

    def test_insert_permission(self):
        self.check_permission("""
            INSERT INTO "GENRES"(genre_id, genre_name)
            VALUES (gen_random_uuid(), 'TestGenre');
        """, expect_success=False)

    def test_update_permission(self):
        self.check_permission("""
            UPDATE "MOVIES" SET movie_rating = 1.0 WHERE false;
        """, expect_success=False)

    def test_delete_permission(self):
        self.check_permission("""
            DELETE FROM "ACTORS" WHERE false;
        """, expect_success=False)

if __name__ == '__main__':
    unittest.main()
