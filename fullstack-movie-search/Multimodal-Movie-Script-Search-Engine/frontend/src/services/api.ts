import axios from 'axios';
import { DialogueResult, SceneResult, ContextualResult, SummaryResponse, GenerationResponse, Dataset } from '../types/index.ts';
import { mockSearchAPI } from './mockApi';

const API_BASE_URL = 'http://localhost:5001/api';

// Check if we're in production (GitHub Pages) or development
const isProduction = window.location.hostname.includes('github.io') || window.location.hostname !== 'localhost';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

// Fallback to mock API if real API is not available
const withFallback = async <T>(apiCall: () => Promise<T>, mockCall: () => Promise<T>): Promise<T> => {
  if (isProduction) {
    return mockCall();
  }
  
  try {
    return await apiCall();
  } catch (error) {
    console.warn('API call failed, falling back to mock data:', error);
    return mockCall();
  }
};

export const searchAPI = {
  dialogueToScene: async (dialogue: string): Promise<{ results: SceneResult[] }> => {
    return withFallback(
      async () => {
        const response = await api.post('/search/dialogue-to-scene', { dialogue });
        return response.data;
      },
      () => mockSearchAPI.dialogueToScene(dialogue)
    );
  },

  sceneToDialogue: async (imageFile: File): Promise<{ results: DialogueResult[] }> => {
    return withFallback(
      async () => {
        const formData = new FormData();
        formData.append('image', imageFile);
        const response = await api.post('/search/scene-to-dialogue', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        return response.data;
      },
      () => mockSearchAPI.sceneToDialogue(imageFile)
    );
  },

  contextualSearch: async (dialogue: string, imageFile: File): Promise<{ results: ContextualResult[] }> => {
    return withFallback(
      async () => {
        const formData = new FormData();
        formData.append('dialogue', dialogue);
        formData.append('image', imageFile);
        const response = await api.post('/search/contextual', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        return response.data;
      },
      () => mockSearchAPI.contextualSearch(dialogue, imageFile)
    );
  },

  summarize: async (text: string): Promise<SummaryResponse> => {
    return withFallback(
      async () => {
        const response = await api.post('/summarize', { text });
        return response.data;
      },
      () => mockSearchAPI.summarize(text)
    );
  },

  generate: async (prompt: string, type: string): Promise<GenerationResponse> => {
    return withFallback(
      async () => {
        const response = await api.post('/generate', { prompt, type });
        return response.data;
      },
      () => mockSearchAPI.generate(prompt, type)
    );
  },

  getDataset: async (): Promise<Dataset> => {
    return withFallback(
      async () => {
        const response = await api.get('/dataset');
        return response.data;
      },
      () => mockSearchAPI.getDataset()
    );
  },

  healthCheck: async (): Promise<{ status: string; models_loaded: boolean }> => {
    return withFallback(
      async () => {
        const response = await api.get('/health');
        return response.data;
      },
      () => mockSearchAPI.healthCheck()
    );
  }
};
