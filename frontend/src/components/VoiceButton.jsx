import React, { useState, useEffect, useRef } from 'react';

export default function VoiceButton({ onSpeechDetected, language, lastQuestionText }) {
  const [isListening, setIsListening] = useState(false);
  const [isSpeakingEnabled, setIsSpeakingEnabled] = useState(true);
  const recognitionRef = useRef(null);

  // Initialize Speech Recognition
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const rec = new SpeechRecognition();
      rec.continuous = false;
      rec.interimResults = false;
      
      // Determine language code
      if (language === 'Hindi') {
        rec.lang = 'hi-IN';
      } else if (language === 'Hinglish') {
        rec.lang = 'hi-IN'; // Fallback to Indian accent / Hindi
      } else {
        rec.lang = 'en-IN';
      }

      rec.onstart = () => {
        setIsListening(true);
      };

      rec.onend = () => {
        setIsListening(false);
      };

      rec.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        if (onSpeechDetected) {
          onSpeechDetected(transcript);
        }
      };

      rec.onerror = (err) => {
        console.error('Speech recognition error:', err);
        setIsListening(false);
      };

      recognitionRef.current = rec;
    } else {
      console.warn('Web Speech Recognition API is not supported in this browser.');
    }
  }, [language, onSpeechDetected]);

  // Read question aloud whenever it changes and speaking is enabled
  useEffect(() => {
    if (isSpeakingEnabled && lastQuestionText) {
      speakText(lastQuestionText);
    }
  }, [lastQuestionText, isSpeakingEnabled]);

  const speakText = (text) => {
    if (!window.speechSynthesis) return;
    
    // Stop any ongoing speech
    window.speechSynthesis.cancel();
    
    // Clean text: strip out FAQs and other headers for speech readability
    const textToSpeak = text.split('-------------------------').pop().replace(/💡/g, '').replace(/\[.*\]/g, '').trim();

    const utterance = new SpeechSynthesisUtterance(textToSpeak);
    
    if (language === 'Hindi') {
      utterance.lang = 'hi-IN';
    } else if (language === 'Hinglish') {
      utterance.lang = 'hi-IN';
    } else {
      utterance.lang = 'en-IN';
    }
    
    // Find matching system voice if possible
    const voices = window.speechSynthesis.getVoices();
    const matchingVoice = voices.find(v => v.lang.includes(language === 'Hindi' ? 'hi' : 'en'));
    if (matchingVoice) {
      utterance.voice = matchingVoice;
    }

    window.speechSynthesis.speak(utterance);
  };

  const handleMicClick = () => {
    if (!recognitionRef.current) {
      alert("Voice recognition is not supported on this browser. Please use Chrome/Edge.");
      return;
    }

    if (isListening) {
      recognitionRef.current.stop();
    } else {
      // Cancel speech before listening
      if (window.speechSynthesis) {
        window.speechSynthesis.cancel();
      }
      recognitionRef.current.start();
    }
  };

  const toggleSpeaking = () => {
    const nextVal = !isSpeakingEnabled;
    setIsSpeakingEnabled(nextVal);
    if (!nextVal && window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
  };

  return (
    <div className="flex items-center gap-3">
      {/* Speaking/Audio Guide Toggle */}
      <button
        onClick={toggleSpeaking}
        className={`p-3 rounded-full border transition-all ${
          isSpeakingEnabled 
            ? 'bg-brand-teal-700/20 text-brand-teal-400 border-brand-teal-500/30' 
            : 'bg-slate-800 text-slate-400 border-slate-700'
        }`}
        title={isSpeakingEnabled ? "Mute Voice Prompts" : "Enable Voice Prompts"}
      >
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          {isSpeakingEnabled ? (
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
          ) : (
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15zM17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2" />
          )}
        </svg>
      </button>

      {/* Primary Listening Button */}
      <button
        onClick={handleMicClick}
        className={`relative flex items-center justify-center p-5 rounded-full transition-all ${
          isListening 
            ? 'bg-red-500 text-white pulse-mic shadow-lg shadow-red-500/50' 
            : 'bg-brand-teal-600 hover:bg-brand-teal-500 text-white shadow-lg shadow-brand-teal-500/20'
        }`}
        title={isListening ? "Listening... Click to stop" : "Talk to JanMitra (Voice Input)"}
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
        </svg>
      </button>

      {/* Visual Equalizer when Listening */}
      {isListening && (
        <div className="flex items-center gap-1 px-2 py-1 bg-slate-900/80 rounded-lg border border-red-500/30">
          <span className="wave-bar"></span>
          <span className="wave-bar"></span>
          <span className="wave-bar"></span>
          <span className="wave-bar"></span>
          <span className="wave-bar"></span>
        </div>
      )}
    </div>
  );
}
