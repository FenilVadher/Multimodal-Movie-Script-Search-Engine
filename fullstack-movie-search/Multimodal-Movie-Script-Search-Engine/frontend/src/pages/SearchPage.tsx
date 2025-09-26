import React, { useState } from 'react';
import { searchAPI } from '../services/api.ts';
import { DialogueResult, SceneResult, ContextualResult } from '../types/index.ts';
import LoadingSpinner from '../components/LoadingSpinner.tsx';
import ResultCard from '../components/ResultCard.tsx';

const SearchPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'dialogue' | 'scene' | 'contextual'>('dialogue');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Search states
  const [dialogueText, setDialogueText] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [contextDialogue, setContextDialogue] = useState('');
  const [contextFile, setContextFile] = useState<File | null>(null);
  
  // Results
  const [dialogueResults, setDialogueResults] = useState<SceneResult[]>([]);
  const [sceneResults, setSceneResults] = useState<DialogueResult[]>([]);
  const [contextualResults, setContextualResults] = useState<ContextualResult[]>([]);

  const handleDialogueSearch = async () => {
    if (!dialogueText.trim()) return;
    
    setLoading(true);
    setError(null);
    try {
      console.log('Searching for dialogue:', dialogueText);
      const response = await searchAPI.dialogueToScene(dialogueText);
      console.log('API Response:', response);
      setDialogueResults(response.results);
    } catch (err: any) {
      console.error('Search error:', err);
      const errorMessage = err.response?.data?.error || err.message || 'Failed to search for scenes. Please try again.';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleSceneSearch = async () => {
    if (!selectedFile) return;
    
    setLoading(true);
    setError(null);
    try {
      const response = await searchAPI.sceneToDialogue(selectedFile);
      setSceneResults(response.results);
    } catch (err) {
      setError('Failed to search for dialogues. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleContextualSearch = async () => {
    if (!contextDialogue.trim() || !contextFile) return;
    
    setLoading(true);
    setError(null);
    try {
      const response = await searchAPI.contextualSearch(contextDialogue, contextFile);
      setContextualResults(response.results);
    } catch (err) {
      setError('Failed to perform contextual search. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>, type: 'scene' | 'contextual') => {
    const file = e.target.files?.[0];
    if (file) {
      if (type === 'scene') {
        setSelectedFile(file);
      } else {
        setContextFile(file);
      }
    }
  };

  const tabs = [
    { id: 'dialogue', label: 'Dialogue → Scene', icon: '💬' },
    { id: 'scene', label: 'Scene → Dialogue', icon: '🖼️' },
    { id: 'contextual', label: 'Contextual Search', icon: '🎭' },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Multimodal Movie Script Search Engine
        </h1>
        <p className="text-lg text-gray-600">
          Search for movie scenes and dialogues using AI-powered multimodal search
        </p>
      </div>

      {/* Tab Navigation */}
      <div className="flex justify-center mb-8">
        <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                activeTab === tab.id
                  ? 'bg-white text-primary-600 shadow-sm'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              <span className="mr-2">{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Search Forms */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
        {activeTab === 'dialogue' && (
          <div className="space-y-4">
            <h2 className="text-xl font-semibold text-gray-800">
              💬 Find Scenes from Dialogue
            </h2>
            <textarea
              value={dialogueText}
              onChange={(e) => setDialogueText(e.target.value)}
              placeholder="Enter movie dialogue... (e.g., 'There is no spoon' or 'May the Force be with you')"
              className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              rows={4}
            />
            <button
              onClick={handleDialogueSearch}
              disabled={!dialogueText.trim() || loading}
              className="bg-primary-600 text-white px-6 py-2 rounded-md hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              🔍 Search for Scenes
            </button>
          </div>
        )}

        {activeTab === 'scene' && (
          <div className="space-y-4">
            <h2 className="text-xl font-semibold text-gray-800">
              🖼️ Find Dialogues from Scene
            </h2>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
              <input
                type="file"
                accept="image/*"
                onChange={(e) => handleFileChange(e, 'scene')}
                className="hidden"
                id="scene-upload"
              />
              <label htmlFor="scene-upload" className="cursor-pointer">
                <div className="text-gray-400 mb-2">
                  <svg className="mx-auto h-12 w-12" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                    <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </div>
                <p className="text-sm text-gray-600">
                  {selectedFile ? selectedFile.name : 'Click to upload movie scene image'}
                </p>
              </label>
            </div>
            <button
              onClick={handleSceneSearch}
              disabled={!selectedFile || loading}
              className="bg-primary-600 text-white px-6 py-2 rounded-md hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              🔍 Search for Dialogues
            </button>
          </div>
        )}

        {activeTab === 'contextual' && (
          <div className="space-y-4">
            <h2 className="text-xl font-semibold text-gray-800">
              🎭 Contextual Search (Dialogue + Scene)
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Dialogue Text
                </label>
                <textarea
                  value={contextDialogue}
                  onChange={(e) => setContextDialogue(e.target.value)}
                  placeholder="Enter dialogue..."
                  className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  rows={3}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Scene Image
                </label>
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={(e) => handleFileChange(e, 'contextual')}
                    className="hidden"
                    id="contextual-upload"
                  />
                  <label htmlFor="contextual-upload" className="cursor-pointer">
                    <p className="text-sm text-gray-600">
                      {contextFile ? contextFile.name : 'Upload scene image'}
                    </p>
                  </label>
                </div>
              </div>
            </div>
            <button
              onClick={handleContextualSearch}
              disabled={!contextDialogue.trim() || !contextFile || loading}
              className="bg-primary-600 text-white px-6 py-2 rounded-md hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              🔍 Contextual Search
            </button>
          </div>
        )}
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Loading */}
      {loading && <LoadingSpinner message="Searching..." />}

      {/* Results */}
      {!loading && (
        <div>
          {activeTab === 'dialogue' && dialogueResults.length > 0 && (
            <div>
              <h3 className="text-xl font-semibold text-gray-800 mb-4">
                🎯 Matching Scenes ({dialogueResults.length})
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {dialogueResults.map((result) => (
                  <ResultCard key={result.id} result={result} type="scene" />
                ))}
              </div>
            </div>
          )}

          {activeTab === 'scene' && sceneResults.length > 0 && (
            <div>
              <h3 className="text-xl font-semibold text-gray-800 mb-4">
                🎯 Matching Dialogues ({sceneResults.length})
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {sceneResults.map((result) => (
                  <ResultCard key={result.id} result={result} type="dialogue" />
                ))}
              </div>
            </div>
          )}

          {activeTab === 'contextual' && contextualResults.length > 0 && (
            <div>
              <h3 className="text-xl font-semibold text-gray-800 mb-4">
                🎯 Contextual Results ({contextualResults.length})
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {contextualResults.map((result, index) => (
                  <ResultCard key={index} result={result} type="contextual" />
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default SearchPage;
