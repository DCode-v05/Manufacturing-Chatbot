import React, { useState, useRef, useEffect } from 'react';
import { sendChatMessage } from '../services/api';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import './ChatPage.css';

function ChatPage() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hello! I\'m your Manufacturing AI Assistant. Ask me about machine status, orders, procedures, or safety protocols.',
      cached: false
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    
    // Add user message to chat
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      const response = await sendChatMessage(userMessage);
      
      if (response.error) {
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: `Error: ${response.message || 'An error occurred'}`,
          error: true
        }]);
      } else {
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: response.reply,
          cached: response.cached || false
        }]);
      }
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Failed to connect to the server. Please try again.',
        error: true
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const quickQuestions = [
    "What's the status of machine A3?",
    "Show me order 101 status",
    "What are the safety procedures?",
    "How do I perform machine maintenance?"
  ];

  const handleQuickQuestion = (question) => {
    setInputMessage(question);
  };

  return (
    <div className="chat-page">
      <div className="chat-container">
        <div className="chat-messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.role}`}>
              <div className="message-avatar">
                <div className={`avatar-circle ${msg.role}`}>
                  {msg.role === 'user' ? 'U' : 'AI'}
                </div>
              </div>
              <div className="message-content">
                <div className={`message-bubble ${msg.error ? 'error' : ''}`}>
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {msg.content}
                  </ReactMarkdown>
                </div>
                {msg.cached && (
                  <span className="cached-badge">Cached Response</span>
                )}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="message assistant">
              <div className="message-avatar">
                <div className="avatar-circle assistant">AI</div>
              </div>
              <div className="message-content">
                <div className="message-bubble loading">
                  <span className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="quick-questions">
          <p className="quick-label">Suggested Questions:</p>
          <div className="quick-buttons">
            {quickQuestions.map((q, i) => (
              <button 
                key={i} 
                onClick={() => handleQuickQuestion(q)}
                disabled={isLoading}
              >
                {q}
              </button>
            ))}
          </div>
        </div>

        <form className="chat-input-form" onSubmit={handleSendMessage}>
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type your message here..."
            disabled={isLoading}
            className="chat-input"
          />
          <button 
            type="submit" 
            disabled={isLoading || !inputMessage.trim()}
            className="send-button"
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default ChatPage;
