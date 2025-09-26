from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import numpy as np
import torch
from PIL import Image
import io
import base64
import requests
from sentence_transformers import SentenceTransformer
from transformers import CLIPProcessor, CLIPModel, BartForConditionalGeneration, BartTokenizer, GPT2LMHeadModel, GPT2Tokenizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
import os
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)

# Global variables for models and data
models = {}
embeddings = {}
dataset = {}

def initialize_models():
    """Initialize all pre-trained models"""
    print("Loading models...")
    
    # CLIP model for both text and image processing
    device = "cuda" if torch.cuda.is_available() else "cpu"
    models['clip'] = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    models['clip_processor'] = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    models['clip'].to(device)
    models['device'] = device
    print("✓ CLIP model loaded")
    
    # Keep Sentence-BERT for backup text processing
    models['text'] = SentenceTransformer('all-MiniLM-L6-v2')
    print("✓ Text model loaded")
    
    # Summarization model
    models['bart_tokenizer'] = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    models['bart_model'] = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
    print("✓ BART summarization model loaded")
    
    # Text generation model
    models['gpt2_tokenizer'] = GPT2Tokenizer.from_pretrained('gpt2')
    models['gpt2_model'] = GPT2LMHeadModel.from_pretrained('gpt2')
    models['gpt2_tokenizer'].pad_token = models['gpt2_tokenizer'].eos_token
    print("✓ GPT-2 generation model loaded")

def create_comprehensive_dataset():
    """Create comprehensive dataset with real movie/web series dialogues including Indian content"""
    dialogues = [
        # Hollywood Movies
        {
            "id": 1,
            "movie": "The Dark Knight",
            "dialogue": "Why do we fall sir? So that we can learn to pick ourselves up. It's not who I am underneath, but what I do that defines me. You either die a hero or live long enough to see yourself become the villain.",
            "scene_description": "Batman confronting Joker in Gotham City, dark urban setting with dramatic lighting",
            "genre": "Action/Crime",
            "year": 2008,
            "language": "English",
            "country": "USA"
        },
        {
            "id": 2,
            "movie": "Inception",
            "dialogue": "We need to go deeper. Dreams feel real while we're in them. It's only when we wake up that we realize something was actually strange. An idea is like a virus, resilient, highly contagious.",
            "scene_description": "Limbo dreamscape with impossible architecture, floating debris and surreal environments",
            "genre": "Sci-Fi/Thriller",
            "year": 2010,
            "language": "English",
            "country": "USA"
        },
        {
            "id": 3,
            "movie": "Interstellar",
            "dialogue": "Love is the one thing we're capable of perceiving that transcends dimensions of time and space. Don't let me leave, Murph! We used to look up at the sky and wonder at our place in the stars.",
            "scene_description": "Space station near black hole with cosmic phenomena and emotional father-daughter moments",
            "genre": "Sci-Fi/Drama",
            "year": 2014,
            "language": "English",
            "country": "USA"
        },
        # Indian Bollywood Movies
        {
            "id": 4,
            "movie": "3 Idiots",
            "dialogue": "All is well! Kamyabi ke peeche mat bhaago, excellence ka peecha karo, kamyabi jhak maarke tumhare peeche aayegi. Life mein sirf do tarah ke log hote hain - Simple aur Complicated.",
            "scene_description": "Engineering college campus with friends studying, hostel rooms and classroom scenes",
            "genre": "Comedy/Drama",
            "year": 2009,
            "language": "Hindi",
            "country": "India"
        },
        {
            "id": 5,
            "movie": "Dangal",
            "dialogue": "Mhari chhoriyaan chhoron se kam hain ke? Gold medal laane ke liye koi gender nahi hota. Sapne dekhna paap nahi, unhe poora na karna paap hai.",
            "scene_description": "Wrestling arena with father training daughters, rural Haryana setting with mud wrestling pit",
            "genre": "Sports/Biography",
            "year": 2016,
            "language": "Hindi",
            "country": "India"
        },
        {
            "id": 6,
            "movie": "Zindagi Na Milegi Dobara",
            "dialogue": "Dar ke aage jeet hai. Seize the day my friend, pehle is din ko puri tarah jiyo, phir agle din ke bare mein sochna. Life mein jo bhi karo, dil se karo.",
            "scene_description": "Spanish countryside with friends on adventure trip, skydiving and scenic landscapes",
            "genre": "Adventure/Comedy",
            "year": 2011,
            "language": "Hindi",
            "country": "India"
        },
        # South Indian Movies
        {
            "id": 7,
            "movie": "Baahubali",
            "dialogue": "Jai Mahishmati! Katappa ne Baahubali ko kyun maara? Rajmata ke aadesh se main Amarendra Baahubali ko maaronga. Shivudu, tu Baahubali hai!",
            "scene_description": "Ancient kingdom with grand palaces, waterfalls, and epic battle sequences with elephants and warriors",
            "genre": "Epic/Action",
            "year": 2015,
            "language": "Telugu/Hindi",
            "country": "India"
        },
        {
            "id": 8,
            "movie": "KGF",
            "dialogue": "Violence, violence, violence... I don't like it. I avoid it. But violence likes me. Main sirf paisa nahi kamana chahta, main history banana chahta hun.",
            "scene_description": "Gold mining underground tunnels with dark industrial setting and period costumes",
            "genre": "Action/Period",
            "year": 2018,
            "language": "Kannada/Hindi",
            "country": "India"
        },
        # Indian Web Series
        {
            "id": 9,
            "movie": "Scam 1992",
            "dialogue": "Risk hai toh ishq hai! Paisa bolta hai, aur main uski awaaz hun. Stock market mein sirf do cheez hoti hai - greed aur fear. Jab tak main zinda hun, main kheluga.",
            "scene_description": "1990s Mumbai stock exchange with vintage cars, old Bombay architecture and trading floors",
            "genre": "Crime/Biography",
            "year": 2020,
            "language": "Hindi",
            "country": "India",
            "type": "Web Series"
        },
        {
            "id": 10,
            "movie": "The Family Man",
            "dialogue": "Main ek middle class family man hun, lekin mere paas ek secret hai. Desh ki suraksha aur family ki khushi, dono sambhalna mushkil hai. Terrorism ka koi religion nahi hota.",
            "scene_description": "Delhi/Mumbai urban settings with government offices, family home and action sequences",
            "genre": "Action/Thriller",
            "year": 2019,
            "language": "Hindi/English",
            "country": "India",
            "type": "Web Series"
        },
        {
            "id": 11,
            "movie": "Sacred Games",
            "dialogue": "Kabhi kabhi lagta hai apun hi bhagwan hai. Mumbai meri jaan hai, aur main iski raksha karunga. Time is a flat circle, Sartaj. Trivedi saab, aapka game khatam.",
            "scene_description": "Mumbai underworld with slums, police stations, and gritty urban landscapes",
            "genre": "Crime/Thriller",
            "year": 2018,
            "language": "Hindi/English",
            "country": "India",
            "type": "Web Series"
        },
        # Regional Indian Cinema
        {
            "id": 12,
            "movie": "Arjun Reddy",
            "dialogue": "Preeti, I love you. Nenu chala aggressive ga untanu, kani naa love kuda antha aggressive. Alcohol and drugs naa pain ni marchipoye chance ivvavu.",
            "scene_description": "Medical college and modern urban Hyderabad with contemporary settings",
            "genre": "Romance/Drama",
            "year": 2017,
            "language": "Telugu",
            "country": "India"
        },
        {
            "id": 13,
            "movie": "Kumbakonam Gopals",
            "dialogue": "Vanakkam Chennai! Naan oru simple middle class payyan. Life la enna nadanthalum, namba family kaga fight pannanum. Success ku shortcut illa.",
            "scene_description": "Chennai city with traditional Tamil architecture, temples and modern IT offices",
            "genre": "Comedy/Family",
            "year": 2019,
            "language": "Tamil",
            "country": "India"
        },
        # International Content
        {
            "id": 14,
            "movie": "Parasite",
            "dialogue": "You know what kind of plan never fails? No plan. No plan at all. When you make a plan, life never works out that way. Crossing the line is so easy.",
            "scene_description": "Modern Seoul with stark contrast between wealthy mansion and semi-basement apartment",
            "genre": "Thriller/Dark Comedy",
            "year": 2019,
            "language": "Korean",
            "country": "South Korea"
        },
        {
            "id": 15,
            "movie": "Money Heist",
            "dialogue": "My name is Tokyo, and this is the story of how we robbed the Bank of Spain. Bella Ciao! The Professor always has a plan. Resistance is not futile.",
            "scene_description": "Royal Mint of Spain with red jumpsuits, hostage situation and elaborate heist setup",
            "genre": "Crime/Thriller",
            "year": 2017,
            "language": "Spanish",
            "country": "Spain",
            "type": "Web Series"
        }
    ]
    
    # Create corresponding images for each dialogue with more diverse and accurate representations
    images = []
    
    for i, dialogue in enumerate(dialogues):
        # Create more diverse colored images that match the movie themes
        if dialogue["genre"] in ["Action/Crime", "Action/Thriller", "Crime/Thriller"]:
            color = (30, 30, 50)  # Dark theme
        elif dialogue["genre"] in ["Sci-Fi/Thriller", "Sci-Fi/Drama", "Epic/Action"]:
            color = (20, 80, 120)  # Blue/cosmic theme
        elif dialogue["genre"] in ["Comedy/Drama", "Adventure/Comedy", "Romance/Drama"]:
            color = (120, 80, 40)  # Warm theme
        elif dialogue["genre"] in ["Sports/Biography", "Crime/Biography"]:
            color = (80, 120, 60)  # Natural theme
        else:
            color = (100, 100, 100)  # Neutral theme
            
        img = Image.new('RGB', (400, 300), color=color)
        images.append({
            "id": dialogue["id"],
            "image": img,
            "description": dialogue["scene_description"],
            "movie": dialogue["movie"],
            "genre": dialogue["genre"],
            "year": dialogue.get("year", 2020),
            "language": dialogue.get("language", "English"),
            "country": dialogue.get("country", "USA"),
            "type": dialogue.get("type", "Movie"),
            "url": f"https://picsum.photos/400/300?random={dialogue['id']}"
        })
    
    return dialogues, images

def compute_embeddings():
    """Compute embeddings for all dialogues and images"""
    print("Computing embeddings...")
    
    # Text embeddings using CLIP text encoder
    dialogue_texts = [d["dialogue"] for d in dataset['dialogues']]
    text_embeddings = []
    for text in dialogue_texts:
        inputs = models['clip_processor'](text=[text], return_tensors="pt", padding=True)
        inputs = {k: v.to(models['device']) for k, v in inputs.items()}
        
        with torch.no_grad():
            text_features = models['clip'].get_text_features(**inputs)
            text_embeddings.append(text_features.cpu().numpy())
    
    embeddings['text'] = np.vstack(text_embeddings)
    print("✓ Text embeddings computed")
    
    # Image embeddings
    image_embeddings = []
    for img_data in dataset['images']:
        inputs = models['clip_processor'](images=img_data["image"], return_tensors="pt")
        inputs = {k: v.to(models['device']) for k, v in inputs.items()}
        
        with torch.no_grad():
            image_features = models['clip'].get_image_features(**inputs)
            image_embeddings.append(image_features.cpu().numpy())
    
    embeddings['image'] = np.vstack(image_embeddings)
    print("✓ Image embeddings computed")

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "models_loaded": len(models) > 0})

@app.route('/api/search/dialogue-to-scene', methods=['POST'])
def dialogue_to_scene():
    """Search for scenes based on dialogue input"""
    try:
        data = request.get_json()
        query_text = data.get('dialogue', '')
        
        if not query_text:
            return jsonify({"error": "Dialogue text is required"}), 400
        
        # Encode query text using CLIP text encoder
        inputs = models['clip_processor'](text=[query_text], return_tensors="pt", padding=True)
        inputs = {k: v.to(models['device']) for k, v in inputs.items()}
        
        with torch.no_grad():
            query_embedding = models['clip'].get_text_features(**inputs).cpu().numpy()
        
        # Compute similarities with image embeddings
        similarities = cosine_similarity(query_embedding, embeddings['image'])[0]
        
        # Get top results with minimum similarity threshold and diversity
        similarity_threshold = 0.1
        valid_indices = np.where(similarities >= similarity_threshold)[0]
        
        if len(valid_indices) == 0:
            # If no results meet threshold, get top 5
            top_indices = np.argsort(similarities)[::-1][:5]
        else:
            # Sort valid results by similarity and take top 8 for diversity
            sorted_valid = valid_indices[np.argsort(similarities[valid_indices])[::-1]]
            top_indices = sorted_valid[:8]
        
        results = []
        seen_movies = set()
        
        for idx in top_indices:
            img_data = dataset['images'][idx]
            # Add diversity by avoiding duplicate movies in top results
            if len(results) < 3 or img_data["movie"] not in seen_movies:
                results.append({
                    "id": img_data["id"],
                    "movie": img_data["movie"],
                    "description": img_data["description"],
                    "image_url": img_data["url"],
                    "genre": img_data["genre"],
                    "year": img_data["year"],
                    "language": img_data["language"],
                    "country": img_data["country"],
                    "type": img_data["type"],
                    "similarity": float(similarities[idx])
                })
                seen_movies.add(img_data["movie"])
                
            if len(results) >= 6:  # Return up to 6 diverse results
                break
                
        return jsonify({
            "query": query_text,
            "results": results,
            "total_results": len(results)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/search/scene-to-dialogue', methods=['POST'])
def scene_to_dialogue():
    """Search for dialogues based on uploaded image"""
    try:
        if 'image' not in request.files:
            return jsonify({"error": "Image file is required"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No image selected"}), 400
        
        # Process uploaded image
        image = Image.open(file.stream)
        inputs = models['clip_processor'](images=image, return_tensors="pt")
        inputs = {k: v.to(models['device']) for k, v in inputs.items()}
        
        with torch.no_grad():
            query_embedding = models['clip'].get_image_features(**inputs).cpu().numpy()
        
        # Compute similarities with text embeddings
        similarities = cosine_similarity(query_embedding, embeddings['text'])[0]
        
        # Get top-3 results
        top_indices = np.argsort(similarities)[::-1][:3]
        
        results = []
        for idx in top_indices:
            dialogue_data = dataset['dialogues'][idx]
            results.append({
                "id": dialogue_data["id"],
                "movie": dialogue_data["movie"],
                "dialogue": dialogue_data["dialogue"],
                "scene_description": dialogue_data["scene_description"],
                "genre": dialogue_data["genre"],
                "similarity": float(similarities[idx])
            })
        
        return jsonify({
            "results": results,
            "total_results": len(results)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/search/contextual', methods=['POST'])
def contextual_search():
    """Combined search using both dialogue and image"""
    try:
        data = request.form
        query_text = data.get('dialogue', '')
        
        if not query_text:
            return jsonify({"error": "Dialogue text is required"}), 400
        
        if 'image' not in request.files:
            return jsonify({"error": "Image file is required"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No image selected"}), 400
        
        # Encode query text
        text_query_embedding = models['text'].encode([query_text])
        
        # Process uploaded image
        image = Image.open(file.stream)
        inputs = models['clip_processor'](images=image, return_tensors="pt")
        inputs = {k: v.to(models['device']) for k, v in inputs.items()}
        
        with torch.no_grad():
            image_query_embedding = models['clip'].get_image_features(**inputs).cpu().numpy()
        
        # Compute combined similarities
        text_similarities = cosine_similarity(text_query_embedding, embeddings['text'])[0]
        image_similarities = cosine_similarity(image_query_embedding, embeddings['image'])[0]
        
        # Combine similarities (weighted average)
        combined_similarities = 0.6 * text_similarities + 0.4 * image_similarities
        
        # Get top-3 results
        top_indices = np.argsort(combined_similarities)[::-1][:3]
        
        results = []
        for idx in top_indices:
            dialogue_data = dataset['dialogues'][idx]
            image_data = dataset['images'][idx]
            results.append({
                "id": dialogue_data["id"],
                "movie": dialogue_data["movie"],
                "dialogue": dialogue_data["dialogue"],
                "scene_description": dialogue_data["scene_description"],
                "genre": dialogue_data["genre"],
                "image_url": image_data["url"],
                "image_description": image_data["description"],
                "text_similarity": float(text_similarities[idx]),
                "image_similarity": float(image_similarities[idx]),
                "combined_similarity": float(combined_similarities[idx])
            })
        
        return jsonify({
            "query": query_text,
            "results": results,
            "total_results": len(results)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/summarize', methods=['POST'])
def summarize_text():
    """Summarize dialogue or script text"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "Text is required"}), 400
        
        # Tokenize and generate summary
        inputs = models['bart_tokenizer'](text, max_length=1024, return_tensors='pt', truncation=True)
        
        with torch.no_grad():
            summary_ids = models['bart_model'].generate(
                inputs['input_ids'],
                max_length=150,
                min_length=30,
                length_penalty=2.0,
                num_beams=4,
                early_stopping=True
            )
        
        summary = models['bart_tokenizer'].decode(summary_ids[0], skip_special_tokens=True)
        
        return jsonify({
            "original_text": text,
            "summary": summary,
            "original_length": len(text.split()),
            "summary_length": len(summary.split())
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate', methods=['POST'])
def generate_creative_text():
    """Generate creative text based on prompt"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        text_type = data.get('type', 'story')  # story, poem, dialogue
        
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400
        
        # Enhance prompt based on type
        if text_type == 'poem':
            enhanced_prompt = f"Write a poem about {prompt}:\n"
        elif text_type == 'dialogue':
            enhanced_prompt = f"Character 1: {prompt}\nCharacter 2:"
        else:  # story
            enhanced_prompt = f"Once upon a time, {prompt}"
        
        # Tokenize and generate
        inputs = models['gpt2_tokenizer'](enhanced_prompt, return_tensors='pt', padding=True)
        
        with torch.no_grad():
            outputs = models['gpt2_model'].generate(
                inputs['input_ids'],
                max_length=200,
                num_return_sequences=1,
                temperature=0.8,
                do_sample=True,
                pad_token_id=models['gpt2_tokenizer'].eos_token_id
            )
        
        generated_text = models['gpt2_tokenizer'].decode(outputs[0], skip_special_tokens=True)
        
        # Remove the original prompt from the generated text
        generated_text = generated_text[len(enhanced_prompt):].strip()
        
        return jsonify({
            "prompt": prompt,
            "type": text_type,
            "generated_text": generated_text
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/dataset', methods=['GET'])
def get_dataset():
    """Get the dummy dataset for frontend display"""
    return jsonify({
        "dialogues": dataset['dialogues'],
        "images": [
            {
                "id": img["id"],
                "movie": img["movie"],
                "description": img["description"],
                "url": img["url"]
            }
            for img in dataset['images']
        ]
    })

if __name__ == '__main__':
    print("Initializing Multimodal Movie Script Search Engine...")
    
    # Initialize models and dataset
    initialize_models()
    dataset['dialogues'], dataset['images'] = create_comprehensive_dataset()
    compute_embeddings()
    
    print("✓ All models and embeddings loaded successfully!")
    print("Starting Flask server...")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
