"""
Data management for movie and scene datasets
"""
import numpy as np
from PIL import Image
from typing import List, Dict, Tuple
from api_client import api_client
import config

class DataManager:
    def __init__(self):
        self.dialogues = []
        self.scenes = []
        self.text_embeddings = None
        self.image_embeddings = None
        
    def create_real_dataset(self) -> Tuple[List[Dict], List[Dict]]:
        """Create dataset using real movie data from APIs"""
        print("Creating real dataset from APIs...")
        
        # Get popular movies and TV shows
        movies = api_client.get_popular_movies(page=1)[:10]  # Get top 10 popular movies
        tv_shows = api_client.get_trending_tv_shows(page=1)[:5]  # Get top 5 TV shows
        
        dialogues = []
        scenes = []
        
        # Process movies
        for i, movie in enumerate(movies):
            movie_details = api_client.get_movie_details(movie['id'])
            if movie_details:
                # Create dialogue entries
                dialogue_samples = self._generate_dialogue_samples(movie_details)
                for j, dialogue in enumerate(dialogue_samples):
                    dialogues.append({
                        "id": len(dialogues) + 1,
                        "movie": movie_details.get('title', 'Unknown'),
                        "dialogue": dialogue,
                        "genre": self._format_genres(movie_details.get('genres', [])),
                        "year": int(movie_details.get('release_date', '2000-01-01')[:4]),
                        "language": movie_details.get('original_language', 'en').upper(),
                        "country": self._get_country_from_language(movie_details.get('original_language', 'en')),
                        "type": "Movie"
                    })
                
                # Create scene entries
                scenes.append({
                    "id": len(scenes) + 1,
                    "movie": movie_details.get('title', 'Unknown'),
                    "description": movie_details.get('overview', 'No description available'),
                    "image_url": f"https://image.tmdb.org/t/p/w500{movie_details.get('poster_path', '')}" if movie_details.get('poster_path') else f"https://picsum.photos/400/300?random={len(scenes) + 1}",
                    "genre": self._format_genres(movie_details.get('genres', [])),
                    "year": int(movie_details.get('release_date', '2000-01-01')[:4]),
                    "language": movie_details.get('original_language', 'en').upper(),
                    "country": self._get_country_from_language(movie_details.get('original_language', 'en')),
                    "type": "Movie",
                    "similarity": 0.0
                })
        
        # Process TV shows
        for tv_show in tv_shows:
            # Create scene entries for TV shows
            scenes.append({
                "id": len(scenes) + 1,
                "movie": tv_show.get('name', 'Unknown'),
                "description": tv_show.get('overview', 'No description available'),
                "image_url": f"https://image.tmdb.org/t/p/w500{tv_show.get('poster_path', '')}" if tv_show.get('poster_path') else f"https://picsum.photos/400/300?random={len(scenes) + 1}",
                "genre": "Drama/Thriller",  # Default genre for TV shows
                "year": int(tv_show.get('first_air_date', '2020-01-01')[:4]),
                "language": tv_show.get('original_language', 'en').upper(),
                "country": self._get_country_from_language(tv_show.get('original_language', 'en')),
                "type": "Web Series",
                "similarity": 0.0
            })
            
            # Create dialogue entries for TV shows
            dialogue_samples = self._generate_tv_dialogue_samples(tv_show)
            for dialogue in dialogue_samples:
                dialogues.append({
                    "id": len(dialogues) + 1,
                    "movie": tv_show.get('name', 'Unknown'),
                    "dialogue": dialogue,
                    "genre": "Drama/Thriller",
                    "year": int(tv_show.get('first_air_date', '2020-01-01')[:4]),
                    "language": tv_show.get('original_language', 'en').upper(),
                    "country": self._get_country_from_language(tv_show.get('original_language', 'en')),
                    "type": "Web Series"
                })
        
        # Add some popular Indian content manually since TMDB might not have extensive Indian content
        indian_content = self._get_indian_content()
        dialogues.extend(indian_content['dialogues'])
        scenes.extend(indian_content['scenes'])
        
        print(f"✓ Created dataset with {len(dialogues)} dialogues and {len(scenes)} scenes")
        return dialogues, scenes
    
    def _generate_dialogue_samples(self, movie_details: Dict) -> List[str]:
        """Generate sample dialogues based on movie genre and overview"""
        genre = self._format_genres(movie_details.get('genres', []))
        title = movie_details.get('title', 'Unknown')
        
        # Genre-based dialogue templates
        if 'Action' in genre:
            return [
                f"We need to stop them before it's too late!",
                f"This ends now!",
                f"I won't let you get away with this!"
            ]
        elif 'Romance' in genre:
            return [
                f"I've been waiting for you my whole life.",
                f"You make me want to be a better person.",
                f"I love you more than words can say."
            ]
        elif 'Comedy' in genre:
            return [
                f"That's not how this works, that's not how any of this works!",
                f"I have a bad feeling about this.",
                f"What could possibly go wrong?"
            ]
        elif 'Horror' in genre:
            return [
                f"Did you hear that?",
                f"We should get out of here.",
                f"Something's not right about this place."
            ]
        else:
            return [
                f"Everything happens for a reason.",
                f"Sometimes you have to take a leap of faith.",
                f"The truth will set you free."
            ]
    
    def _generate_tv_dialogue_samples(self, tv_show: Dict) -> List[str]:
        """Generate sample dialogues for TV shows"""
        return [
            "The game has changed, and so have the rules.",
            "Trust no one, not even yourself.",
            "Every choice has consequences."
        ]
    
    def _format_genres(self, genres: List[Dict]) -> str:
        """Format genre list into string"""
        if not genres:
            return "Drama"
        genre_names = [g.get('name', '') for g in genres[:2]]  # Take first 2 genres
        return '/'.join(genre_names) if genre_names else "Drama"
    
    def _get_country_from_language(self, language: str) -> str:
        """Map language code to country"""
        language_map = {
            'en': 'USA',
            'hi': 'India',
            'te': 'India',
            'ta': 'India',
            'ko': 'South Korea',
            'ja': 'Japan',
            'es': 'Spain',
            'fr': 'France',
            'de': 'Germany',
            'it': 'Italy'
        }
        return language_map.get(language.lower(), 'USA')
    
    def _get_indian_content(self) -> Dict:
        """Add popular Indian movies and web series"""
        indian_dialogues = [
            {
                "id": 1000,
                "movie": "3 Idiots",
                "dialogue": "All is well, all is well!",
                "genre": "Comedy/Drama",
                "year": 2009,
                "language": "Hindi",
                "country": "India",
                "type": "Movie"
            },
            {
                "id": 1001,
                "movie": "Dangal",
                "dialogue": "Gold medal laane ke liye khelna padega, sirf sapne dekhne se nahi milega.",
                "genre": "Sports/Biography",
                "year": 2016,
                "language": "Hindi",
                "country": "India",
                "type": "Movie"
            },
            {
                "id": 1002,
                "movie": "Sacred Games",
                "dialogue": "Mumbai meri jaan hai, aur main iski jaan hun.",
                "genre": "Crime/Thriller",
                "year": 2018,
                "language": "Hindi/English",
                "country": "India",
                "type": "Web Series"
            },
            {
                "id": 1003,
                "movie": "The Dark Knight",
                "dialogue": "Why so serious?",
                "genre": "Action/Crime",
                "year": 2008,
                "language": "English",
                "country": "USA",
                "type": "Movie"
            },
            {
                "id": 1004,
                "movie": "Interstellar",
                "dialogue": "Love is the one thing we're capable of perceiving that transcends dimensions of time and space.",
                "genre": "Sci-Fi/Drama",
                "year": 2014,
                "language": "English",
                "country": "USA",
                "type": "Movie"
            },
            {
                "id": 1005,
                "movie": "Money Heist",
                "dialogue": "No es un atraco, es una guerra.",
                "genre": "Crime/Thriller",
                "year": 2017,
                "language": "Spanish",
                "country": "Spain",
                "type": "Web Series"
            },
            {
                "id": 1006,
                "movie": "Baahubali",
                "dialogue": "Baahubali! Baahubali! Baahubali!",
                "genre": "Epic/Action",
                "year": 2015,
                "language": "Telugu/Hindi",
                "country": "India",
                "type": "Movie"
            },
            {
                "id": 1007,
                "movie": "The Family Man",
                "dialogue": "Family first, country second.",
                "genre": "Action/Thriller",
                "year": 2019,
                "language": "Hindi/English",
                "country": "India",
                "type": "Web Series"
            },
            {
                "id": 1008,
                "movie": "Parasite",
                "dialogue": "You know what kind of plan never fails? No plan.",
                "genre": "Thriller/Drama",
                "year": 2019,
                "language": "Korean",
                "country": "South Korea",
                "type": "Movie"
            },
            {
                "id": 1009,
                "movie": "KGF",
                "dialogue": "Violence, violence, violence. I don't like it. I avoid. But violence likes me.",
                "genre": "Action/Drama",
                "year": 2018,
                "language": "Kannada/Hindi",
                "country": "India",
                "type": "Movie"
            }
        ]
        
        indian_scenes = [
            {
                "id": 1000,
                "movie": "3 Idiots",
                "description": "Engineering college campus with students studying and having fun, hostel rooms and classrooms",
                "image_url": "https://picsum.photos/400/300?random=1000",
                "video_url": "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4",
                "genre": "Comedy/Drama",
                "year": 2009,
                "language": "Hindi",
                "country": "India",
                "type": "Movie",
                "similarity": 0.0
            },
            {
                "id": 1001,
                "movie": "Dangal",
                "description": "Wrestling arena with intense training and competition scenes, rural Indian village setting",
                "image_url": "https://picsum.photos/400/300?random=1001",
                "video_url": "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_2mb.mp4",
                "genre": "Sports/Biography",
                "year": 2016,
                "language": "Hindi",
                "country": "India",
                "type": "Movie",
                "similarity": 0.0
            },
            {
                "id": 1002,
                "movie": "Sacred Games",
                "description": "Mumbai underworld with slums, police stations, and gritty urban landscapes",
                "image_url": "https://picsum.photos/400/300?random=1002",
                "video_url": "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_5mb.mp4",
                "genre": "Crime/Thriller",
                "year": 2018,
                "language": "Hindi/English",
                "country": "India",
                "type": "Web Series",
                "similarity": 0.0
            },
            {
                "id": 1003,
                "movie": "The Dark Knight",
                "description": "Gotham City at night with Batman confronting Joker, dark urban setting with dramatic lighting",
                "image_url": "https://picsum.photos/400/300?random=1003",
                "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
                "genre": "Action/Crime",
                "year": 2008,
                "language": "English",
                "country": "USA",
                "type": "Movie",
                "similarity": 0.0
            },
            {
                "id": 1004,
                "movie": "Interstellar",
                "description": "Space station near black hole with cosmic phenomena and emotional father-daughter moments",
                "image_url": "https://picsum.photos/400/300?random=1004",
                "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
                "genre": "Sci-Fi/Drama",
                "year": 2014,
                "language": "English",
                "country": "USA",
                "type": "Movie",
                "similarity": 0.0
            },
            {
                "id": 1005,
                "movie": "Money Heist",
                "description": "Royal Mint of Spain with red jumpsuits, hostage situation and elaborate heist setup",
                "image_url": "https://picsum.photos/400/300?random=1005",
                "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
                "genre": "Crime/Thriller",
                "year": 2017,
                "language": "Spanish",
                "country": "Spain",
                "type": "Web Series",
                "similarity": 0.0
            },
            {
                "id": 1006,
                "movie": "Baahubali",
                "description": "Ancient kingdom with grand palaces, waterfalls, and epic battle sequences with elephants and warriors",
                "image_url": "https://picsum.photos/400/300?random=1006",
                "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4",
                "genre": "Epic/Action",
                "year": 2015,
                "language": "Telugu/Hindi",
                "country": "India",
                "type": "Movie",
                "similarity": 0.0
            },
            {
                "id": 1007,
                "movie": "The Family Man",
                "description": "Delhi/Mumbai urban settings with government offices, family home and action sequences",
                "image_url": "https://picsum.photos/400/300?random=1007",
                "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4",
                "genre": "Action/Thriller",
                "year": 2019,
                "language": "Hindi/English",
                "country": "India",
                "type": "Web Series",
                "similarity": 0.0
            },
            {
                "id": 1008,
                "movie": "Parasite",
                "description": "Modern Seoul with stark contrast between wealthy mansion and poor semi-basement apartment",
                "image_url": "https://picsum.photos/400/300?random=1008",
                "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/VolkswagenGTIReview.mp4",
                "genre": "Thriller/Drama",
                "year": 2019,
                "language": "Korean",
                "country": "South Korea",
                "type": "Movie",
                "similarity": 0.0
            },
            {
                "id": 1009,
                "movie": "KGF",
                "description": "Gold mining fields with intense action sequences, underground mines and period setting",
                "image_url": "https://picsum.photos/400/300?random=1009",
                "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WhatCarCanYouGetForAGrand.mp4",
                "genre": "Action/Drama",
                "year": 2018,
                "language": "Kannada/Hindi",
                "country": "India",
                "type": "Movie",
                "similarity": 0.0
            }
        ]
        
        return {"dialogues": indian_dialogues, "scenes": indian_scenes}
    
    def compute_embeddings(self, dialogues: List[Dict], scenes: List[Dict], model_manager):
        """Compute embeddings for all dialogues and scenes"""
        print("Computing embeddings...")
        
        # Compute text embeddings
        dialogue_texts = [d['dialogue'] for d in dialogues]
        scene_texts = [s['description'] for s in scenes]
        
        self.text_embeddings = []
        for text in dialogue_texts + scene_texts:
            embedding = model_manager.encode_text(text)
            self.text_embeddings.append(embedding)
        
        print("✓ Text embeddings computed")
        
        # Create placeholder images for scenes and compute image embeddings
        self.image_embeddings = []
        for scene in scenes:
            # Create a colored image based on genre
            color = self._get_genre_color(scene['genre'])
            img = Image.new('RGB', config.IMAGE_SIZE, color=color)
            embedding = model_manager.encode_image(img)
            self.image_embeddings.append(embedding)
        
        print("✓ Image embeddings computed")
        
        self.dialogues = dialogues
        self.scenes = scenes
    
    def _get_genre_color(self, genre: str) -> Tuple[int, int, int]:
        """Get color based on genre"""
        genre_colors = {
            "Action": (139, 0, 0),      # Dark red
            "Comedy": (255, 215, 0),    # Gold
            "Drama": (70, 130, 180),    # Steel blue
            "Horror": (25, 25, 112),    # Midnight blue
            "Romance": (255, 20, 147),  # Deep pink
            "Sci-Fi": (0, 191, 255),    # Deep sky blue
            "Thriller": (105, 105, 105), # Dim gray
            "Crime": (139, 69, 19),     # Saddle brown
        }
        
        for key, color in genre_colors.items():
            if key in genre:
                return color
        return (100, 100, 100)  # Default gray

# Global data manager instance
data_manager = DataManager()
