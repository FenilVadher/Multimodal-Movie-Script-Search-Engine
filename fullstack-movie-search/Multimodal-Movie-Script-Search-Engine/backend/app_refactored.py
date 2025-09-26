"""
Refactored Flask application for Multimodal Movie Script Search Engine
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import config
from models import model_manager
from data_manager import data_manager
from search_engine import SearchEngine
import search_engine as search_engine_module

app = Flask(__name__)
CORS(app)

def initialize_application():
    """Initialize all components of the application"""
    print("Initializing Multimodal Movie Script Search Engine...")
    
    # Load models
    model_manager.load_models()
    
    # Create real dataset using APIs
    dialogues, scenes = data_manager.create_real_dataset()
    
    # Compute embeddings
    data_manager.compute_embeddings(dialogues, scenes, model_manager)
    
    # Initialize search engine
    search_engine_module.search_engine = SearchEngine(model_manager, data_manager)
    
    print("✓ All models and embeddings loaded successfully!")
    print("Starting Flask server...")

@app.route('/api/search/dialogue-to-scene', methods=['POST'])
def dialogue_to_scene():
    """Search for scenes based on dialogue input"""
    try:
        data = request.get_json()
        dialogue = data.get('dialogue', '')
        
        if not dialogue:
            return jsonify({'error': 'Dialogue is required'}), 400
        
        results = search_engine_module.search_engine.search_dialogue_to_scene(dialogue)
        
        return jsonify({
            'query': dialogue,
            'results': results,
            'total_results': len(results)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search/scene-to-dialogue', methods=['POST'])
def scene_to_dialogue():
    """Search for dialogues based on scene description"""
    try:
        data = request.get_json()
        scene_description = data.get('scene_description', '')
        
        if not scene_description:
            return jsonify({'error': 'Scene description is required'}), 400
        
        results = search_engine_module.search_engine.search_scene_to_dialogue(scene_description)
        
        return jsonify({
            'query': scene_description,
            'results': results,
            'total_results': len(results)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search/contextual', methods=['POST'])
def contextual_search():
    """Perform contextual search combining dialogue and scene matching"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        results = search_engine_module.search_engine.contextual_search(query)
        
        return jsonify({
            'query': query,
            'results': results,
            'total_results': len(results)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/summarize', methods=['POST'])
def summarize():
    """Summarize given text"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        max_length = data.get('max_length', 150)
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        result = search_engine_module.search_engine.summarize_text(text)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate', methods=['POST'])
def generate():
    """Generate script based on prompt"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        max_length = data.get('max_length', 100)
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        result = search_engine_module.search_engine.generate_script(prompt)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': search_engine_module.search_engine is not None,
        'total_dialogues': len(data_manager.dialogues),
        'total_scenes': len(data_manager.scenes)
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get application statistics"""
    return jsonify({
        'total_dialogues': len(data_manager.dialogues),
        'total_scenes': len(data_manager.scenes),
        'max_results': config.MAX_RESULTS,
        'similarity_threshold': config.SIMILARITY_THRESHOLD
    })

if __name__ == '__main__':
    initialize_application()
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
