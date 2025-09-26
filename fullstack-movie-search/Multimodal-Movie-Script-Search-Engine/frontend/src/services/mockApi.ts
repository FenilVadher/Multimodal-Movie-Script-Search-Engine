import { DialogueResult, SceneResult, ContextualResult, SummaryResponse, GenerationResponse, Dataset } from '../types/index';

// Mock data based on your backend
const mockMoviesData = [
  { title: "The Shawshank Redemption", year: 1994, genre: ["Drama"], country: "USA", language: "English", rating: 9.3 },
  { title: "The Dark Knight", year: 2008, genre: ["Action", "Crime", "Drama"], country: "USA", language: "English", rating: 9.0 },
  { title: "Inception", year: 2010, genre: ["Action", "Sci-Fi", "Thriller"], country: "USA", language: "English", rating: 8.8 },
  { title: "The Matrix", year: 1999, genre: ["Action", "Sci-Fi"], country: "USA", language: "English", rating: 8.7 },
  { title: "3 Idiots", year: 2009, genre: ["Comedy", "Drama"], country: "India", language: "Hindi", rating: 8.4 },
  { title: "Dangal", year: 2016, genre: ["Biography", "Drama", "Sport"], country: "India", language: "Hindi", rating: 8.3 },
  { title: "Parasite", year: 2019, genre: ["Comedy", "Drama", "Thriller"], country: "South Korea", language: "Korean", rating: 8.5 },
  { title: "Spirited Away", year: 2001, genre: ["Animation", "Adventure", "Family"], country: "Japan", language: "Japanese", rating: 9.2 }
];

const mockDialogues = [
  { id: 1, dialogue: "Why so serious?", movie: "The Dark Knight", scene_description: "Joker interrogation scene", genre: "Action, Crime, Drama" },
  { id: 2, dialogue: "All is well", movie: "3 Idiots", scene_description: "Engineering college motivational scene", genre: "Comedy, Drama" },
  { id: 3, dialogue: "I'll be back", movie: "Terminator 2", scene_description: "Terminator promise scene", genre: "Action, Sci-Fi" },
  { id: 4, dialogue: "May the Force be with you", movie: "Star Wars", scene_description: "Jedi blessing scene", genre: "Adventure, Fantasy, Sci-Fi" },
  { id: 5, dialogue: "Hakuna Matata", movie: "The Lion King", scene_description: "Timon and Pumbaa philosophy scene", genre: "Animation, Adventure, Drama" },
  { id: 6, dialogue: "There is no spoon", movie: "The Matrix", scene_description: "Oracle's apartment spoon bending scene", genre: "Action, Sci-Fi" },
  { id: 7, dialogue: "We need to go deeper", movie: "Inception", scene_description: "Dream layer explanation scene", genre: "Action, Sci-Fi, Thriller" }
];

const mockScenes = [
  {
    id: 1,
    movie: "The Dark Knight",
    description: "Joker confronts Batman in dark interrogation room asking why so serious",
    dialogue: "Why so serious?",
    character: "Joker",
    keywords: ["interrogation", "joker", "batman", "serious"],
    image_url: "https://picsum.photos/400/300?random=1",
    video_url: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
  },
  {
    id: 2,
    movie: "3 Idiots",
    description: "Rancho teaches his friends about optimism and engineering with all is well philosophy",
    dialogue: "All is well",
    character: "Rancho",
    keywords: ["optimism", "engineering", "friendship", "well"],
    image_url: "https://picsum.photos/400/300?random=2",
    video_url: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4"
  },
  {
    id: 3,
    movie: "Inception",
    description: "Dream explanation scene with Cobb teaching about dreams feeling real",
    dialogue: "We need to go deeper",
    character: "Cobb",
    keywords: ["dreams", "reality", "deeper", "inception"],
    image_url: "https://picsum.photos/400/300?random=3",
    video_url: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"
  },
  {
    id: 4,
    movie: "The Matrix",
    description: "Oracle's apartment scene with spoon bending and there is no spoon",
    dialogue: "There is no spoon",
    character: "Spoon Boy",
    keywords: ["spoon", "matrix", "reality", "oracle"],
    image_url: "https://picsum.photos/400/300?random=4",
    video_url: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4"
  }
];

// Simple similarity function
function calculateSimilarity(query: string, item: any): number {
  const queryLower = query.toLowerCase();
  const queryWords = queryLower.split(/\s+/);
  
  // Check for exact dialogue match
  if (item.dialogue && item.dialogue.toLowerCase().includes(queryLower)) {
    return 0.95;
  }
  
  // Check keywords
  let keywordScore = 0;
  if (item.keywords) {
    const matchingKeywords = item.keywords.filter((keyword: string) => 
      queryWords.some(word => keyword.toLowerCase().includes(word.toLowerCase()) || 
                            word.toLowerCase().includes(keyword.toLowerCase()))
    );
    keywordScore = matchingKeywords.length / Math.max(queryWords.length, 1);
  }
  
  // Check description
  let descriptionScore = 0;
  if (item.description) {
    const descriptionWords = item.description.toLowerCase().split(/\s+/);
    const matchingWords = queryWords.filter(word => 
      descriptionWords.some(descWord => descWord.includes(word) || word.includes(descWord))
    );
    descriptionScore = matchingWords.length / Math.max(queryWords.length, 1);
  }
  
  // Check movie title
  let titleScore = 0;
  if (item.movie) {
    const titleWords = item.movie.toLowerCase().split(/\s+/);
    const matchingTitleWords = queryWords.filter(word => 
      titleWords.some(titleWord => titleWord.includes(word) || word.includes(titleWord))
    );
    titleScore = matchingTitleWords.length / Math.max(queryWords.length, 1);
  }
  
  // Calculate final score
  const finalScore = (keywordScore * 0.4) + (descriptionScore * 0.4) + (titleScore * 0.2);
  return Math.max(finalScore, 0.15); // Minimum relevance
}

export const mockSearchAPI = {
  dialogueToScene: async (dialogue: string): Promise<{ results: SceneResult[] }> => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500));
    
    const results = mockScenes
      .map(scene => ({
        ...scene,
        similarity: calculateSimilarity(dialogue, scene),
        type: "Movie" as const,
        genre: mockMoviesData.find(m => m.title === scene.movie)?.genre.join(", ") || "Drama",
        year: mockMoviesData.find(m => m.title === scene.movie)?.year || 2000,
        country: mockMoviesData.find(m => m.title === scene.movie)?.country || "USA",
        language: mockMoviesData.find(m => m.title === scene.movie)?.language || "English"
      }))
      .sort((a, b) => b.similarity - a.similarity)
      .slice(0, 10);
    
    return { results };
  },

  sceneToDialogue: async (imageFile: File): Promise<{ results: DialogueResult[] }> => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 800));
    
    // For demo purposes, return random dialogues
    const results = mockDialogues
      .slice(0, 5)
      .map((dialogue, index) => ({
        ...dialogue,
        id: index + 1,
        similarity: 0.8 - (index * 0.1),
        type: "Dialogue" as const,
        genre: mockMoviesData.find(m => m.title === dialogue.movie)?.genre.join(", ") || "Drama",
        year: mockMoviesData.find(m => m.title === dialogue.movie)?.year || 2000,
        country: mockMoviesData.find(m => m.title === dialogue.movie)?.country || "USA",
        language: mockMoviesData.find(m => m.title === dialogue.movie)?.language || "English",
        image_url: `https://picsum.photos/400/300?random=${index + 10}`,
        video_url: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
      }));
    
    return { results };
  },

  contextualSearch: async (dialogue: string, imageFile: File): Promise<{ results: ContextualResult[] }> => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    const results = mockScenes
      .map(scene => ({
        ...scene,
        similarity: calculateSimilarity(dialogue, scene) * 0.9, // Slightly lower for contextual
        type: "Contextual" as const,
        genre: mockMoviesData.find(m => m.title === scene.movie)?.genre.join(", ") || "Drama",
        year: mockMoviesData.find(m => m.title === scene.movie)?.year || 2000,
        country: mockMoviesData.find(m => m.title === scene.movie)?.country || "USA",
        language: mockMoviesData.find(m => m.title === scene.movie)?.language || "English"
      }))
      .sort((a, b) => b.similarity - a.similarity)
      .slice(0, 8);
    
    return { results };
  },

  summarize: async (text: string): Promise<SummaryResponse> => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1200));
    
    const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
    const keyPoints = sentences.slice(0, 3).map(s => s.trim());
    const summary = sentences.slice(0, 2).join('. ') + '.';
    
    return {
      summary,
      key_points: keyPoints,
      word_count: text.split(/\s+/).length,
      processing_time: "1.2s"
    };
  },

  generate: async (prompt: string, type: string): Promise<GenerationResponse> => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    const templates = {
      script: `FADE IN:

INT. ${prompt.toUpperCase()} - DAY

A compelling scene unfolds, exploring themes of ${prompt}. The characters engage in meaningful dialogue that reveals their motivations and drives the story forward.

CHARACTER 1
This is where the magic happens. Every great story needs conflict and resolution.

CHARACTER 2
You're right. The journey of ${prompt} teaches us about human nature and the choices we make.

The scene builds tension as the characters face their challenges, ultimately leading to a moment of truth that defines their relationship.

FADE OUT.`,
      
      dialogue: `Character 1: "I never thought ${prompt} would lead us here."

Character 2: "Sometimes the most unexpected journeys teach us the most about ourselves."

Character 1: "But what if we're not ready for what comes next?"

Character 2: "That's exactly when we need to trust in ${prompt} the most."`,
      
      summary: `This is a generated summary about ${prompt}. The content explores various aspects and implications, providing insights into the topic while maintaining narrative coherence. Key themes include character development, plot progression, and thematic resonance that connects with audiences on multiple levels.`
    };
    
    return {
      generated_text: templates[type as keyof typeof templates] || templates.summary,
      type,
      prompt,
      processing_time: "1.5s"
    };
  },

  getDataset: async (): Promise<Dataset> => {
    return {
      movies: mockMoviesData,
      dialogues: mockDialogues,
      scenes: mockScenes,
      total_movies: mockMoviesData.length,
      total_dialogues: mockDialogues.length,
      total_scenes: mockScenes.length
    };
  },

  healthCheck: async (): Promise<{ status: string; models_loaded: boolean }> => {
    return {
      status: "healthy",
      models_loaded: true
    };
  }
};
