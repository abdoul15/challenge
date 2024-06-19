import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from config.settings import DATABASE_URL





def load_csv_to_dataframe(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Le fichier {file_path} est introuvable.")
    return pd.read_csv(file_path)

def create_tables(engine):
    create_cleaned_bofficemojo_table = """
    CREATE TABLE IF NOT EXISTS cleaned_bofficemojo (
        id SERIAL PRIMARY KEY,
        Brand VARCHAR,
        Total INTEGER,
        Releases INTEGER,
        Release VARCHAR,
        Lifetime_Gross INTEGER,
        normalized_title VARCHAR UNIQUE
    );
    """
    
    create_tmdb_movies_table = """
    CREATE TABLE IF NOT EXISTS tmdb_movies (
        id SERIAL PRIMARY KEY,
        original_title VARCHAR,
        genres VARCHAR,
        overview TEXT,
        popularity FLOAT,
        release_date DATE,
        vote_average FLOAT,
        vote_count INTEGER,
        normalized_title VARCHAR,
        FOREIGN KEY (normalized_title) REFERENCES cleaned_bofficemojo (normalized_title)
    );
    """
    
    with engine.connect() as connection:
        connection.execute(text(create_cleaned_bofficemojo_table))
        connection.execute(text(create_tmdb_movies_table))
        print("Les tables ont été créées avec succès.")

def ingest_data_to_db(df, table_name, engine):
    try:
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Les données ont été ingérées avec succès dans la table {table_name}.")
    except SQLAlchemyError as e:
             print(f"Erreur lors de l'ingestion des données dans la table {table_name}: {e}")

def main():
    try:
        # Connexion à la base de données
        engine = create_engine(DATABASE_URL)
        
        # Créer les tables
        create_tables(engine)

        # Chargement des données nettoyées
        df_mojo = load_csv_to_dataframe('data/cleaned_bofficemojo.csv')
        df_tmdb = load_csv_to_dataframe('data/tmdb_movies.csv')

        # Vérification des colonnes
        df_mojo.columns = ['Brand', 'Total', 'Releases', 'Release', 'Lifetime_Gross', 'normalized_title']
        df_tmdb.columns = ['original_title', 'genres', 'overview', 'popularity', 'release_date', 'vote_average', 'vote_count', 'normalized_title']

        # Ingestion des données dans la base de données
        ingest_data_to_db(df_mojo, 'cleaned_bofficemojo', engine)
        ingest_data_to_db(df_tmdb, 'tmdb_movies', engine)

    except SQLAlchemyError as e:
        print(f"Erreur lors de la connexion à la base de données : {e}")
    except FileNotFoundError as e:
        print(f"Erreur lors du chargement des fichiers CSV : {e}")

if __name__ == "__main__":
    main()