"""
Simple Flask backend for testing frontend connection
Uses mock data instead of AI models to avoid dependency issues
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

# Mock dataset
MOCK_SCENES = [
    {
        "id": 1001,
        "movie": "3 Idiots",
        "description": "College dormitory with friends discussing life and dreams",
        "image_url": "https://picsum.photos/400/300?random=1001",
        "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
        "genre": "Comedy/Drama",
        "year": 2009,
        "language": "Hindi",
        "country": "India",
        "type": "Movie",
        "similarity": 0.85
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
        "similarity": 0.75
    },
    {
        "id": 1003,
        "movie": "The Dark Knight",
        "description": "Gotham City rooftop with Batman confronting Joker in dramatic nighttime scene",
        "image_url": "https://picsum.photos/400/300?random=1003",
        "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/SubaruOutbackOnStreetAndDirt.mp4",
        "genre": "Action/Crime",
        "year": 2008,
        "language": "English",
        "country": "USA",
        "type": "Movie",
        "similarity": 0.65
    }
]

MOCK_DIALOGUES = [
    {
        "id": 2001,
        "movie": "3 Idiots",
        "dialogue": "All is well! All is well!",
        "character": "Rancho",
        "context": "Encouraging friends during stressful situations",
        "genre": "Comedy/Drama",
        "year": 2009,
        "language": "Hindi",
        "country": "India",
        "type": "Movie",
        "similarity": 0.90
    },
    {
        "id": 2007,
        "movie": "The Family Man",
        "dialogue": "Family first, everything else second",
        "character": "Srikant Tiwari",
        "context": "Balancing work and family responsibilities",
        "genre": "Action/Thriller",
        "year": 2019,
        "language": "Hindi/English",
        "country": "India",
        "type": "Web Series",
        "similarity": 0.80
    },
    {
        "id": 2003,
        "movie": "The Dark Knight",
        "dialogue": "Why so serious?",
        "character": "Joker",
        "context": "Joker's menacing question to his victims",
        "genre": "Action/Crime",
        "year": 2008,
        "language": "English",
        "country": "USA",
        "type": "Movie",
        "similarity": 0.70
    }
]

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'models_loaded': True,
        'message': 'Simple backend running with mock data'
    })

@app.route('/api/search/dialogue-to-scene', methods=['POST'])
def dialogue_to_scene():
    data = request.get_json()
    dialogue = data.get('dialogue', '').lower()
    
    # Simple keyword matching for demo
    results = []
    for scene in MOCK_SCENES:
        score = 0.1
        if 'family' in dialogue:
            if 'family' in scene['movie'].lower() or 'family' in scene['description'].lower():
                score = 0.85
        elif 'well' in dialogue or 'all is well' in dialogue:
            if '3 idiots' in scene['movie'].lower():
                score = 0.90
        elif 'serious' in dialogue or 'why so serious' in dialogue:
            if 'dark knight' in scene['movie'].lower() or 'batman' in scene['description'].lower():
                score = 0.88
        else:
            score = scene['similarity'] * 0.5
            
        scene_copy = scene.copy()
        scene_copy['similarity'] = score
        results.append(scene_copy)
    
    # Sort by similarity and limit to top 3
    results.sort(key=lambda x: x['similarity'], reverse=True)
    results = results[:3]
    
    return jsonify({
        'query': dialogue,
        'results': results,
        'total_results': len(results)
    })

@app.route('/api/search/scene-to-dialogue', methods=['POST'])
def scene_to_dialogue():
    # For image upload, return mock dialogues
    results = MOCK_DIALOGUES[:3]
    
    return jsonify({
        'query': 'uploaded_image',
        'results': results,
        'total_results': len(results)
    })

@app.route('/api/search/contextual', methods=['POST'])
def contextual_search():
    dialogue = request.form.get('dialogue', '').lower()
    
    # Combine dialogue and scene results for contextual search
    combined_results = []
    
    # Add some scenes
    for scene in MOCK_SCENES[:2]:
        combined_results.append({
            'type': 'scene',
            'content': scene,
            'similarity': scene['similarity'] * 0.8
        })
    
    # Add some dialogues
    for dialogue_item in MOCK_DIALOGUES[:1]:
        combined_results.append({
            'type': 'dialogue', 
            'content': dialogue_item,
            'similarity': dialogue_item['similarity'] * 0.7
        })
    
    return jsonify({
        'query': dialogue,
        'results': combined_results,
        'total_results': len(combined_results)
    })

@app.route('/api/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    text = data.get('text', '')
    
    # Mock summarization
    summary = f"Summary: {text[:100]}..." if len(text) > 100 else f"Summary: {text}"
    
    return jsonify({
        'original_text': text,
        'summary': summary,
        'length_reduction': max(0, len(text) - len(summary))
    })

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt', '')
    gen_type = data.get('type', 'script')
    
    # Mock generation
    if gen_type == 'script':
        generated = f"Generated script based on: {prompt}\n\nCharacter 1: This is a mock generated dialogue.\nCharacter 2: Indeed, this demonstrates the generation capability."
    else:
        generated = f"Generated content for '{prompt}': This is mock generated text showing the API functionality."
    
    return jsonify({
        'prompt': prompt,
        'generated_text': generated,
        'type': gen_type
    })

@app.route('/api/dataset', methods=['GET'])
def get_dataset():
    return jsonify({
        'dialogues': MOCK_DIALOGUES,
        'scenes': MOCK_SCENES,
        'total_dialogues': len(MOCK_DIALOGUES),
        'total_scenes': len(MOCK_SCENES)
    })

if __name__ == '__main__':
    print("Starting Simple Movie Search Backend...")
    print("Backend will run on http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=True)
