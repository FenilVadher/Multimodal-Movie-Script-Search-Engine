export interface SearchResult {
  id: number;
  movie: string;
  similarity: number;
}

export interface DialogueResult {
  id: number;
  movie: string;
  dialogue: string;
  genre: string;
  year: number;
  language: string;
  country: string;
  type: string;
  similarity: number;
}

export interface SceneResult {
  id: number;
  movie: string;
  description: string;
  image_url: string;
  video_url: string;
  genre: string;
  year: number;
  language: string;
  country: string;
  type: string;
  similarity: number;
}

export interface ContextualResult {
  type: 'scene' | 'dialogue';
  content: SceneResult | DialogueResult;
  similarity: number;
}

export interface SummaryResponse {
  original_text: string;
  summary: string;
  original_length: number;
  summary_length: number;
}

export interface GenerationResponse {
  prompt: string;
  type: string;
  generated_text: string;
}

export interface Dataset {
  dialogues: Array<{
    id: number;
    movie: string;
    dialogue: string;
    scene_description: string;
    genre: string;
  }>;
  images: Array<{
    id: number;
    movie: string;
    description: string;
    url: string;
  }>;
}
