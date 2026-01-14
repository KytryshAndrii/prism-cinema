from flask import request, jsonify
from db.connection import get_connection

def search_entities(table_name):
    query = request.args.get("query", "")
    limit = 10

    conn = get_connection()
    cur = conn.cursor()
    result = []

    try:
        table_upper = table_name.upper()

        if table_upper in ["ACTORS", "DIRECTORS"]:
            cur.execute(f"""
                SELECT {table_name[:-1].lower()}_id, first_name, middle_name, last_name
                FROM "{table_name.upper()}"
                WHERE first_name ILIKE %s OR middle_name ILIKE %s OR last_name ILIKE %s
                ORDER BY last_name, first_name
                LIMIT %s
            """, (f"%{query}%", f"%{query}%", f"%{query}%", limit))

            rows = cur.fetchall()
            result = [
                {
                    "id": row[0],
                    "name": " ".join(filter(None, [row[1], row[2], row[3]]))
                } for row in rows
            ]

        elif table_upper == "GENRES":
            cur.execute(f"""
                SELECT {table_name[:-1].lower()}_id, genre_name
                FROM "{table_name.upper()}"
                WHERE genre_name ILIKE %s
                ORDER BY genre_name
                LIMIT %s
            """, (f"%{query}%", limit))

            rows = cur.fetchall()
            result = [{"id": row[0], "name": row[1]} for row in rows]

        elif table_upper == "MOVIES":
            cur.execute(f"""
                SELECT {table_name[:-1].lower()}_id, movie_name
                FROM "{table_name.upper()}"
                WHERE movie_name ILIKE %s
                ORDER BY movie_name
                LIMIT %s
            """, (f"%{query}%", limit))

            rows = cur.fetchall()
            result = [{"id": row[0], "name": row[1]} for row in rows]

        elif table_upper == "USERS":
            cur.execute(f"""
                SELECT {table_name[:-1].lower()}_id, user_login
                FROM "{table_name.upper()}"
                WHERE user_login ILIKE %s
                ORDER BY user_login
                LIMIT %s
            """, (f"%{query}%", limit))

            rows = cur.fetchall()
            result = [{"id": row[0], "name": row[1]} for row in rows]

    finally:
        cur.close()
        conn.close()

    return jsonify(result), 200
