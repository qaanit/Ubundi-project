import { useState, useRef, useEffect } from "react";
import { TailSpin } from "react-loader-spinner";
import "./App.css"; // Import the CSS file

const App = () => {
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState("");
  const [tone, setTone] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const chatEndRef = useRef(null);

  const tones = ["Default", "Professional", "Casual","Concise"];

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query) return;

    const newUserMessage = { type: "user", text: query };
    setMessages((prev) => [...prev, newUserMessage]);
    setQuery("");
    setLoading(true);
    setError("");

    try {
      const backendUrl = "http://127.0.0.1:8000/query";
      const response = await fetch(backendUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: newUserMessage.text, tone: tone || "Default" }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Something went wrong on the server.");
      }

      const data = await response.json();
      const newAssistantMessage = {
        type: "assistant",
        text: data.response_text,
        sources: data.sources,
      };
      setMessages((prev) => [...prev, newAssistantMessage]);
    } catch (err) {
      setError("Failed to fetch response. Please ensure your backend is running.");
      setMessages((prev) => [...prev, { type: "error", text: err.message }]);
    } finally {
      setLoading(false);
    }
  };

  const Message = ({ message }) => {
    const [showSources, setShowSources] = useState(false);

    if (message.type === "user") {
      return <div className="message user">{message.text}</div>;
    }

    if (message.type === "assistant") {
      return (
        <div className="message assistant">
          <p>{message.text}</p>
          {message.sources && message.sources.length > 0 && (
            <div className="sources">
              <button onClick={() => setShowSources(!showSources)} className="source-btn">
                {showSources ? "Hide Sources" : "Show Sources"}
              </button>
              {showSources && (
                <ul>
                  {message.sources.map((src, i) => (
                    <li key={i}>{src}</li>
                  ))}
                </ul>
              )}
            </div>
          )}
        </div>
      );
    }

    if (message.type === "error") {
      return <div className="message error">Error: {message.text}</div>;
    }

    return null;
  };

  return (
    <div className="app">
      <div className="chat-container">
        <header className="chat-header">
          <h1>Qaanit-Bot</h1>
        </header>

        <div className="chat-history">
          {messages.length === 0 && (
            <div className="welcome-screen">
              <h2>Hello,</h2>
              <p>Ask a question about Qaanit to get started.</p>
            </div>
          )}

          {messages.map((msg, index) => (
            <Message key={index} message={msg} />
          ))}

          {loading && (
            <div className="loading">
              <TailSpin color="#3B82F6" height={30} width={30} />
            </div>
          )}

          {error && <div className="error-text">{error}</div>}

          <div ref={chatEndRef} />
        </div>

        <form onSubmit={handleSubmit} className="chat-input">
          <select value={tone} onChange={(e) => setTone(e.target.value)}>
            {tones.map((t) => (
              <option key={t} value={t === "Default" ? "" : t}>
                {t}
              </option>
            ))}
          </select>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder=" Ask a question..."
            disabled={loading}
          />
          <button type="submit" disabled={loading}>
            Send
          </button>
        </form>
      </div>
    </div>
  );
};

export default App;
