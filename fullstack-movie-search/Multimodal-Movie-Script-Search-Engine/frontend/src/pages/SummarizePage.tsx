import React, { useState } from 'react';
import { searchAPI } from '../services/api.ts';
import { SummaryResponse } from '../types/index.ts';
import LoadingSpinner from '../components/LoadingSpinner.tsx';

const SummarizePage: React.FC = () => {
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [summary, setSummary] = useState<SummaryResponse | null>(null);

  const handleSummarize = async () => {
    if (!inputText.trim()) return;
    
    setLoading(true);
    setError(null);
    try {
      const response = await searchAPI.summarize(inputText);
      setSummary(response);
    } catch (err) {
      setError('Failed to generate summary. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const sampleTexts = [
    {
      title: "Matrix Script Sample",
      text: "Neo is a computer programmer by day and a hacker by night. He is contacted by the mysterious Morpheus who reveals that the world Neo knows is actually a computer simulation called the Matrix. Neo must choose between the red pill and the blue pill - between the truth and blissful ignorance. He chooses the red pill and awakens to the real world, where machines have enslaved humanity and use human bodies as an energy source. Neo discovers he may be 'The One' prophesied to free humanity from the Matrix."
    },
    {
      title: "Star Wars Script Sample", 
      text: "Luke Skywalker, a young farm boy on the desert planet Tatooine, dreams of adventure beyond his mundane life. When he encounters two droids carrying a message from Princess Leia, he becomes entangled in a galactic civil war. Obi-Wan Kenobi reveals that Luke's father was a Jedi Knight who was betrayed and murdered by his former pupil, Darth Vader. Luke begins training in the ways of the Force and joins the Rebel Alliance in their fight against the evil Galactic Empire."
    }
  ];

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          📝 Script Summarizer
        </h1>
        <p className="text-lg text-gray-600">
          Get AI-powered summaries of movie scripts and dialogues
        </p>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Script or Dialogue Text
            </label>
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Paste your movie script, dialogue, or scene description here..."
              className="w-full p-4 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              rows={8}
            />
            <p className="text-sm text-gray-500 mt-1">
              {inputText.length} characters • {inputText.split(' ').length} words
            </p>
          </div>

          <div className="flex space-x-4">
            <button
              onClick={handleSummarize}
              disabled={!inputText.trim() || loading}
              className="bg-primary-600 text-white px-6 py-2 rounded-md hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              ✨ Generate Summary
            </button>
            <button
              onClick={() => setInputText('')}
              className="bg-gray-200 text-gray-700 px-6 py-2 rounded-md hover:bg-gray-300"
            >
              🗑️ Clear
            </button>
          </div>
        </div>
      </div>

      {/* Sample Texts */}
      <div className="bg-gray-50 rounded-lg p-6 mb-8">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">
          📚 Try Sample Texts
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {sampleTexts.map((sample, index) => (
            <div key={index} className="bg-white p-4 rounded-md border border-gray-200">
              <h4 className="font-medium text-gray-800 mb-2">{sample.title}</h4>
              <p className="text-sm text-gray-600 mb-3 line-clamp-3">
                {sample.text.substring(0, 150)}...
              </p>
              <button
                onClick={() => setInputText(sample.text)}
                className="text-primary-600 hover:text-primary-700 text-sm font-medium"
              >
                Use this sample →
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
      {loading && <LoadingSpinner message="Generating summary..." />}

      {/* Summary Results */}
      {summary && !loading && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">
            📋 Summary Results
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-blue-50 p-4 rounded-md">
              <p className="text-sm text-blue-600 font-medium">Original Length</p>
              <p className="text-2xl font-bold text-blue-800">{summary.original_length}</p>
              <p className="text-xs text-blue-600">words</p>
            </div>
            <div className="bg-green-50 p-4 rounded-md">
              <p className="text-sm text-green-600 font-medium">Summary Length</p>
              <p className="text-2xl font-bold text-green-800">{summary.summary_length}</p>
              <p className="text-xs text-green-600">words</p>
            </div>
            <div className="bg-purple-50 p-4 rounded-md">
              <p className="text-sm text-purple-600 font-medium">Compression</p>
              <p className="text-2xl font-bold text-purple-800">
                {((1 - summary.summary_length / summary.original_length) * 100).toFixed(1)}%
              </p>
              <p className="text-xs text-purple-600">reduction</p>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <h4 className="font-medium text-gray-800 mb-2">📝 Generated Summary</h4>
              <div className="bg-gray-50 p-4 rounded-md border-l-4 border-primary-500">
                <p className="text-gray-700 leading-relaxed">{summary.summary}</p>
              </div>
            </div>

            <div>
              <h4 className="font-medium text-gray-800 mb-2">📄 Original Text</h4>
              <div className="bg-gray-50 p-4 rounded-md max-h-40 overflow-y-auto">
                <p className="text-gray-600 text-sm">{summary.original_text}</p>
              </div>
            </div>
          </div>

          <div className="mt-6 flex space-x-4">
            <button
              onClick={() => navigator.clipboard.writeText(summary.summary)}
              className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 text-sm"
            >
              📋 Copy Summary
            </button>
            <button
              onClick={() => setSummary(null)}
              className="bg-gray-200 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-300 text-sm"
            >
              🔄 New Summary
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default SummarizePage;
