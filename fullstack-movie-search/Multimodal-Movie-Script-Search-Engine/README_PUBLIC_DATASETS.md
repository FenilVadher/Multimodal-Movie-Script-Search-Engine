# Multimodal Movie Script Search Engine - Public Datasets

## Overview
This enhanced version uses publicly available movie datasets and APIs for authentic movie search functionality.

## Data Sources
- **IMDb Top 250 Movies**: Classic and popular films
- **Famous Movie Quotes**: Iconic dialogues from cinema history
- **Bollywood Classics**: Popular Indian films (3 Idiots, Dangal, etc.)
- **International Cinema**: Films from Korea, Japan, France, Italy
- **Hollywood Blockbusters**: Marvel, Star Wars, Christopher Nolan films

## Current Dataset Statistics
- **Movies**: 30 curated films from public sources
- **Dialogues**: 24 famous movie quotes
- **Scenes**: 78 generated scenes based on movie genres
- **Languages**: English, Hindi, Korean, Japanese, French, Italian
- **Countries**: USA, India, South Korea, Japan, France, Italy

## API Integration Options

### TMDB (The Movie Database)
1. Get free API key from: https://www.themoviedb.org/settings/api
2. Replace `your_tmdb_api_key_here` in `app_public_fast.py`
3. Enables real-time movie data fetching

### OMDB (Open Movie Database)
1. Get free API key from: http://www.omdbapi.com/apikey.aspx
2. Replace `your_omdb_api_key_here` in `app_public_fast.py`
3. Provides additional movie metadata

## Famous Dialogues Included

### Hollywood Classics
- "Hope is a good thing, maybe the best of things" - The Shawshank Redemption
- "I'm gonna make him an offer he can't refuse" - The Godfather
- "Why so serious?" - The Dark Knight
- "Life is like a box of chocolates" - Forrest Gump
- "May the Force be with you" - Star Wars
- "There is no spoon" - The Matrix

### Bollywood Hits
- "All is well! All is well!" - 3 Idiots
- "Pursue excellence, and success will follow" - 3 Idiots
- "Gold is gold, whether won by a boy or a girl" - Dangal

### International Cinema
- "You know what kind of plan never fails? No plan" - Parasite (Korean)

## Search Features

### Dialogue-to-Scene Search
- Advanced similarity algorithms
- Phrase matching and word overlap
- Genre-based scene generation
- Multi-language support

### Scene-to-Dialogue Search
- Intelligent dialogue scoring
- Character-based weighting
- Movie popularity factors
- Length and content analysis

### Contextual Search
- Combines dialogue and image inputs
- Mixed result types (scenes + dialogues)
- Contextual similarity scoring

## Technical Architecture

### Backend (Flask)
- **File**: `app_public_fast.py`
- **Port**: 5001
- **Features**: CORS enabled, JSON APIs, error handling
- **Dependencies**: Flask, NumPy, Requests

### Frontend (React)
- **Port**: 3000
- **Features**: Three search modes, file upload, responsive UI
- **Technologies**: TypeScript, Tailwind CSS

### Data Processing
- **Similarity Computation**: Advanced text matching algorithms
- **Scene Generation**: Genre-based templates
- **Metadata Enrichment**: Real movie information

## Usage Examples

### Test Queries
```bash
# Test dialogue search
curl -X POST http://localhost:5001/api/search/dialogue-to-scene \
  -H "Content-Type: application/json" \
  -d '{"dialogue": "Why so serious"}'

# Test health endpoint
curl -X GET http://localhost:5001/api/health
```

### Frontend Testing
1. Open http://localhost:3000
2. Try "Dialogue → Scene" tab with famous quotes
3. Upload images in "Scene → Dialogue" tab
4. Use "Contextual Search" for combined queries

## Extending the Dataset

### Adding More Movies
Edit the `movies_data` array in `app_public_fast.py`:
```python
{"title": "New Movie", "year": 2023, "genre": ["Drama"], 
 "country": "USA", "language": "English", "rating": 8.0}
```

### Adding More Dialogues
Edit the `dialogs_data` array:
```python
{"movie": "Movie Name", "character": "Character", 
 "text": "Famous quote", "scene": "Scene description"}
```

## Performance Optimization
- Curated dataset for fast loading
- Efficient similarity algorithms
- Caching for repeated queries
- Minimal external dependencies

## Future Enhancements
1. **Real AI Models**: Integrate CLIP for image processing
2. **Larger Datasets**: Cornell Movie Dialogs Corpus
3. **API Expansion**: More movie database APIs
4. **Language Models**: GPT integration for generation
5. **Vector Search**: Semantic similarity with embeddings

## Troubleshooting

### Backend Issues
- Check port 5001 availability
- Verify Python dependencies
- Review console logs for errors

### Frontend Issues
- Ensure port 3000 is free
- Check API connectivity
- Verify CORS configuration

### Data Issues
- Validate JSON structure
- Check similarity algorithm parameters
- Review search query formatting

## Contributing
This project uses publicly available movie data. When adding new content:
1. Ensure data is from public sources
2. Include proper attribution
3. Respect copyright and fair use
4. Document data sources

## License
This project uses publicly available movie data and respects fair use guidelines for educational and research purposes.
