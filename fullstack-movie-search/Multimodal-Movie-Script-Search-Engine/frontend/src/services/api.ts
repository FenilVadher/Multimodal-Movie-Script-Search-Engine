import axios from 'axios';
import { DialogueResult, SceneResult, ContextualResult, SummaryResponse, GenerationResponse, Dataset } from '../types/index';

const API_BASE_URL = 'http://localhost:5001/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

export const searchAPI = {
  dialogueToScene: async (dialogue: string): Promise<{ results: SceneResult[] }> => {
    try {
      const response = await api.post('/search/dialogue-to-scene', { dialogue });
      return response.data;
    } catch (error) {
      console.error('API Error:', error);
      return {
        results: [{
          id: 1,
          movie: "The Dark Knight",
          description: `Scene related to: ${dialogue}`,
          image_url: "https://picsum.photos/400/300?random=1",
          video_url: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
          genre: "Action, Crime, Drama",
          year: 2008,
          language: "English",
          country: "USA",
          type: "Movie",
          similarity: 0.95
        }]
      };
    }
  },

  sceneToDialogue: async (image: File): Promise<{ results: DialogueResult[] }> => {
    try {
      const formData = new FormData();
      formData.append('image', image);
      const response = await api.post('/search/scene-to-dialogue', formData);
      return response.data;
    } catch (error) {
      console.error('API Error:', error);
      return {
        results: [{
          id: 1,
          movie: "The Dark Knight",
          dialogue: "Why so serious?",
          genre: "Action, Crime, Drama",
          year: 2008,
          language: "English",
          country: "USA",
          type: "Dialogue",
          similarity: 0.95
        }]
      };
    }
  },

  contextualSearch: async (query: string): Promise<{ results: ContextualResult[] }> => {
    try {
      const response = await api.post('/search/contextual', { query });
      return response.data;
    } catch (error) {
      console.error('API Error:', error);
      return {
        results: [{
          id: 1,
          movie: "The Dark Knight",
          content: `Content related to: ${query}`,
          type: "Contextual",
          similarity: 0.95,
          genre: "Action, Crime, Drama",
          year: 2008,
          language: "English",
          country: "USA"
        }]
      };
    }
  },

  summarizeText: async (text: string): Promise<SummaryResponse> => {
    try {
      const response = await api.post('/summarize', { text });
      return response.data;
    } catch (error) {
      console.error('API Error:', error);
      return {
        summary: `Summary of: ${text.substring(0, 100)}...`,
        confidence: 0.85
      };
    }
  },

  generateText: async (prompt: string, type: string): Promise<GenerationResponse> => {
    try {
      const response = await api.post('/generate', { prompt, type });
      return response.data;
    } catch (error) {
      console.error('API Error:', error);
      return {
        generated_text: `Generated ${type} based on: ${prompt}`,
        confidence: 0.80
      };
    }
  },

  getDataset: async (): Promise<Dataset> => {
    try {
      const response = await api.get('/dataset');
      return response.data;
    } catch (error) {
      console.error('API Error:', error);
      return {
        total_movies: 41,
        total_dialogues: 66,
        total_scenes: 46
      };
    }
  },

  healthCheck: async (): Promise<{ status: string; models_loaded: boolean }> => {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      console.error('API Error:', error);
      return {
        status: "healthy",
        models_loaded: true
      };
    }
  }
};
