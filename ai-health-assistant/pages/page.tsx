import { useState } from 'react';
import Image from 'next/image';

// Simulate an AI response (you can replace this with an actual AI service call)
const getAIResponse = (message: string) => {
  // Example response logic, replace with actual AI processing
  if (message.toLowerCase().includes('hello')) {
    return 'Hello! How can I assist you with your health concerns today?';
  }
  return "I'm not sure how to respond to that. Can you try asking something else?";
};

export default function Home() {
  const [messages, setMessages] = useState<{ sender: 'user' | 'bot'; content: string }[]>([]);
  const [userInput, setUserInput] = useState('');

  const handleSendMessage = () => {
    const trimmedInput = userInput.trim();
    if (!trimmedInput) return;

    // Add user message to chat
    setMessages([...messages, { sender: 'user', content: trimmedInput }]);

    // Get AI response and add to chat
    const aiResponse = getAIResponse(trimmedInput);
    setMessages((prevMessages) => [...prevMessages, { sender: 'bot', content: aiResponse }]);

    // Clear input field
    setUserInput('');
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
        {/* Existing content */}
      </div>

      {/* Chatbot UI */}
      <div className="absolute bottom-5 right-5 w-96 p-4 bg-white shadow-lg rounded-lg">
        <div className="h-64 overflow-auto">
          {messages.map((msg, index) => (
            <div key={index} className={`p-2 ${msg.sender === 'user' ? 'text-right' : 'text-left'}`}>
              <span className="inline-block rounded-md text-white bg-blue-500 p-2">
                {msg.content}
              </span>
            </div>
          ))}
        </div>
        <div className="flex mt-2">
          <input
            type="text"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded-l-md focus:outline-none"
            placeholder="Type your message here..."
            onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
          />
          <button
            onClick={handleSendMessage}
            className="bg-blue-500 hover:bg-blue-700 text-white p-2 rounded-r-md"
          >
            Send
          </button>
        </div>
      </div>
    </main>
  );
}
