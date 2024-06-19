import asyncio
import aiohttp
import pandas as pd
from config.settings import tmdb_api_key

def normalize_title(title):
    return title.strip().lower().replace(" ", "").replace(":", "").replace("-", "")

async def fetch_genres(session):
    url = f"https://api.themoviedb.org/3/genre/movie/list"
    params = {'api_key': tmdb_api_key}
    async with session.get(url, params=params) as response:
        response.raise_for_status()
        data = await response.json()
        return {genre['id']: genre['name'] for genre in data['genres']}

async def fetch_movie_details(session, title, genres):
    url = f"https://api.themoviedb.org/3/search/movie"
    params = {'api_key': tmdb_api_key, 'query': title, 'include_adult': 'false'}
    async with session.get(url, params=params) as response:
        response.raise_for_status()
        data = await response.json()
        if data['results']:
            result = data['results'][0]
            genre_names = [genres.get(genre_id, 'Unknown') for genre_id in result.get('genre_ids', [])]
            return {
                'original_title': result.get('title', title),
                'genres': genre_names,
                'overview': result.get('overview', ''),
                'popularity': result.get('popularity', 0),
                'release_date': result.get('release_date', ''),
                'vote_average': result.get('vote_average', 0),
                'vote_count': result.get('vote_count', 0),
                'normalized_title': normalize_title(result.get('title', title))
            }
        else:
            return {
                'original_title': title,
                'genres': [],
                'overview': '',
                'popularity': 0,
                'release_date': '',
                'vote_average': 0,
                'vote_count': 0,
                'normalized_title': normalize_title(title)
            }

async def fetch_all_movies(titles):
    async with aiohttp.ClientSession() as session:
        genres = await fetch_genres(session)
        tasks = [fetch_movie_details(session, title, genres) for title in titles]
        results = []
        for i in range(0, len(tasks), 50):
            batch = tasks[i:i+50]
            results.extend(await asyncio.gather(*batch))
            await asyncio.sleep(1)
        return results

def main():
    df_bomojo = pd.read_csv('data/cleaned_bofficemojo.csv')
    titles = df_bomojo['#1 Release'].tolist()
    movie_details = asyncio.run(fetch_all_movies(titles))
    df_tmdb = pd.DataFrame(movie_details)
    df_tmdb.to_csv('data/tmdb_movies.csv', index=False)

if __name__ == "__main__":
    main()