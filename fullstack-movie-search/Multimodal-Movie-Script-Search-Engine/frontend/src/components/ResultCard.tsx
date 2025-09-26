import React from 'react';
import { DialogueResult, SceneResult, ContextualResult } from '../types/index.ts';

interface ResultCardProps {
  result: DialogueResult | SceneResult | ContextualResult;
  type: 'dialogue' | 'scene' | 'contextual';
}

const ResultCard: React.FC<ResultCardProps> = ({ result, type }) => {
  const getSimilarityColor = (similarity: number) => {
    if (similarity >= 0.3) return 'text-emerald-600 bg-emerald-100 border-emerald-200';
    if (similarity >= 0.2) return 'text-amber-600 bg-amber-100 border-amber-200';
    return 'text-rose-600 bg-rose-100 border-rose-200';
  };

  const formatSimilarity = (similarity: number) => {
    return `${(similarity * 100).toFixed(1)}%`;
  };

  const getCountryFlag = (country: string) => {
    const flags: { [key: string]: string } = {
      'USA': '🇺🇸',
      'India': '🇮🇳',
      'South Korea': '🇰🇷',
      'Spain': '🇪🇸',
    };
    return flags[country] || '🌍';
  };

  const getTypeIcon = (type: string) => {
    return type === 'Web Series' ? '📺' : '🎬';
  };

  if (type === 'dialogue') {
    const dialogueResult = result as DialogueResult;
    return (
      <div className="bg-white/95 backdrop-blur-sm rounded-2xl p-6 shadow-xl border border-gray-200 hover:shadow-2xl transition-all duration-300">
        <div className="flex justify-between items-start mb-4">
          <div className="flex items-center space-x-3">
            <span className="text-2xl">{getTypeIcon(dialogueResult.type || 'Movie')}</span>
            <div>
              <h3 className="text-xl font-bold text-gray-900">{dialogueResult.movie}</h3>
              <p className="text-gray-600 text-sm font-medium">{dialogueResult.year} • {dialogueResult.language}</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-xl">{getCountryFlag(dialogueResult.country || 'USA')}</span>
            <span className={`px-3 py-1 rounded-full text-xs font-bold border-2 ${getSimilarityColor(dialogueResult.similarity)}`}>
              {formatSimilarity(dialogueResult.similarity)}
            </span>
          </div>
        </div>
        <div className="bg-blue-50 border-l-4 border-blue-400 rounded-r-xl p-4 mb-4">
          <p className="text-gray-800 text-sm italic leading-relaxed font-medium">"{dialogueResult.dialogue}"</p>
        </div>
        <div className="flex flex-wrap gap-2">
          <span className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-4 py-2 rounded-full text-sm font-bold shadow-md">
            {dialogueResult.genre}
          </span>
          <span className="bg-gray-200 text-gray-800 px-4 py-2 rounded-full text-sm font-semibold">
            {dialogueResult.type || 'Movie'}
          </span>
        </div>
      </div>
    );
  }

  if (type === 'scene') {
    const sceneResult = result as SceneResult;
    return (
      <div className="bg-white/95 backdrop-blur-sm rounded-2xl overflow-hidden shadow-xl border border-gray-200 hover:shadow-2xl transition-all duration-300">
        <div className="relative">
          <div className="flex">
            <img 
              src={sceneResult.image_url} 
              alt={sceneResult.description}
              className="w-1/2 h-48 object-cover"
            />
            <video 
              src={sceneResult.video_url}
              controls
              className="w-1/2 h-48 object-cover"
              poster={sceneResult.image_url}
            >
              Your browser does not support the video tag.
            </video>
          </div>
          <div className="absolute top-4 right-4 flex items-center space-x-2">
            <span className="text-xl bg-white/90 rounded-full p-1">{getCountryFlag(sceneResult.country || 'USA')}</span>
            <span className={`px-3 py-1 rounded-full text-xs font-bold border-2 backdrop-blur-md bg-white/90 ${getSimilarityColor(sceneResult.similarity)}`}>
              {formatSimilarity(sceneResult.similarity)}
            </span>
          </div>
          <div className="absolute bottom-4 left-4 bg-white/90 rounded-full p-2">
            <span className="text-2xl">{getTypeIcon(sceneResult.type || 'Movie')}</span>
          </div>
        </div>
        <div className="p-6">
          <div className="flex justify-between items-start mb-3">
            <div>
              <h3 className="text-xl font-bold text-gray-900">{sceneResult.movie}</h3>
              <p className="text-gray-600 text-sm font-medium">{sceneResult.year} • {sceneResult.language}</p>
            </div>
          </div>
          <p className="text-gray-800 text-sm mb-4 leading-relaxed font-medium">{sceneResult.description}</p>
          <div className="flex flex-wrap gap-2">
            <span className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-4 py-2 rounded-full text-sm font-bold shadow-md">
              {sceneResult.genre}
            </span>
            <span className="bg-gray-200 text-gray-800 px-4 py-2 rounded-full text-sm font-semibold">
              {sceneResult.type || 'Movie'}
            </span>
          </div>
        </div>
      </div>
    );
  }

  if (type === 'contextual') {
    const contextualResult = result as ContextualResult;
    
    if (contextualResult.type === 'scene') {
      const sceneContent = contextualResult.content as SceneResult;
      return (
        <div className="bg-white/95 backdrop-blur-sm rounded-2xl overflow-hidden shadow-xl border border-gray-200 hover:shadow-2xl transition-all duration-300">
          <div className="relative">
            <div className="flex">
              <img 
                src={sceneContent.image_url} 
                alt={sceneContent.description}
                className="w-1/2 h-48 object-cover"
              />
              <video 
                src={sceneContent.video_url}
                controls
                className="w-1/2 h-48 object-cover"
                poster={sceneContent.image_url}
              >
                Your browser does not support the video tag.
              </video>
            </div>
            <div className="absolute top-4 right-4 flex items-center space-x-2">
              <span className="text-xl bg-white/90 rounded-full p-1">{getCountryFlag(sceneContent.country || 'USA')}</span>
              <span className={`px-3 py-1 rounded-full text-xs font-bold border-2 backdrop-blur-md bg-white/90 ${getSimilarityColor(contextualResult.similarity)}`}>
                {formatSimilarity(contextualResult.similarity)}
              </span>
            </div>
            <div className="absolute bottom-4 left-4 bg-white/90 rounded-full p-2">
              <span className="text-2xl">{getTypeIcon(sceneContent.type || 'Movie')}</span>
            </div>
            <div className="absolute top-4 left-4 bg-blue-600 text-white px-3 py-1 rounded-full text-xs font-bold">
              SCENE
            </div>
          </div>
          <div className="p-6">
            <div className="flex justify-between items-start mb-3">
              <div>
                <h3 className="text-xl font-bold text-gray-900">{sceneContent.movie}</h3>
                <p className="text-gray-600 text-sm font-medium">{sceneContent.year} • {sceneContent.language}</p>
              </div>
            </div>
            <p className="text-gray-800 text-sm mb-4 leading-relaxed font-medium">{sceneContent.description}</p>
            <div className="flex flex-wrap gap-2">
              <span className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-4 py-2 rounded-full text-sm font-bold shadow-md">
                {sceneContent.genre}
              </span>
              <span className="bg-gray-200 text-gray-800 px-4 py-2 rounded-full text-sm font-semibold">
                {sceneContent.type || 'Movie'}
              </span>
            </div>
          </div>
        </div>
      );
    } else {
      const dialogueContent = contextualResult.content as DialogueResult;
      return (
        <div className="bg-white/95 backdrop-blur-sm rounded-2xl p-6 shadow-xl border border-gray-200 hover:shadow-2xl transition-all duration-300">
          <div className="flex justify-between items-start mb-4">
            <div className="flex items-center space-x-3">
              <span className="text-2xl">{getTypeIcon(dialogueContent.type || 'Movie')}</span>
              <div>
                <h3 className="text-xl font-bold text-gray-900">{dialogueContent.movie}</h3>
                <p className="text-gray-600 text-sm font-medium">{dialogueContent.year} • {dialogueContent.language}</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <span className="bg-green-600 text-white px-3 py-1 rounded-full text-xs font-bold">
                DIALOGUE
              </span>
              <span className="text-xl">{getCountryFlag(dialogueContent.country || 'USA')}</span>
              <span className={`px-3 py-1 rounded-full text-xs font-bold border-2 ${getSimilarityColor(contextualResult.similarity)}`}>
                {formatSimilarity(contextualResult.similarity)}
              </span>
            </div>
          </div>
          <div className="bg-blue-50 border-l-4 border-blue-400 rounded-r-xl p-4 mb-4">
            <p className="text-gray-800 text-sm italic leading-relaxed font-medium">"{dialogueContent.dialogue}"</p>
          </div>
          <div className="flex flex-wrap gap-2">
            <span className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-4 py-2 rounded-full text-sm font-bold shadow-md">
              {dialogueContent.genre}
            </span>
            <span className="bg-gray-200 text-gray-800 px-4 py-2 rounded-full text-sm font-semibold">
              {dialogueContent.type || 'Movie'}
            </span>
          </div>
        </div>
      );
    }
  }

  return null;
};

export default ResultCard;
