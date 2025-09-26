import React, { useState } from 'react';
import { searchAPI } from '../services/api.ts';
import { GenerationResponse } from '../types/index.ts';
import LoadingSpinner from '../components/LoadingSpinner.tsx';

const GeneratePage: React.FC = () => {
  const [prompt, setPrompt] = useState('');
  const [textType, setTextType] = useState<'story' | 'poem' | 'dialogue'>('story');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [generation, setGeneration] = useState<GenerationResponse | null>(null);

  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    
    setLoading(true);
    setError(null);
    try {
      const response = await searchAPI.generate(prompt, textType);
      setGeneration(response);
    } catch (err) {
      setError('Failed to generate text. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const samplePrompts = {
    story: [
      "a detective investigating a mysterious case in a futuristic city",
      "two friends discovering a hidden portal in their backyard",
      "a chef who can taste emotions in food"
    ],
    poem: [
      "the beauty of a sunset over the ocean",
      "the feeling of nostalgia on a rainy day",
      "the journey of a single leaf falling from a tree"
    ],
    dialogue: [
      "What do you think about artificial intelligence?",
      "I've been having the strangest dreams lately...",
      "Did you hear that sound coming from the basement?"
    ]
  };

  const typeDescriptions = {
    story: "Generate creative short stories and narratives",
    poem: "Create poetic verses and lyrical content", 
    dialogue: "Generate conversational exchanges between characters"
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          ✨ Creative Text Generator
        </h1>
        <p className="text-lg text-gray-600">
          Generate creative stories, poems, and dialogues using AI
        </p>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
        <div className="space-y-6">
          {/* Text Type Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Content Type
            </label>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {Object.entries(typeDescriptions).map(([type, description]) => (
                <div
                  key={type}
                  onClick={() => setTextType(type as any)}
                  className={`p-4 border-2 rounded-lg cursor-pointer transition-colors ${
                    textType === type
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="text-center">
                    <div className="text-2xl mb-2">
                      {type === 'story' ? '📚' : type === 'poem' ? '🎭' : '💬'}
                    </div>
                    <h3 className="font-medium text-gray-800 capitalize">{type}</h3>
                    <p className="text-sm text-gray-600 mt-1">{description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Prompt Input */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Creative Prompt
            </label>
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder={`Enter your ${textType} prompt...`}
              className="w-full p-4 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              rows={4}
            />
          </div>

          <div className="flex space-x-4">
            <button
              onClick={handleGenerate}
              disabled={!prompt.trim() || loading}
              className="bg-primary-600 text-white px-6 py-2 rounded-md hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              ✨ Generate {textType.charAt(0).toUpperCase() + textType.slice(1)}
            </button>
            <button
              onClick={() => setPrompt('')}
              className="bg-gray-200 text-gray-700 px-6 py-2 rounded-md hover:bg-gray-300"
            >
              🗑️ Clear
            </button>
          </div>
        </div>
      </div>

      {/* Sample Prompts */}
      <div className="bg-gray-50 rounded-lg p-6 mb-8">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">
          💡 Sample Prompts for {textType.charAt(0).toUpperCase() + textType.slice(1)}
        </h3>
        <div className="space-y-2">
          {samplePrompts[textType].map((sample, index) => (
            <div key={index} className="bg-white p-3 rounded-md border border-gray-200">
              <p className="text-gray-700 mb-2">"{sample}"</p>
              <button
                onClick={() => setPrompt(sample)}
                className="text-primary-600 hover:text-primary-700 text-sm font-medium"
              >
                Use this prompt →
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Loading */}
      {loading && <LoadingSpinner message={`Generating ${textType}...`} />}

      {/* Generation Results */}
      {generation && !loading && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex justify-between items-start mb-4">
            <h3 className="text-xl font-semibold text-gray-800">
              🎨 Generated {generation.type.charAt(0).toUpperCase() + generation.type.slice(1)}
            </h3>
            <span className="bg-primary-100 text-primary-800 text-xs px-2 py-1 rounded-full">
              {generation.type}
            </span>
          </div>
          
          <div className="space-y-4">
            <div>
              <h4 className="font-medium text-gray-800 mb-2">📝 Your Prompt</h4>
              <div className="bg-gray-50 p-3 rounded-md border-l-4 border-gray-400">
                <p className="text-gray-700 italic">"{generation.prompt}"</p>
              </div>
            </div>

            <div>
              <h4 className="font-medium text-gray-800 mb-2">✨ Generated Content</h4>
              <div className="bg-gradient-to-r from-primary-50 to-purple-50 p-4 rounded-md border-l-4 border-primary-500">
                <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">
                  {generation.generated_text}
                </p>
              </div>
            </div>
          </div>

          <div className="mt-6 flex space-x-4">
            <button
              onClick={() => navigator.clipboard.writeText(generation.generated_text)}
              className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 text-sm"
            >
              📋 Copy Text
            </button>
            <button
              onClick={() => setGeneration(null)}
              className="bg-gray-200 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-300 text-sm"
            >
              🔄 Generate New
            </button>
            <button
              onClick={() => {
                setPrompt(generation.generated_text);
                setGeneration(null);
              }}
              className="bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700 text-sm"
            >
              🔄 Continue Story
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default GeneratePage;
