import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ThemeToggle from '../components/ThemeToggle';

export default function Landing() {
  const navigate = useNavigate();
  const [phone, setPhone] = useState('');
  const [fullName, setFullName] = useState('');
  const [language, setLanguage] = useState('English');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const languages = ['English', 'Hindi', 'Hinglish'];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!phone || phone.length < 10) {
      setError('Please enter a valid 10-digit mobile number.');
      return;
    }
    setError('');
    setLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          phone: phone,
          full_name: fullName || 'Citizen',
          preferred_language: language,
        }),
      });

      if (!response.ok) {
        throw new Error('Registration failed');
      }

      const data = await response.json();
      
      // Save details to localStorage
      localStorage.setItem('janmitra_token', data.access_token);
      localStorage.setItem('janmitra_user_id', data.user_id);
      localStorage.setItem('janmitra_name', data.full_name || 'Citizen');
      localStorage.setItem('janmitra_lang', data.preferred_language);

      // Start a new chat session immediately
      const chatResponse = await fetch('http://127.0.0.1:8000/api/chat/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${data.access_token}`,
        },
        body: JSON.stringify({
          preferred_language: language,
        }),
      });

      if (!chatResponse.ok) {
        throw new Error('Failed to start chat session');
      }

      const chatData = await chatResponse.json();
      localStorage.setItem('janmitra_conv_id', chatData.conversation_id);

      // Navigate to the assessment page
      navigate('/assessment');
    } catch (err) {
      setError('Failed to connect to JanMitra server. Make sure the backend is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-between bg-[#0A0F1D] relative overflow-hidden">
      {/* Decorative Blur Orbs */}
      <div className="absolute top-[-10%] right-[-10%] w-[50vw] h-[50vw] rounded-full bg-brand-teal-700/10 blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] left-[-10%] w-[50vw] h-[50vw] rounded-full bg-brand-amber-500/5 blur-[120px] pointer-events-none" />

      {/* Top Navbar */}
      <header className="w-full max-w-7xl mx-auto px-6 py-4 flex items-center justify-between border-b border-slate-900/50 z-10">
        <div className="flex items-center gap-3">
          <span className="flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-teal-700 to-brand-teal-500 text-white font-bold text-lg shadow-lg shadow-brand-teal-500/20">
            JM
          </span>
          <div>
            <h1 className="text-lg font-bold text-slate-100 leading-none">JanMitra AI</h1>
            <span className="text-[10px] text-brand-teal-400 font-semibold tracking-wide uppercase">Gov Schemes Helper</span>
          </div>
        </div>
        
        {/* Quick Admin Navigation & Theme Toggle */}
        <div className="flex items-center gap-3">
          <ThemeToggle />
          <button 
            onClick={() => navigate('/admin')}
            className="text-xs font-semibold text-slate-400 hover:text-slate-200 border border-slate-800 hover:border-slate-700 px-3 py-1.5 rounded-lg transition-all"
          >
            Admin Console
          </button>
        </div>
      </header>

      {/* Main Hero Container */}
      <main className="flex-1 max-w-7xl mx-auto px-6 grid grid-cols-1 lg:grid-cols-12 items-center gap-12 py-12 z-10 w-full">
        {/* Left Column: Vision & Features */}
        <div className="lg:col-span-7 space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-teal-500/10 border border-brand-teal-500/25 text-xs text-brand-teal-400 font-semibold">
            <span className="w-2 h-2 rounded-full bg-brand-teal-400 animate-pulse" />
            Empowering Citizens Across Bharat
          </div>

          <h2 className="text-4xl md:text-5xl font-black text-slate-100 tracking-tight leading-none">
            Find Government Schemes You Are <span className="text-brand-teal-400">Eligible</span> For in Minutes
          </h2>
          
          <p className="text-base text-slate-400 leading-relaxed max-w-xl">
            JanMitra AI uses advanced Agentic AI + RAG to match you with central and state government benefits. 
            Speak or type naturally in Hindi, English, or Hinglish.
          </p>

          {/* Quick Feature Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4 max-w-lg">
            <div className="flex gap-3 items-start p-3 bg-slate-900/35 border border-slate-850 rounded-xl">
              <div className="p-2 rounded-lg bg-brand-teal-600/10 text-brand-teal-400 mt-0.5">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                </svg>
              </div>
              <div>
                <h4 className="text-sm font-semibold text-slate-200">Voice-First Experience</h4>
                <p className="text-xs text-slate-400 mt-0.5">Speaks questions aloud. Tap and speak your answers.</p>
              </div>
            </div>

            <div className="flex gap-3 items-start p-3 bg-slate-900/35 border border-slate-850 rounded-xl">
              <div className="p-2 rounded-lg bg-brand-teal-600/10 text-brand-teal-400 mt-0.5">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <div>
                <h4 className="text-sm font-semibold text-slate-200">Personalized Roadmap</h4>
                <p className="text-xs text-slate-400 mt-0.5">Custom action plans to secure missing documents.</p>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Dynamic Form Panel */}
        <div className="lg:col-span-5 w-full">
          <div className="glass-panel border border-slate-800 rounded-3xl p-6 md:p-8 shadow-2xl relative">
            <div className="absolute top-3 right-3 flex items-center gap-1.5 px-2.5 py-1 bg-brand-teal-700/10 border border-brand-teal-500/20 rounded-full">
              <span className="w-1.5 h-1.5 rounded-full bg-brand-teal-400" />
              <span className="text-[10px] font-bold text-brand-teal-400 uppercase">Interactive Check</span>
            </div>

            <h3 className="text-2xl font-bold text-slate-100">Get Started</h3>
            <p className="text-xs text-slate-400 mt-1">Enter your details to initiate the dynamic scheme eligibility check.</p>

            <form onSubmit={handleSubmit} className="mt-6 space-y-4">
              {/* Language Selector */}
              <div>
                <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-2">Preferred Language</label>
                <div className="grid grid-cols-3 gap-2">
                  {languages.map((lang) => (
                    <button
                      key={lang}
                      type="button"
                      onClick={() => setLanguage(lang)}
                      className={`py-2 px-3 rounded-xl border text-sm font-semibold transition-all ${
                        language === lang
                          ? 'bg-brand-teal-700 text-white border-brand-teal-500 shadow-md shadow-brand-teal-500/10'
                          : 'bg-slate-900/40 text-slate-300 border-slate-800 hover:border-slate-700'
                      }`}
                    >
                      {lang}
                    </button>
                  ))}
                </div>
              </div>

              {/* Full Name */}
              <div>
                <label htmlFor="name" className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-2">Full Name</label>
                <input
                  type="text"
                  id="name"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="e.g. Ramesh Kumar"
                  className="w-full bg-slate-950/60 border border-slate-800 rounded-xl px-4 py-3 text-slate-100 placeholder-slate-500 focus:outline-none focus:border-brand-teal-500 text-sm transition-all"
                />
              </div>

              {/* Mobile Number */}
              <div>
                <label htmlFor="phone" className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-2">Mobile Number (with OTP simulation)</label>
                <div className="relative">
                  <span className="absolute left-4 top-3 text-slate-500 text-sm font-semibold">+91</span>
                  <input
                    type="tel"
                    id="phone"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value.replace(/\D/g, '').slice(0, 10))}
                    placeholder="9999999999"
                    maxLength={10}
                    className="w-full bg-slate-950/60 border border-slate-800 rounded-xl pl-14 pr-4 py-3 text-slate-100 placeholder-slate-500 focus:outline-none focus:border-brand-teal-500 text-sm font-semibold tracking-wider transition-all"
                  />
                </div>
              </div>

              {error && (
                <div className="p-3 bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs font-medium rounded-xl">
                  {error}
                </div>
              )}

              {/* Submit CTA */}
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-brand-teal-600 hover:bg-brand-teal-500 disabled:bg-brand-teal-700/50 text-white font-bold py-3.5 px-4 rounded-xl transition-all shadow-lg shadow-brand-teal-500/25 flex items-center justify-center gap-2 text-sm mt-6"
              >
                {loading ? (
                  <>
                    <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                    Contacting Welfare Agents...
                  </>
                ) : (
                  <>
                    Start Eligibility Check
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                    </svg>
                  </>
                )}
              </button>
            </form>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="w-full text-center py-6 border-t border-slate-900/40 z-10 text-xs text-slate-500">
        © {new Date().getFullYear()} JanMitra AI. Government Welfare Scheme Discovery Portal. Supported under National Digital Health & Farming Missions.
      </footer>
    </div>
  );
}
