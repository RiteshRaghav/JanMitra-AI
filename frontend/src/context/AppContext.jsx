import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';

const AppContext = createContext(null);

export function AppProvider({ children }) {
  // ── Theme ──────────────────────────────────────────────────────────────────
  const [theme, setThemeState] = useState(() => {
    return localStorage.getItem('janmitra_theme') || 'dark';
  });

  const setTheme = useCallback((newTheme) => {
    setThemeState(newTheme);
    localStorage.setItem('janmitra_theme', newTheme);
    if (newTheme === 'light') {
      document.documentElement.classList.add('light');
      document.body.classList.add('light');
    } else {
      document.documentElement.classList.remove('light');
      document.body.classList.remove('light');
    }
  }, []);

  // Apply persisted theme on mount
  useEffect(() => {
    setTheme(theme);
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // ── Language ───────────────────────────────────────────────────────────────
  const [language, setLanguageState] = useState(() => {
    return localStorage.getItem('janmitra_lang') || 'English';
  });

  const setLanguage = useCallback((newLang) => {
    setLanguageState(newLang);
    localStorage.setItem('janmitra_lang', newLang);
  }, []);

  const toggleTheme = useCallback(() => {
    setTheme(theme === 'light' ? 'dark' : 'light');
  }, [theme, setTheme]);

  return (
    <AppContext.Provider value={{ theme, setTheme, toggleTheme, language, setLanguage }}>
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error('useApp must be used inside AppProvider');
  return ctx;
}
