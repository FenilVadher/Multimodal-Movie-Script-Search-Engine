"""
External API client for fetching real movie data from TMDB and OMDB
"""
import requests
import config
from typing import Dict, List, Optional

class MovieAPIClient:
    def __init__(self):
        self.tmdb_api_key = config.TMDB_API_KEY
        self.omdb_api_key = config.OMDB_API_KEY
        self.tmdb_base_url = config.TMDB_BASE_URL
        self.omdb_base_url = config.OMDB_BASE_URL
        
    def get_popular_movies(self, page: int = 1) -> List[Dict]:
        """Get popular movies from TMDB"""
        try:
            url = f"{self.tmdb_base_url}/movie/popular"
            params = {
                'api_key': self.tmdb_api_key,
                'page': page,
                'language': 'en-US'
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json().get('results', [])
        except Exception as e:
            print(f"Error fetching popular movies: {e}")
            return []
    
    def get_movie_details(self, movie_id: int) -> Optional[Dict]:
        """Get detailed movie information from TMDB"""
        try:
            url = f"{self.tmdb_base_url}/movie/{movie_id}"
            params = {
                'api_key': self.tmdb_api_key,
                'language': 'en-US'
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching movie details for ID {movie_id}: {e}")
            return None
    
    def search_movies(self, query: str) -> List[Dict]:
        """Search for movies by title"""
        try:
            url = f"{self.tmdb_base_url}/search/movie"
            params = {
                'api_key': self.tmdb_api_key,
                'query': query,
                'language': 'en-US'
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json().get('results', [])
        except Exception as e:
            print(f"Error searching movies: {e}")
            return []
    
    def get_movie_images(self, movie_id: int) -> Dict:
        """Get movie images from TMDB"""
        try:
            url = f"{self.tmdb_base_url}/movie/{movie_id}/images"
            params = {
                'api_key': self.tmdb_api_key
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching movie images for ID {movie_id}: {e}")
            return {}
    
    def get_omdb_details(self, imdb_id: str) -> Optional[Dict]:
        """Get movie details from OMDB using IMDB ID"""
        try:
            url = self.omdb_base_url
            params = {
                'apikey': self.omdb_api_key,
                'i': imdb_id,
                'plot': 'full'
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if data.get('Response') == 'True':
                return data
            return None
        except Exception as e:
            print(f"Error fetching OMDB details for IMDB ID {imdb_id}: {e}")
            return None
    
    def get_trending_tv_shows(self, page: int = 1) -> List[Dict]:
        """Get trending TV shows from TMDB"""
        try:
            url = f"{self.tmdb_base_url}/trending/tv/week"
            params = {
                'api_key': self.tmdb_api_key,
                'page': page
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json().get('results', [])
        except Exception as e:
            print(f"Error fetching trending TV shows: {e}")
            return []

# Global API client instance
api_client = MovieAPIClient()
