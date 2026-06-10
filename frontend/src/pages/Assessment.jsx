import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import VoiceButton from '../components/VoiceButton';
import ThemeToggle from '../components/ThemeToggle';

export default function Assessment() {
  const navigate = useNavigate();
  const chatEndRef = useRef(null);
  
  // State
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [questionCount, setQuestionCount] = useState(1);
  const [activeQuestionText, setActiveQuestionText] = useState('');
  const [profile, setProfile] = useState({});
  const [loading, setLoading] = useState(false);

  // Local storage credentials
  const token = localStorage.getItem('janmitra_token');
  const convId = localStorage.getItem('janmitra_conv_id');
  const language = localStorage.getItem('janmitra_lang') || 'English';

  useEffect(() => {
    if (!token || !convId) {
      navigate('/');
      return;
    }
    loadChatHistory();
  }, []);

  useEffect(() => {
    // Scroll chat list to bottom on new messages
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const loadChatHistory = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/chat/history/${convId}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (response.ok) {
        const history = await response.json();
        setMessages(history);
        
        // Find the last assistant message as active question text
        const assistantMsgs = history.filter(m => m.sender === 'assistant');
        if (assistantMsgs.length > 0) {
          const lastMsg = assistantMsgs[assistantMsgs.length - 1];
          setActiveQuestionText(lastMsg.text);
          setQuestionCount(assistantMsgs.length);
        }
      }
    } catch (err) {
      console.error('Error fetching chat history:', err);
    }
  };

  const handleSendMessage = async (textToSend) => {
    if (!textToSend.trim()) return;
    setInputText('');
    setLoading(true);

    // Append user message instantly to UI
    const tempUserMsg = {
      id: `temp-user-${Date.now()}`,
      sender: 'user',
      text: textToSend,
      created_at: new Date().toISOString(),
    };
    setMessages(prev => [...prev, tempUserMsg]);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/chat/message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          conversation_id: convId,
          text: textToSend,
        }),
      });

      if (!response.ok) {
        throw new Error('Message sending failed');
      }

      const data = await response.json();
      
      // Append assistant's reply
      setMessages(prev => [...prev, data.message]);
      setQuestionCount(data.question_count);

      if (data.is_completed) {
        // Save results cache and redirect
        localStorage.setItem('janmitra_results', JSON.stringify(data.results));
        // Small delay for natural conversational ending
        setTimeout(() => {
          navigate('/results');
        }, 3000);
      } else {
        setActiveQuestionText(data.next_question);
        
        // Dynamically update profile tracker from the returned backend message stream or custom side effects
        // We will fetch history again to get standard profile state
        fetchProfileState();
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchProfileState = async () => {
    // In a real application, we would have a GET /api/chat/status endpoint.
    // For our prototype, we will decode the messages or call a simple check
    // We can infer the state fields from messages or do a quick parse.
    // To make it simple, we query the scheme matching or read the SQLite DB status.
    // Here we can decode keys based on questions answered.
    // Let's create a quick function that infers what values are answered:
    try {
      // Let's parse messages locally to populate our sidebar, keeping it instant!
      const profileExtract = {};
      const keywords = {
        name: ['name', 'naam'],
        age: ['age', 'उम्र', 'saal'],
        gender: ['gender', 'लिंग'],
        state: ['state', 'राज्य'],
        occupation: ['occupation', 'व्यवसाय', 'work'],
        income: ['income', 'पारिवारिक आय', 'salary'],
        category: ['category', 'श्रेणी', 'cast'],
      };
      
      // We will parse user answers chronologically to fill the sidebar values
      let currentField = '';
      messages.forEach(msg => {
        if (msg.sender === 'assistant') {
          const text = msg.text.toLowerCase();
          if (text.includes('name') || text.includes('नाम')) currentField = 'Name';
          else if (text.includes('age') || text.includes('उम्र')) currentField = 'Age';
          else if (text.includes('gender') || text.includes('लिंग')) currentField = 'Gender';
          else if (text.includes('state') || text.includes('राज्य')) currentField = 'State';
          else if (text.includes('occupation') || text.includes('व्यवसाय')) currentField = 'Occupation';
          else if (text.includes('income') || text.includes('आय')) currentField = 'Income';
          else if (text.includes('category') || text.includes('श्रेणी')) currentField = 'Category';
          else if (text.includes('land') || text.includes('कृषि')) currentField = 'Land';
          else if (text.includes('disability') || text.includes('विकलांग')) currentField = 'Disability';
        } else if (msg.sender === 'user' && currentField) {
          profileExtract[currentField] = msg.text;
        }
      });
      setProfile(profileExtract);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    if (messages.length > 0) {
      fetchProfileState();
    }
  }, [messages]);

  return (
    <div className="min-h-screen flex bg-[#0A0F1D] text-slate-100 font-sans">
      {/* Left Sidebar: Real-time Profile Tracker */}
      <aside className="hidden lg:flex flex-col w-80 bg-slate-950 border-r border-slate-900 p-6 space-y-6">
        <div>
          <h2 className="text-lg font-bold text-slate-200">Citizen Profile</h2>
          <p className="text-xs text-slate-400 mt-1">Real-time parameters extracted by JanMitra Agents.</p>
        </div>

        {/* Profile Attributes List */}
        <div className="flex-1 space-y-4">
          {[
            { label: 'Citizen Name', value: profile.Name || 'Identifying...' },
            { label: 'Age', value: profile.Age || 'Identifying...' },
            { label: 'Gender', value: profile.Gender || 'Identifying...' },
            { label: 'State', value: profile.State || 'Identifying...' },
            { label: 'Occupation', value: profile.Occupation || 'Identifying...' },
            { label: 'Family Income', value: profile.Income || 'Identifying...' },
            { label: 'Social Category', value: profile.Category || 'Identifying...' },
            { label: 'Owns Land', value: profile.Land || 'Identifying...' },
            { label: 'Disability Status', value: profile.Disability || 'Identifying...' },
          ].map((item, idx) => (
            <div key={idx} className="p-3 bg-slate-900/40 rounded-xl border border-slate-850 flex justify-between items-center text-sm">
              <span className="text-slate-400 font-semibold">{item.label}</span>
              <span className={`font-semibold truncate max-w-[140px] ${
                item.value.includes('Identifying') ? 'text-brand-amber-500/80 italic text-xs' : 'text-brand-teal-400'
              }`}>
                {item.value}
              </span>
            </div>
          ))}
        </div>

        <div className="pt-4 border-t border-slate-900 text-center">
          <span className="text-[10px] text-slate-500 uppercase tracking-wider font-bold">DigiLocker Integration Active</span>
        </div>
      </aside>

      {/* Main Assessment Chat Center */}
      <section className="flex-1 flex flex-col justify-between max-w-5xl mx-auto h-screen relative">
        {/* Assessment Progress Header */}
        <header className="p-4 border-b border-slate-900/50 bg-[#0A0F1D]/80 backdrop-blur-md flex items-center justify-between z-10">
          <div>
            <span className="text-[10px] font-bold text-brand-teal-400 uppercase tracking-wide">Live Assessment</span>
            <h2 className="text-sm font-bold text-slate-200">Dynamic Interview Agent</h2>
          </div>
          
          <div className="flex items-center gap-3">
            <ThemeToggle />
            <span className="text-xs text-slate-400 font-medium">Question {questionCount} of 12</span>
            <div className="w-24 bg-slate-950 rounded-full h-2 border border-slate-850">
              <div 
                className="bg-brand-teal-500 h-2 rounded-full transition-all duration-300"
                style={{ width: `${(questionCount / 12) * 100}%` }}
              />
            </div>
          </div>
        </header>

        {/* Chat Feed */}
        <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
          {messages.map((msg) => {
            const isUser = msg.sender === 'user';
            
            // Format RAG answers differently inside bubbles
            const textParts = msg.text.split('-------------------------');
            const hasRagAnswer = textParts.length > 1;
            const ragText = hasRagAnswer ? textParts[0] : '';
            const questionText = hasRagAnswer ? textParts[1] : msg.text;

            return (
              <div key={msg.id} className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-xl rounded-2xl p-4 shadow-md ${
                  isUser 
                    ? 'bg-brand-teal-700 text-white rounded-br-none' 
                    : 'bg-slate-900 border border-slate-850 text-slate-200 rounded-bl-none'
                }`}>
                  
                  {/* Render RAG block if present */}
                  {!isUser && hasRagAnswer && (
                    <div className="mb-3 p-3 bg-brand-teal-700/10 border border-brand-teal-500/20 rounded-xl text-xs text-slate-300">
                      {ragText.trim().split('\n').map((line, i) => (
                        <p key={i} className="leading-relaxed">{line}</p>
                      ))}
                    </div>
                  )}

                  <p className="text-sm leading-relaxed whitespace-pre-line font-medium">
                    {questionText.trim()}
                  </p>
                </div>
              </div>
            );
          })}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-slate-900 border border-slate-850 rounded-2xl rounded-bl-none p-4 flex items-center gap-2 text-sm text-slate-400 shadow-md">
                <svg className="animate-spin h-4 w-4 text-brand-teal-400" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Profiling response...
              </div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        {/* Chat Control Input Bar */}
        <footer className="p-4 bg-[#0A0F1D]/65 backdrop-blur-md border-t border-slate-900/50">
          <div className="max-w-3xl mx-auto flex items-center gap-3">
            {/* Native Voice Assistant integration */}
            <VoiceButton
              language={language}
              lastQuestionText={activeQuestionText}
              onSpeechDetected={(speechText) => handleSendMessage(speechText)}
            />

            {/* Plain Text Input */}
            <form 
              onSubmit={(e) => { e.preventDefault(); handleSendMessage(inputText); }}
              className="flex-1 flex bg-slate-900 border border-slate-800 focus-within:border-brand-teal-500 rounded-xl overflow-hidden transition-all shadow-inner"
            >
              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder={language === 'Hindi' ? 'अपना उत्तर टाइप करें...' : 'Type your answer here...'}
                className="flex-1 bg-transparent px-4 py-3 text-sm text-slate-100 placeholder-slate-500 focus:outline-none"
              />
              <button
                type="submit"
                disabled={!inputText.trim()}
                className="bg-brand-teal-700/30 hover:bg-brand-teal-600/50 disabled:bg-transparent text-brand-teal-400 disabled:text-slate-650 px-4 py-2 flex items-center justify-center transition-all border-l border-slate-850/50"
              >
                <svg className="w-5 h-5 transform rotate-90" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </button>
            </form>
          </div>
          <div className="text-center text-[10px] text-slate-500 mt-2">
            Ask details mid-chat (e.g. "What is PM Kisan?") to query our semantic search FAQs.
          </div>
        </footer>
      </section>
    </div>
  );
}
