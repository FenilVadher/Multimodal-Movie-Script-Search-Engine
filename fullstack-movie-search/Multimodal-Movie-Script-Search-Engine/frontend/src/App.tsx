import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation.tsx';
import SearchPage from './pages/SearchPage.tsx';
import SummarizePage from './pages/SummarizePage.tsx';
import GeneratePage from './pages/GeneratePage.tsx';
import './index.css';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navigation />
        <main>
          <Routes>
            <Route path="/" element={<SearchPage />} />
            <Route path="/summarize" element={<SummarizePage />} />
            <Route path="/generate" element={<GeneratePage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
