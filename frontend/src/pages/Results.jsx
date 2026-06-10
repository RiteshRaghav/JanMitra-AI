import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import SchemeCard from '../components/SchemeCard';
import ActionPlanView from '../components/ActionPlanView';
import ThemeToggle from '../components/ThemeToggle';

export default function Results() {
  const navigate = useNavigate();
  const [results, setResults] = useState(null);
  const [activeTab, setActiveTab] = useState('schemes'); // 'schemes', 'plan'

  const token = localStorage.getItem('janmitra_token');
  const convId = localStorage.getItem('janmitra_conv_id');
  const citizenName = localStorage.getItem('janmitra_name') || 'Citizen';

  useEffect(() => {
    // Load results from cache
    const cachedResults = localStorage.getItem('janmitra_results');
    if (cachedResults) {
      setResults(JSON.parse(cachedResults));
    } else {
      // Fallback: navigate home if no results found
      navigate('/');
    }
  }, [navigate]);

  if (!results) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#0A0F1D] text-slate-400">
        <div className="flex flex-col items-center gap-3">
          <svg className="animate-spin h-8 w-8 text-brand-teal-400" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
          <span>Retrieving Welfare Profiles...</span>
        </div>
      </div>
    );
  }

  const { eligibility_results, document_analysis, action_plan, profile } = results;

  // Flatten matching schemes
  const eligibleSchemes = [
    ...(eligibility_results['Highly Eligible'] || []),
    ...(eligibility_results['Eligible'] || []),
    ...(eligibility_results['Potentially Eligible'] || [])
  ];

  const handleDownloadPDF = () => {
    if (!convId || !token) return;
    
    // Direct link to backend PDF generation endpoint
    const url = `http://127.0.0.1:8000/api/chat/report/${convId}/download`;
    
    // Fetch with authentication headers to retrieve the binary PDF
    fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    .then(response => {
      if (!response.ok) throw new Error("Failed to download PDF");
      return response.blob();
    })
    .then(blob => {
      // Create local URL for blob download
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = `JanMitra_Eligibility_Report_${citizenName.replace(/\s+/g, '_')}.pdf`;
      document.body.appendChild(link);
      link.click();
      link.remove();
    })
    .catch(err => {
      alert("Error generating PDF. Please ensure backend is running.");
      console.error(err);
    });
  };

  const handleShareWhatsApp = () => {
    const schemeNames = eligibleSchemes.map(s => s.scheme_name).join(', ');
    const text = `Hello! I checked my government scheme eligibility on JanMitra AI. I am eligible for: ${schemeNames || 'several welfare plans'}. Try it now at: http://127.0.0.1:5173/`;
    const encodedText = encodeURIComponent(text);
    window.open(`https://api.whatsapp.com/send?text=${encodedText}`, '_blank');
  };

  const handleRestart = () => {
    localStorage.removeItem('janmitra_conv_id');
    localStorage.removeItem('janmitra_results');
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-[#0A0F1D] pb-16 relative">
      {/* Decorative background grid/orb */}
      <div className="absolute top-0 left-0 w-full h-[350px] bg-gradient-to-b from-brand-teal-700/10 to-transparent pointer-events-none" />

      {/* Header */}
      <header className="max-w-7xl mx-auto px-6 py-6 flex items-center justify-between border-b border-slate-900/50 relative z-10">
        <div className="flex items-center gap-3" onClick={() => navigate('/')} style={{ cursor: 'pointer' }}>
          <span className="flex items-center justify-center w-8 h-8 rounded-lg bg-brand-teal-700 text-white font-bold">JM</span>
          <h2 className="text-base font-bold text-slate-200">JanMitra AI</h2>
        </div>

        <div className="flex items-center gap-3">
          <ThemeToggle />
          <button 
            onClick={handleRestart}
            className="text-xs font-bold text-slate-400 hover:text-slate-200 bg-slate-900 px-4 py-2 border border-slate-800 rounded-xl transition-all"
          >
            Check Again
          </button>
        </div>
      </header>

      {/* Hero Stats Panel */}
      <section className="max-w-7xl mx-auto px-6 mt-8 grid grid-cols-1 lg:grid-cols-12 gap-6 relative z-10">
        
        {/* Left Column: Welcome Banner & Score widgets */}
        <div className="lg:col-span-8 flex flex-col justify-between p-6 md:p-8 glass-panel rounded-3xl border border-slate-800 shadow-2xl">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-brand-teal-400">Citizen Welfare Dashboard</span>
            <h2 className="text-3xl font-black text-slate-100 mt-2">Namaste, {citizenName}!</h2>
            <p className="text-sm text-slate-400 mt-1 max-w-xl leading-relaxed">
              Based on your details (Family Income: Rs. {profile.income?.toLocaleString('en-IN') || 'N/A'}, Occupation: {profile.occupation || 'N/A'}), 
              we found <span className="text-brand-teal-400 font-bold">{eligibleSchemes.length} matched schemes</span> you can apply for.
            </p>
          </div>

          {/* Widgets Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-8">
            <div className="bg-slate-900/40 border border-slate-850 p-4 rounded-2xl flex items-center gap-4">
              <div className="w-12 h-12 rounded-xl bg-brand-teal-600/10 flex items-center justify-center text-brand-teal-400 text-xl font-bold border border-brand-teal-500/20">
                {eligibleSchemes.length > 0 ? '90%' : '0%'}
              </div>
              <div>
                <span className="text-xs text-slate-400 font-medium">Eligibility Match</span>
                <h4 className="text-lg font-bold text-slate-200 mt-0.5">Highly Eligible</h4>
              </div>
            </div>

            <div className="bg-slate-900/40 border border-slate-850 p-4 rounded-2xl flex items-center gap-4">
              <div className="w-12 h-12 rounded-xl bg-brand-amber-500/10 flex items-center justify-center text-brand-amber-400 text-xl font-bold border border-brand-amber-500/20">
                {document_analysis.readiness_score || 0}%
              </div>
              <div>
                <span className="text-xs text-slate-400 font-medium">Document Readiness</span>
                <h4 className="text-lg font-bold text-slate-200 mt-0.5">
                  {document_analysis.readiness_score >= 80 ? 'Highly Ready' : 'Documents Missing'}
                </h4>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Download & Share controls */}
        <div className="lg:col-span-4 flex flex-col justify-center p-6 glass-panel rounded-3xl border border-slate-800 shadow-2xl gap-4">
          <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400">Dashboard Actions</h3>
          
          <button
            onClick={handleDownloadPDF}
            className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-brand-teal-700 to-brand-teal-600 hover:from-brand-teal-600 hover:to-brand-teal-500 border border-brand-teal-500/30 text-white font-bold py-3.5 px-4 rounded-xl transition-all shadow-md shadow-brand-teal-700/10 text-sm"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Download PDF Report
          </button>

          <button
            onClick={handleShareWhatsApp}
            className="w-full flex items-center justify-center gap-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3.5 px-4 rounded-xl transition-all shadow-md shadow-emerald-700/10 text-sm"
          >
            <svg className="w-5 h-5 fill-current" viewBox="0 0 24 24">
              <path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946C.06 5.348 5.397.01 12.008.01c3.202.001 6.212 1.246 8.477 3.514 2.266 2.268 3.507 5.28 3.505 8.484-.004 6.657-5.34 11.997-11.953 11.997-2.005-.001-3.973-.502-5.733-1.455L0 24zm6.59-4.846c1.6.95 3.188 1.449 4.825 1.451 5.436 0 9.86-4.37 9.864-9.799.002-2.63-1.023-5.101-2.885-6.963C16.488 2.01 14.039.99 11.536.99c-5.447 0-9.873 4.372-9.877 9.802-.001 1.77.47 3.5 1.365 5.011L2.01 21.752l6.067-1.594zM18.822 14c-.38-.19-2.247-1.11-2.593-1.235-.347-.127-.6-.19-.85.19-.25.38-.968 1.235-1.185 1.488-.217.253-.433.282-.813.093-.38-.19-1.6-.59-3.05-1.885-1.127-1.006-1.89-2.25-2.11-2.63-.22-.38-.024-.585.167-.773.17-.17.38-.443.57-.665.19-.22.253-.38.38-.633.127-.253.063-.475-.03-.665-.095-.19-.85-2.06-1.165-2.822-.31-.747-.62-.647-.85-.658-.215-.011-.462-.011-.71-.011-.248 0-.65.093-1 .475-.35.38-1.338 1.31-1.338 3.193s1.372 3.693 1.56 3.946c.19.253 2.7 4.12 6.54 5.78 1.15.5 2.03.8 2.72 1 .97.31 1.85.27 2.55.16.78-.12 2.247-.92 2.56-1.8.312-.88.312-1.636.218-1.8-.09-.16-.34-.25-.72-.44z"/>
            </svg>
            Share on WhatsApp
          </button>
        </div>
      </section>

      {/* Tabs / Switcher */}
      <section className="max-w-7xl mx-auto px-6 mt-12 relative z-10">
        <div className="flex gap-4 border-b border-slate-900 pb-2">
          <button
            onClick={() => setActiveTab('schemes')}
            className={`pb-2 text-lg font-bold border-b-2 transition-all ${
              activeTab === 'schemes' ? 'border-brand-teal-500 text-brand-teal-400' : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            Eligible Schemes ({eligibleSchemes.length})
          </button>
          
          <button
            onClick={() => setActiveTab('plan')}
            className={`pb-2 text-lg font-bold border-b-2 transition-all ${
              activeTab === 'plan' ? 'border-brand-teal-500 text-brand-teal-400' : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            Personalized Action Plan
          </button>
        </div>

        {/* Tab Panels */}
        <div className="mt-8">
          {activeTab === 'schemes' && (
            <div className="space-y-6">
              {eligibleSchemes.length > 0 ? (
                eligibleSchemes.map((scheme, idx) => (
                  <SchemeCard 
                    key={idx} 
                    scheme={scheme} 
                    userDocuments={profile.available_documents || []} 
                  />
                ))
              ) : (
                <div className="text-center py-12 bg-slate-900/10 border border-slate-850 rounded-2xl text-slate-450 italic">
                  No eligible schemes matched. Check your profile settings.
                </div>
              )}
            </div>
          )}

          {activeTab === 'plan' && (
            <ActionPlanView actionPlan={action_plan} />
          )}
        </div>
      </section>
    </div>
  );
}
