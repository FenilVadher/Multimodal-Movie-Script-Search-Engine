"""
Search engine for multimodal movie script search
"""
import numpy as np
from typing import List, Dict, Tuple
import config

class SearchEngine:
    def __init__(self, model_manager, data_manager):
        self.model_manager = model_manager
        self.data_manager = data_manager
    
    def search_dialogue_to_scene(self, query: str) -> List[Dict]:
        """Search for scenes based on dialogue query"""
        # Encode the query
        query_embedding = self.model_manager.encode_text(query)
        
        # Compute similarities with all scenes
        similarities = []
        for i, scene in enumerate(self.data_manager.scenes):
            scene_embedding = self.data_manager.text_embeddings[len(self.data_manager.dialogues) + i]
            similarity = self.model_manager.compute_similarity(query_embedding, scene_embedding)
            similarities.append((similarity, scene))
        
        # Sort by similarity and return top results
        similarities.sort(key=lambda x: x[0], reverse=True)
        
        # Filter by threshold and limit results
        results = []
        for similarity, scene in similarities[:config.MAX_RESULTS]:
            if similarity >= config.SIMILARITY_THRESHOLD:
                scene_copy = scene.copy()
                scene_copy['similarity'] = float(similarity)
                results.append(scene_copy)
        
        return results
    
    def search_scene_to_dialogue(self, query: str) -> List[Dict]:
        """Search for dialogues based on scene description query"""
        # Encode the query
        query_embedding = self.model_manager.encode_text(query)
        
        # Compute similarities with all dialogues
        similarities = []
        for i, dialogue in enumerate(self.data_manager.dialogues):
            dialogue_embedding = self.data_manager.text_embeddings[i]
            similarity = self.model_manager.compute_similarity(query_embedding, dialogue_embedding)
            similarities.append((similarity, dialogue))
        
        # Sort by similarity and return top results
        similarities.sort(key=lambda x: x[0], reverse=True)
        
        # Filter by threshold and limit results
        results = []
        for similarity, dialogue in similarities[:config.MAX_RESULTS]:
            if similarity >= config.SIMILARITY_THRESHOLD:
                dialogue_copy = dialogue.copy()
                dialogue_copy['similarity'] = float(similarity)
                results.append(dialogue_copy)
        
        return results
    
    def contextual_search(self, query: str) -> List[Dict]:
        """Perform contextual search combining dialogue and scene matching"""
        # Get both dialogue and scene results
        dialogue_results = self.search_scene_to_dialogue(query)
        scene_results = self.search_dialogue_to_scene(query)
        
        # Create contextual results by pairing dialogues with scenes from same movie
        contextual_results = []
        
        for scene in scene_results[:config.MAX_RESULTS]:
            # Find matching dialogue from same movie
            matching_dialogue = None
            for dialogue in dialogue_results:
                if dialogue['movie'] == scene['movie']:
                    matching_dialogue = dialogue['dialogue']
                    break
            
            if not matching_dialogue:
                # Use a generic dialogue if no match found
                matching_dialogue = "This is a memorable moment from the movie."
            
            contextual_result = {
                'similarity': scene['similarity'],
                'scene': scene,
                'dialogue': matching_dialogue
            }
            contextual_results.append(contextual_result)
        
        return contextual_results
    
    def summarize_text(self, text: str) -> Dict:
        """Summarize given text"""
        summary = self.model_manager.summarize_text(text)
        return {
            'original_text': text,
            'summary': summary,
            'original_length': len(text),
            'summary_length': len(summary)
        }
    
    def generate_script(self, prompt: str) -> Dict:
        """Generate script based on prompt"""
        generated_text = self.model_manager.generate_text(prompt)
        return {
            'prompt': prompt,
            'generated_script': generated_text,
            'length': len(generated_text)
        }

# Global search engine instance (will be initialized in app.py)
search_engine = None
