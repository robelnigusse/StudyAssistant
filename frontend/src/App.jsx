import React, { useState, useEffect, useRef } from 'react';
import Sidebar from './components/Sidebar';
import ChatArea from './components/ChatArea';

const API_BASE_URL = 'http://127.0.0.1:8000';

function App() {
  const [conversations, setConversations] = useState([]);
  const [currentConvId, setCurrentConvId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [isUploading, setIsUploading] = useState(false);
  const messagesEndRef = useRef(null);

  const fetchConversations = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/conversations/`);
      if (res.ok) {
        const data = await res.json();
        setConversations(data);
      }
    } catch (err) {
      console.error("Failed to fetch conversations", err);
    }
  };

  useEffect(() => {
    fetchConversations();
  }, []);

  useEffect(() => {
    if (currentConvId) {
      const fetchMessages = async () => {
        try {
          const res = await fetch(`${API_BASE_URL}/conversations/${currentConvId}/messages`);
          if (res.ok) {
            const data = await res.json();
            setMessages(data);
          }
        } catch (err) {
          console.error("Failed to fetch messages", err);
        }
      };
      fetchMessages();
    } else {
      setMessages([]);
    }
  }, [currentConvId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (e) => {
    e?.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    setIsLoading(true);

    setMessages(prev => [...prev, { role: 'user', content: userMessage, id: Date.now() }]);

    try {
      const url = new URL(`${API_BASE_URL}/conversations/messages`);
      if (currentConvId) {
        url.searchParams.append('conversation_id', currentConvId);
      }

      const res = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ content: userMessage })
      });

      if (res.ok) {
        if (!currentConvId) {
          await fetchConversations();
          const convRes = await fetch(`${API_BASE_URL}/conversations/`);
          if (convRes.ok) {
            const data = await convRes.json();
            setConversations(data);
            if (data.length > 0) {
              setCurrentConvId(data[0].id);
            }
          }
        } else {
          const msgRes = await fetch(`${API_BASE_URL}/conversations/${currentConvId}/messages`);
          if (msgRes.ok) {
            setMessages(await msgRes.json());
          }
        }
      }
    } catch (err) {
      console.error("Failed to send message", err);
    } finally {
      setIsLoading(false);
    }
  };

  const deleteConversation = async (id, e) => {
    e.stopPropagation();
    if (!confirm("Are you sure you want to delete this chat?")) return;
    
    try {
      const res = await fetch(`${API_BASE_URL}/conversations/${id}`, {
        method: 'DELETE'
      });
      if (res.ok) {
        if (currentConvId === id) {
          setCurrentConvId(null);
        }
        fetchConversations();
      }
    } catch (err) {
      console.error("Failed to delete", err);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch(`${API_BASE_URL}/books/upload`, {
        method: 'POST',
        body: formData,
      });

      if (res.ok) {
        alert('Book uploaded successfully!');
      } else {
        alert('Failed to upload book.');
      }
    } catch (err) {
      console.error('Upload error:', err);
      alert('An error occurred during upload.');
    } finally {
      setIsUploading(false);
      e.target.value = null;
    }
  };

  return (
    <div className="flex h-screen bg-[#212121] text-gray-100 font-sans">
      <Sidebar 
        isSidebarOpen={isSidebarOpen} 
        setIsSidebarOpen={setIsSidebarOpen}
        conversations={conversations}
        currentConvId={currentConvId}
        setCurrentConvId={setCurrentConvId}
        deleteConversation={deleteConversation}
        handleFileUpload={handleFileUpload}
        isUploading={isUploading}
      />
      <ChatArea 
        isSidebarOpen={isSidebarOpen}
        setIsSidebarOpen={setIsSidebarOpen}
        setCurrentConvId={setCurrentConvId}
        messages={messages}
        isLoading={isLoading}
        input={input}
        setInput={setInput}
        handleSend={handleSend}
        messagesEndRef={messagesEndRef}
      />
    </div>
  );
}

export default App;