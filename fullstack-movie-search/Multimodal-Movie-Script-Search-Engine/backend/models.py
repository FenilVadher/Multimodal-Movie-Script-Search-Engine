"""
Model loading and management for the Multimodal Movie Script Search Engine
"""
import torch
import numpy as np
from transformers import CLIPProcessor, CLIPModel, BartForConditionalGeneration, BartTokenizer, GPT2LMHeadModel, GPT2Tokenizer
from sentence_transformers import SentenceTransformer
from PIL import Image
import config

class ModelManager:
    def __init__(self):
        self.clip_model = None
        self.clip_processor = None
        self.text_model = None
        self.bart_model = None
        self.bart_tokenizer = None
        self.gpt2_model = None
        self.gpt2_tokenizer = None
        
    def load_models(self):
        """Load all required models"""
        print("Loading models...")
        
        # Load CLIP model for image-text similarity
        print("✓ Loading CLIP model...")
        self.clip_model = CLIPModel.from_pretrained(config.CLIP_MODEL_NAME)
        self.clip_processor = CLIPProcessor.from_pretrained(config.CLIP_MODEL_NAME)
        print("✓ CLIP model loaded")
        
        # Load text embedding model
        print("✓ Loading text model...")
        self.text_model = SentenceTransformer(config.TEXT_MODEL_NAME)
        print("✓ Text model loaded")
        
        # Load BART for summarization
        print("✓ Loading BART model...")
        self.bart_model = BartForConditionalGeneration.from_pretrained(config.BART_MODEL_NAME)
        self.bart_tokenizer = BartTokenizer.from_pretrained(config.BART_MODEL_NAME)
        print("✓ BART summarization model loaded")
        
        # Load GPT-2 for text generation
        print("✓ Loading GPT-2 model...")
        self.gpt2_model = GPT2LMHeadModel.from_pretrained(config.GPT2_MODEL_NAME)
        self.gpt2_tokenizer = GPT2Tokenizer.from_pretrained(config.GPT2_MODEL_NAME)
        self.gpt2_tokenizer.pad_token = self.gpt2_tokenizer.eos_token
        print("✓ GPT-2 generation model loaded")
        
    def encode_text(self, text):
        """Encode text using the text model"""
        return self.text_model.encode([text])[0]
    
    def encode_image(self, image):
        """Encode image using CLIP model"""
        inputs = self.clip_processor(images=image, return_tensors="pt")
        with torch.no_grad():
            image_features = self.clip_model.get_image_features(**inputs)
        return image_features.squeeze().numpy()
    
    def compute_similarity(self, embedding1, embedding2):
        """Compute cosine similarity between two embeddings"""
        return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
    
    def summarize_text(self, text, max_length=150):
        """Summarize text using BART model"""
        inputs = self.bart_tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
        with torch.no_grad():
            summary_ids = self.bart_model.generate(inputs, max_length=max_length, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
        return self.bart_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    def generate_text(self, prompt, max_length=100):
        """Generate text using GPT-2 model"""
        inputs = self.gpt2_tokenizer.encode(prompt, return_tensors="pt")
        with torch.no_grad():
            outputs = self.gpt2_model.generate(
                inputs, 
                max_length=len(inputs[0]) + max_length,
                num_return_sequences=1,
                temperature=0.7,
                pad_token_id=self.gpt2_tokenizer.eos_token_id,
                do_sample=True
            )
        return self.gpt2_tokenizer.decode(outputs[0], skip_special_tokens=True)

# Global model manager instance
model_manager = ModelManager()
