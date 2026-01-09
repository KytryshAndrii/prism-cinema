import psycopg2

# # Dane dostępowe do bazy
# conn = psycopg2.connect(
#     dbname="ks_bd",
#     user="postgres",
#     password="root",
#     host="localhost",
#     port="5432"
# )

def get_connection():
    return psycopg2.connect(
        dbname="ks_bd",
        user="postgres",
        password="root",
        host="localhost",
        port="5432"
    )
