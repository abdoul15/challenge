import psycopg2
from psycopg2 import sql
from urllib.parse import urlparse
from config.settings import DATABASE_URL

def create_views(connection):
    create_normalized_titles_view = """
    CREATE OR REPLACE VIEW public.normalized_titles AS
    SELECT 
        t1.original_title AS movie_title,
        t1.popularity,
        t2."Brand" AS movie_brand,
        t1.vote_average,
        t1.vote_count
    FROM 
        public.tmdb_movies t1
    JOIN 
        public.cleaned_bofficemojo t2 ON LOWER(t1.normalized_title) = LOWER(t2.normalized_title);
    """
    
    create_avg_popularity_by_brand_view = """
    CREATE OR REPLACE VIEW public.avg_popularity_by_brand AS
    SELECT 
        movie_brand,
        AVG(popularity) AS avg_popularity
    FROM 
        public.normalized_titles
    GROUP BY 
        movie_brand;
    """
    
    create_ratings_comparison_view = """
    CREATE OR REPLACE VIEW public.ratings_comparison AS
    SELECT 
        movie_brand,
        AVG(vote_average) AS avg_rating,
        COUNT(vote_count) AS total_votes
    FROM 
        public.normalized_titles
    GROUP BY 
        movie_brand;
    """
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql.SQL(create_normalized_titles_view))
            cursor.execute(sql.SQL(create_avg_popularity_by_brand_view))
            cursor.execute(sql.SQL(create_ratings_comparison_view))
            connection.commit()
            print("Les vues ont été créées avec succès.")
    except Exception as e:
        print(f"Erreur lors de la création des vues : {e}")
        connection.rollback()

def main():
    connection = None
    try:
        # Parse the DATABASE_URL
        result = urlparse(DATABASE_URL)
        username = result.username
        password = result.password
        database = result.path[1:]
        hostname = result.hostname
        port = result.port

        # Connexion à la base de données
        connection = psycopg2.connect(
            dbname=database,
            user=username,
            password=password,
            host=hostname,
            port=port
        )
        create_views(connection)
    except Exception as e:
        print(f"Erreur lors de la connexion à la base de données: {e}")
    finally:
        if connection:
            connection.close()
            print("Connexion à la base de données fermée.")

if __name__ == "__main__":
    main()
