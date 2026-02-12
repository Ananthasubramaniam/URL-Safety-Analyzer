import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import UrlPage from './pages/UrlPage';
import EmailPage from './pages/EmailPage';
import AttachmentPage from './pages/AttachmentPage';
import HistoryPage from './pages/HistoryPage';
import CommunityPage from './pages/CommunityPage';
import './App.css';
import './index.css';

function App() {
  return (
    <Router>
      <div className="app-container">
        <Navbar />
        <main className="main-content container">
          <Routes>
            <Route path="/" element={<UrlPage />} />
            <Route path="/email" element={<EmailPage />} />
            <Route path="/attachment" element={<AttachmentPage />} />
            <Route path="/history" element={<HistoryPage />} />
            <Route path="/community" element={<CommunityPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
        <footer className="footer">
          <p>© {new Date().getFullYear()} PhishGuard. All rights reserved.</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
