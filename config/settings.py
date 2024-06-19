import os
from dotenv import load_dotenv

load_dotenv()

# Clé API TMDB
tmdb_api_key = os.getenv('TMDB_API_KEY')

# Informations de connexion à la base de données
DATABASE_URL = os.getenv('DATABASE_URL')