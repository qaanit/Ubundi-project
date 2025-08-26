import { useState, useRef } from 'react';
import { TailSpin } from 'react-loader-spinner'; // Assuming you install this package

// Note: You can install the loader with:
// npm install react-loader-spinner

const App = () => {
  // State for managing the user's query input
  const [query, setQuery] = useState('');
  
  // State for the selected tone from the dropdown
  const [tone, setTone] = useState('');

  // State for the response from the backend
  const [response, setResponse] = useState('');

  // State for the sources from the backend
  const [sources, setSources] = useState([]);

  // State to handle the loading screen while waiting for the backend
  const [loading, setLoading] = useState(false);

  // State to control the visibility of the sources
  const [showSources, setShowSources] = useState(false);

  // State to handle any errors from the API call
  const [error, setError] = useState('');

  // A ref to automatically scroll to the bottom of the chat display
  const chatEndRef = useRef(null);

  const tones = ['Default', 'Friendly', 'Professional', 'Casual', 'Formal', 'Concise'];

  // Function to handle the form submission and API call
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query) return; // Prevent empty queries
    
    setLoading(true);
    setResponse('');
    setSources([]);
    setShowSources(false); // Hide sources for new query
    setError('');

    try {
      // The URL for your FastAPI backend. Adjust if it's deployed elsewhere.
      const backendUrl = 'http://127.0.0.1:8000/query';
      
      const response = await fetch(backendUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query, tone: tone || 'Default' }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Something went wrong on the server.');
      }

      const data = await response.json();
      setResponse(data.response_text);
      setSources(data.sources);
    } catch (err) {
      console.error('API Error:', err);
      setError('Failed to fetch response. Please ensure your backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100 p-4 font-inter">
      {/* Main chat interface container */}
      <div className="flex-1 overflow-y-auto p-4 rounded-xl bg-white dark:bg-gray-800 shadow-lg flex flex-col items-center">
        <h1 className="text-3xl font-bold mb-6 text-center">Your Personal RAG Agent</h1>
        
        {/* Response display area */}
        {response && (
          <div className="w-full max-w-4xl bg-gray-50 dark:bg-gray-700 p-6 rounded-xl shadow-inner mb-6 transition-opacity duration-300 opacity-100">
            <p className="text-lg leading-relaxed whitespace-pre-wrap">{response}</p>
            
            {/* Show Sources button */}
            {sources.length > 0 && (
              <div className="mt-4">
                <button
                  onClick={() => setShowSources(!showSources)}
                  className="text-blue-500 hover:text-blue-400 font-medium transition-colors"
                >
                  {showSources ? 'Hide Sources' : 'Show Sources'}
                </button>
                {/* Sources list */}
                {showSources && (
                  <ul className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                    {sources.map((source, index) => (
                      <li key={index} className="list-disc ml-5">{source}</li>
                    ))}
                  </ul>
                )}
              </div>
            )}
          </div>
        )}

        {/* Loading spinner or error message */}
        {loading && (
          <div className="flex justify-center items-center h-full">
            <TailSpin color="#3B82F6" height={50} width={50} />
          </div>
        )}

        {error && (
          <div className="text-center p-4 text-red-500 rounded-lg">
            {error}
          </div>
        )}
        
        <div ref={chatEndRef} />
      </div>

      {/* Input form at the bottom */}
      <div className="mt-4">
        <form onSubmit={handleSubmit} className="flex flex-col md:flex-row items-center gap-4 w-full">
          {/* Tone dropdown */}
          <select
            value={tone}
            onChange={(e) => setTone(e.target.value)}
            className="flex-shrink-0 w-full md:w-auto p-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-xl shadow-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
          >
            {tones.map(t => (
              <option key={t} value={t === 'Default' ? '' : t}>{t}</option>
            ))}
          </select>
          
          {/* Query input field */}
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="flex-1 w-full p-4 border border-gray-300 dark:border-gray-600 rounded-xl shadow-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
            placeholder="Ask me a question about your documents..."
            disabled={loading}
          />

          {/* Submit button */}
          <button
            type="submit"
            className="w-full md:w-auto p-4 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-xl shadow-md transition-colors disabled:bg-blue-400"
            disabled={loading}
          >
            {loading ? 'Sending...' : 'Send'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default App;
