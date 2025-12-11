import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import os

# Lista zapytań
queries = {
    "USERS": 'SELECT * FROM "USERS"',
    "SERVICE_SUBSCRIPTION_PLANS": 'SELECT * FROM "SERVICE_SUBSCRIPTION_PLANS"',
    "MOVIES": 'SELECT * FROM "MOVIES"',
    "LICENSES": 'SELECT * FROM "LICENSES"',
    "ADDITIONAL_MOVIE_DATA": 'SELECT * FROM "ADDITIONAL_MOVIE_DATA"',
    "MOVIE_LOCALIZATIONS": 'SELECT * FROM "MOVIE_LOCALIZATIONS"',
    "DIRECTORS": 'SELECT * FROM "DIRECTORS"',
    "ACTORS": 'SELECT * FROM "ACTORS"',
    "GENRES": 'SELECT * FROM "GENRES"',
    "FAVOURITE_MOVIES": 'SELECT * FROM "FAVOURITE_MOVIES"',
    "MOVIE_DIRECTORS": 'SELECT * FROM "MOVIE_DIRECTORS"',
    "MOVIE_ACTORS": 'SELECT * FROM "MOVIE_ACTORS"',
    "MOVIE_GENRES": 'SELECT * FROM "MOVIE_GENRES"',
    "MOVIE_LICENSES": 'SELECT * FROM "MOVIE_LICENSES"',
    "movies_with_actors": 'SELECT * FROM "movies_with_actors"',
    "highest_rate_movies": 'SELECT * FROM "highest_rate_movies"',
    "movies_with_directors": 'SELECT * FROM "movies_with_directors"',
    "movies_language_info": 'SELECT * FROM "movies_language_info"',
    "user_favourites_movies": 'SELECT * FROM "user_favourites_movies"'
}

# Połączenie do bazy
conn = psycopg2.connect(
    dbname="ks_bd",
    user="postgres",
    password="root",
    host="localhost",
    port="5432"
)

# Stwórz folder na screeny
output_folder = "query_screenshots"
os.makedirs(output_folder, exist_ok=True)

# Ustawienia matplotlib
plt.rcParams["font.size"] = 6
plt.rcParams["figure.figsize"] = (12, 4)

def dataframe_to_image(df, title, filename):
    fig, ax = plt.subplots()
    ax.axis("off")
    ax.set_title(title, fontsize=10, loc='left')

    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        loc="center",
        cellLoc='center',
    )
    table.scale(1, 1.2)

    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, filename), dpi=300)
    plt.close()


# Główna pętla
for name, query in queries.items():
    df = pd.read_sql(query, conn)
    if df.empty:
        print(f"⚠️  {name}: brak danych.")
    else:
        print(f"✅  {name}: {len(df)} rekordów. Generuję zrzut…")
        safe_name = name.replace(" ", "_").lower() + ".png"
        dataframe_to_image(df, f"{name} — wyniki zapytania", safe_name)

conn.close()
print("\n🎉 Wszystkie zapytania wykonane i zapisane jako obrazy w folderze 'query_screenshots'.")
