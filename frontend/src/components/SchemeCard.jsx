import React, { useState } from 'react';

export default function SchemeCard({ scheme, userDocuments = [] }) {
  const [isOpen, setIsOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('info'); // 'info', 'docs', 'apply', 'faqs'

  // Map badge classes
  const statusColors = {
    'Highly Eligible': 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
    'Eligible': 'bg-teal-500/10 text-brand-teal-400 border-brand-teal-500/30',
    'Potentially Eligible': 'bg-amber-500/10 text-brand-amber-400 border-brand-amber-500/30',
    'Ineligible': 'bg-rose-500/10 text-rose-400 border-rose-500/30'
  };

  const getDocStatus = (docName) => {
    // Check if doc is in user's available documents list
    const isAvailable = userDocuments.some(ud => 
      ud.toLowerCase().includes(docName.toLowerCase()) || 
      docName.toLowerCase().includes(ud.toLowerCase())
    );
    return isAvailable;
  };

  const requiredDocs = scheme.required_documents || [];
  const availableCount = requiredDocs.filter(getDocStatus).length;
  const totalCount = requiredDocs.length;
  const docReadiness = totalCount > 0 ? Math.round((availableCount / totalCount) * 100) : 100;

  return (
    <div className="glass-panel rounded-2xl border border-slate-800 p-6 transition-all hover:border-slate-700/60 shadow-xl">
      {/* Card Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <span className="text-xs font-semibold tracking-wider uppercase text-brand-teal-400">{scheme.ministry}</span>
          <h3 className="text-xl font-bold text-slate-100 mt-1">{scheme.scheme_name}</h3>
          <p className="text-sm text-slate-400 mt-0.5">Administered by: <span className="text-slate-300 font-medium">{scheme.state} Government</span></p>
        </div>
        
        <div className="flex items-center gap-3">
          <span className={`px-3 py-1 text-xs font-semibold rounded-full border ${statusColors[scheme.status]}`}>
            {scheme.status}
          </span>
          <div className="flex flex-col items-end">
            <span className="text-xs text-slate-400 font-medium">Match Score</span>
            <span className="text-lg font-bold text-brand-teal-400">{scheme.match_percentage}%</span>
          </div>
        </div>
      </div>

      {/* Why Eligible (Summary) */}
      <div className="mt-4 p-3 bg-slate-900/40 rounded-xl border border-slate-800/40">
        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
          <svg className="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Why You Qualify
        </h4>
        <ul className="mt-2 space-y-1 text-sm text-slate-300 pl-5 list-disc">
          {scheme.reasons.slice(0, 3).map((r, i) => (
            <li key={i}>{r}</li>
          ))}
        </ul>
      </div>

      {/* Tabs Menu */}
      <div className="mt-5 border-b border-slate-850 flex gap-2">
        <button
          onClick={() => setActiveTab('info')}
          className={`pb-2 px-3 text-sm font-semibold border-b-2 transition-all ${
            activeTab === 'info' ? 'border-brand-teal-500 text-brand-teal-400' : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          Benefits
        </button>
        <button
          onClick={() => setActiveTab('docs')}
          className={`pb-2 px-3 text-sm font-semibold border-b-2 transition-all ${
            activeTab === 'docs' ? 'border-brand-teal-500 text-brand-teal-400' : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          Required Documents ({availableCount}/{totalCount})
        </button>
        <button
          onClick={() => setActiveTab('apply')}
          className={`pb-2 px-3 text-sm font-semibold border-b-2 transition-all ${
            activeTab === 'apply' ? 'border-brand-teal-500 text-brand-teal-400' : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          Apply Steps
        </button>
        <button
          onClick={() => setActiveTab('faqs')}
          className={`pb-2 px-3 text-sm font-semibold border-b-2 transition-all ${
            activeTab === 'faqs' ? 'border-brand-teal-500 text-brand-teal-400' : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          FAQs
        </button>
      </div>

      {/* Tab Panels */}
      <div className="mt-4 min-h-[120px] transition-all">
        {activeTab === 'info' && (
          <div className="space-y-2">
            {scheme.benefits.map((b, i) => (
              <div key={i} className="flex gap-2.5 items-start">
                <span className="w-1.5 h-1.5 rounded-full bg-brand-teal-500 mt-2 flex-shrink-0" />
                <p className="text-sm text-slate-300">{b}</p>
              </div>
            ))}
          </div>
        )}

        {activeTab === 'docs' && (
          <div className="space-y-2">
            <div className="flex justify-between items-center text-xs text-slate-400 mb-2">
              <span>Readiness score</span>
              <span className="font-semibold text-brand-teal-400">{docReadiness}%</span>
            </div>
            <div className="w-full bg-slate-900 rounded-full h-1.5 mb-3 border border-slate-800">
              <div 
                className="bg-gradient-to-r from-brand-teal-600 to-brand-teal-400 h-1.5 rounded-full" 
                style={{ width: `${docReadiness}%` }}
              />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {requiredDocs.map((doc, i) => {
                const hasDoc = getDocStatus(doc);
                return (
                  <div key={i} className={`flex items-center gap-2 p-2 rounded-lg border text-sm ${
                    hasDoc ? 'bg-emerald-500/5 border-emerald-500/10 text-slate-200' : 'bg-rose-500/5 border-rose-500/10 text-slate-400'
                  }`}>
                    {hasDoc ? (
                      <svg className="w-4 h-4 text-emerald-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    ) : (
                      <svg className="w-4 h-4 text-rose-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    )}
                    <span className="truncate">{doc}</span>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {activeTab === 'apply' && (
          <div className="space-y-3">
            <div className="space-y-2 pl-2">
              {scheme.application_steps.map((step, i) => (
                <div key={i} className="flex gap-3 items-start">
                  <span className="flex items-center justify-center w-5 h-5 rounded-full bg-slate-800 text-xs font-semibold text-brand-teal-400 flex-shrink-0 mt-0.5 border border-slate-700">
                    {i + 1}
                  </span>
                  <p className="text-sm text-slate-300">{step}</p>
                </div>
              ))}
            </div>
            
            {scheme.official_link && (
              <div className="pt-2">
                <a
                  href={scheme.official_link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1.5 px-4 py-2 bg-brand-teal-700 hover:bg-brand-teal-600 border border-brand-teal-500/30 text-white text-xs font-semibold rounded-lg transition-all"
                >
                  Visit Official Portal
                  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                </a>
              </div>
            )}
          </div>
        )}

        {activeTab === 'faqs' && (
          <div className="space-y-3">
            {scheme.faqs && scheme.faqs.length > 0 ? (
              scheme.faqs.map((faq, i) => (
                <div key={i} className="p-3 bg-slate-900/20 rounded-xl border border-slate-800/60">
                  <h5 className="text-sm font-semibold text-slate-200">Q: {faq.question}</h5>
                  <p className="text-sm text-slate-400 mt-1 pl-4 border-l border-brand-teal-500/35">A: {faq.answer}</p>
                </div>
              ))
            ) : (
              <p className="text-sm text-slate-400 italic">No FAQs available for this scheme yet.</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
