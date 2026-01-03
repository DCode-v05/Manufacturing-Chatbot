import React from 'react';
import ChatPage from './pages/ChatPage';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="app-header">
        <div className="header-content">
          <h1>Manufacturing AI Assistant</h1>
          <p>Intelligent Factory Operations Support</p>
        </div>
      </header>

      <main className="app-main">
        <ChatPage />
      </main>

      <footer className="app-footer">
        <p>Powered by Google Gemini AI</p>
      </footer>
    </div>
  );
}

export default App;
