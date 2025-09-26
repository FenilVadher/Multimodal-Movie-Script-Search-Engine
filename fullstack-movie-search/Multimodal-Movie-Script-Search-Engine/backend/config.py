"""
Configuration settings for the Multimodal Movie Script Search Engine
"""
import os

# API Configuration
TMDB_API_KEY = os.getenv('TMDB_API_KEY', 'your_tmdb_api_key_here')
OMDB_API_KEY = os.getenv('OMDB_API_KEY', 'your_omdb_api_key_here')

# Model Configuration
CLIP_MODEL_NAME = "openai/clip-vit-base-patch32"
TEXT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
BART_MODEL_NAME = "facebook/bart-large-cnn"
GPT2_MODEL_NAME = "gpt2"

# Search Configuration
MAX_RESULTS = 3
SIMILARITY_THRESHOLD = 0.0
IMAGE_SIZE = (400, 300)

# API URLs
TMDB_BASE_URL = "https://api.themoviedb.org/3"
OMDB_BASE_URL = "http://www.omdbapi.com"

# Flask Configuration
DEBUG = True
HOST = '0.0.0.0'
PORT = 5001
