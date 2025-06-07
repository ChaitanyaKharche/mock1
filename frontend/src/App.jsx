import { useState, useEffect, useRef } from 'react';
import './index.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const chatEndRef = useRef(null);

  useEffect(() => {
    // Generate a unique session ID for the user
    const id = crypto.randomUUID();
    setSessionId(id);
    setMessages([{ sender: 'assistant', text: 'Hi! I can help you find an apartment. What is your full name?' }]);
    setIsLoading(false);
  }, []);

  useEffect(() => {
    // Auto-scroll to the latest message
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || !sessionId) return;

    const userMessage = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/chat', { // Use your Render backend URL in production
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, message: input }),
      });

      if (!response.ok) throw new Error('Network response was not ok');
      
      const data = await response.json();
      const assistantMessage = { sender: 'assistant', text: data.reply };
      setMessages(prev => [...prev, assistantMessage]);

    } catch (error) {
      console.error("Fetch Error:", error);
      const errorMessage = { sender: 'assistant', text: 'Sorry, I\'m having trouble connecting. Please try again later.' };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-widget">
      <div className="chat-header">
        <h2>Homewiz Assistant</h2>
      </div>
      <div className="chat-body">
        {messages.map((msg, index) => (
          <div key={index} className={`chat-message ${msg.sender}`}>
            <p>{msg.text}</p>
          </div>
        ))}
        {isLoading && <div className="chat-message assistant"><p>...</p></div>}
        <div ref={chatEndRef} />
      </div>
      <div className="chat-input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Type your message..."
          disabled={isLoading}
        />
        <button onClick={handleSend} disabled={isLoading}>Send</button>
      </div>
    </div>
  );
}

export default App;