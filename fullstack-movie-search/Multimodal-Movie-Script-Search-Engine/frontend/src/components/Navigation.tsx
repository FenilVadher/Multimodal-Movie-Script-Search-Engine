import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navigation: React.FC = () => {
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <nav className="bg-white/95 backdrop-blur-sm border-b-2 border-gray-200 sticky top-0 z-50 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-20">
          <div className="flex items-center">
            <div className="flex-shrink-0 flex items-center animate-fadeIn">
              <div className="bg-gradient-to-r from-purple-500 to-pink-500 p-3 rounded-xl shadow-lg">
                <span className="text-2xl">🎬</span>
              </div>
              <div className="ml-4">
                <h1 className="text-2xl font-bold text-gray-900">
                  CineSearch AI
                </h1>
                <p className="text-sm text-gray-600 font-medium">Multimodal Movie Discovery</p>
              </div>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Link
              to="/"
              className={`group relative px-6 py-3 rounded-xl text-sm font-bold transition-all duration-300 shadow-md hover:shadow-lg ${
                isActive('/')
                  ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
                  : 'bg-gray-100 text-gray-800 hover:bg-gray-200 border-2 border-gray-300'
              }`}
            >
              <span className="flex items-center space-x-2">
                <span className="text-lg">🔍</span>
                <span>Search</span>
              </span>
            </Link>
            <Link
              to="/summarize"
              className={`group relative px-6 py-3 rounded-xl text-sm font-bold transition-all duration-300 shadow-md hover:shadow-lg ${
                isActive('/summarize')
                  ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
                  : 'bg-gray-100 text-gray-800 hover:bg-gray-200 border-2 border-gray-300'
              }`}
            >
              <span className="flex items-center space-x-2">
                <span className="text-lg">📄</span>
                <span>Summarize</span>
              </span>
            </Link>
            <Link
              to="/generate"
              className={`group relative px-6 py-3 rounded-xl text-sm font-bold transition-all duration-300 shadow-md hover:shadow-lg ${
                isActive('/generate')
                  ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
                  : 'bg-gray-100 text-gray-800 hover:bg-gray-200 border-2 border-gray-300'
              }`}
            >
              <span className="flex items-center space-x-2">
                <span className="text-lg">✨</span>
                <span>Generate</span>
              </span>
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
