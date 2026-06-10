import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ThemeToggle from '../components/ThemeToggle';

export default function Admin() {
  const navigate = useNavigate();
  const [schemes, setSchemes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [pdfFile, setPdfFile] = useState(null);
  const [pdfParsing, setPdfParsing] = useState(false);

  // Form State
  const [schemeId, setSchemeId] = useState('');
  const [schemeName, setSchemeName] = useState('');
  const [ministry, setMinistry] = useState('');
  const [stateName, setStateName] = useState('Central');
  
  // Rules State
  const [occupations, setOccupations] = useState('');
  const [maxIncome, setMaxIncome] = useState('');
  const [minAge, setMinAge] = useState('');
  const [maxAge, setMaxAge] = useState('');
  const [genders, setGenders] = useState('Male, Female, Other');
  const [socialCategories, setSocialCategories] = useState('');
  const [isStudent, setIsStudent] = useState('any');
  const [isDisabled, setIsDisabled] = useState('any');

  // Lists
  const [benefits, setBenefits] = useState('');
  const [requiredDocs, setRequiredDocs] = useState('');
  const [appSteps, setAppSteps] = useState('');
  
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    loadSchemes();
  }, []);

  const loadSchemes = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/api/schemes');
      if (response.ok) {
        const data = await response.json();
        setSchemes(data);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm(`Are you sure you want to delete scheme: ${id}?`)) return;
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/schemes/admin/${id}`, {
        method: 'DELETE',
      });
      if (response.ok) {
        setSuccess('Scheme deleted successfully.');
        loadSchemes();
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handlePdfUpload = async (e) => {
    e.preventDefault();
    if (!pdfFile) return;
    
    setPdfParsing(true);
    setError('');
    setSuccess('');
    
    const formData = new FormData();
    formData.append('file', pdfFile);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/schemes/admin/upload-pdf', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('PDF parsing failed');
      
      const data = await response.json();
      const draft = data.draft_scheme;
      
      // Auto-populate form from PDF parse draft
      setSchemeId(draft.scheme_id);
      setSchemeName(draft.scheme_name);
      setMinistry(draft.ministry);
      setStateName(draft.state);
      
      setOccupations(draft.eligibility_rules.occupations.join(', '));
      setMaxIncome(draft.eligibility_rules.max_income || '');
      setMinAge(draft.eligibility_rules.min_age || '');
      setMaxAge(draft.eligibility_rules.max_age || '');
      setGenders(draft.eligibility_rules.genders ? draft.eligibility_rules.genders.join(', ') : 'Male, Female, Other');
      setIsStudent(draft.eligibility_rules.is_student === true ? 'true' : draft.eligibility_rules.is_student === false ? 'false' : 'any');
      
      setBenefits(draft.benefits.join('\n'));
      setRequiredDocs(draft.required_documents.join('\n'));
      setAppSteps(draft.application_steps.join('\n'));
      
      setSuccess('PDF parsed successfully by Document Agent! Review and click Save Scheme below.');
    } catch (err) {
      setError('Failed to parse PDF document.');
      console.error(err);
    } finally {
      setPdfParsing(false);
    }
  };

  const handleSaveScheme = async (e) => {
    e.preventDefault();
    if (!schemeId || !schemeName || !ministry) {
      setError('Please fill in Scheme ID, Name, and Ministry.');
      return;
    }

    const payload = {
      scheme_id: schemeId.trim().toLowerCase().replace(/\s+/g, '_'),
      scheme_name: schemeName.trim(),
      ministry: ministry.trim(),
      state: stateName.trim(),
      eligibility_rules: {
        occupations: occupations ? occupations.split(',').map(s => s.trim()) : [],
        max_income: maxIncome ? parseFloat(maxIncome) : null,
        landholder: occupations.toLowerCase().includes('farmer') ? true : null,
        min_age: minAge ? parseInt(minAge) : 0,
        max_age: maxAge ? parseInt(maxAge) : 120,
        genders: genders ? genders.split(',').map(s => s.trim()) : ['Male', 'Female', 'Other'],
        states: stateName !== 'Central' ? [stateName] : [],
        social_categories: socialCategories ? socialCategories.split(',').map(s => s.trim()) : [],
        is_student: isStudent === 'true' ? true : isStudent === 'false' ? false : null,
        is_disabled: isDisabled === 'true' ? true : isDisabled === 'false' ? false : null,
      },
      benefits: benefits ? benefits.split('\n').map(s => s.trim()).filter(Boolean) : [],
      required_documents: requiredDocs ? requiredDocs.split('\n').map(s => s.trim()).filter(Boolean) : [],
      application_steps: appSteps ? appSteps.split('\n').map(s => s.trim()).filter(Boolean) : [],
      official_link: 'https://services.india.gov.in/',
      faqs: [
        {
          question: `Who can apply for ${schemeName}?`,
          answer: `Eligible citizens can apply through the official ${ministry} channels.`
        }
      ]
    };

    try {
      const response = await fetch('http://127.0.0.1:8000/api/schemes/admin/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error('Save failed');
      }

      setSuccess('New welfare scheme registered successfully.');
      loadSchemes();
      
      // Reset form
      setSchemeId('');
      setSchemeName('');
      setMinistry('');
      setOccupations('');
      setMaxIncome('');
      setMinAge('');
      setMaxAge('');
      setBenefits('');
      setRequiredDocs('');
      setAppSteps('');
    } catch (err) {
      setError('Scheme registration failed. Make sure Scheme ID is unique.');
      console.error(err);
    }
  };

  return (
    <div className="min-h-screen bg-[#0A0F1D] text-slate-100 pb-16">
      {/* Header */}
      <header className="max-w-7xl mx-auto px-6 py-6 flex items-center justify-between border-b border-slate-900/50">
        <div className="flex items-center gap-3" onClick={() => navigate('/')} style={{ cursor: 'pointer' }}>
          <span className="flex items-center justify-center w-8 h-8 rounded-lg bg-brand-teal-700 text-white font-bold">JM</span>
          <h2 className="text-base font-bold text-slate-200">JanMitra AI Admin</h2>
        </div>
        <div className="flex items-center gap-3">
          <ThemeToggle />
          <button 
            onClick={() => navigate('/')} 
            className="text-xs font-semibold text-slate-400 hover:text-slate-200"
          >
            Exit Console
          </button>
        </div>
      </header>

      {/* Analytics widgets */}
      <main className="max-w-7xl mx-auto px-6 mt-8 space-y-12">
        <section className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          <div className="p-6 bg-slate-900/40 border border-slate-850 rounded-2xl">
            <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Total Schemes Active</span>
            <h3 className="text-3xl font-bold text-brand-teal-400 mt-2">{schemes.length}</h3>
          </div>
          <div className="p-6 bg-slate-900/40 border border-slate-850 rounded-2xl">
            <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Indexed FAQ Docs</span>
            <h3 className="text-3xl font-bold text-brand-teal-400 mt-2">{schemes.reduce((acc, s) => acc + (s.faqs?.length || 0), 0)}</h3>
          </div>
          <div className="p-6 bg-slate-900/40 border border-slate-850 rounded-2xl">
            <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Agent Parser Status</span>
            <h3 className="text-3xl font-bold text-emerald-400 mt-2">Active</h3>
          </div>
        </section>

        {/* Dashboard split content */}
        <section className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* Left panel: Add Scheme form & PDF parser */}
          <div className="lg:col-span-7 space-y-6">
            
            {/* PDF Uploader */}
            <div className="glass-panel rounded-2xl border border-slate-800 p-6">
              <h3 className="text-lg font-bold text-slate-200">Ingest Policy Guidelines (PDF)</h3>
              <p className="text-xs text-slate-400 mt-1">Upload a government welfare guidelines circular. Our document agent will parse rules, benefits, and checklists automatically.</p>
              
              <form onSubmit={handlePdfUpload} className="mt-4 flex flex-col sm:flex-row gap-3">
                <input
                  type="file"
                  accept=".pdf"
                  onChange={(e) => setPdfFile(e.target.files[0])}
                  className="flex-1 bg-slate-950/60 border border-slate-850 rounded-xl px-4 py-2 text-xs text-slate-400 focus:outline-none cursor-pointer"
                />
                <button
                  type="submit"
                  disabled={pdfParsing || !pdfFile}
                  className="bg-brand-teal-700 hover:bg-brand-teal-600 disabled:bg-slate-800 text-white font-bold px-5 py-2.5 rounded-xl transition-all text-xs flex items-center justify-center gap-2"
                >
                  {pdfParsing ? 'Analyzing circular...' : 'Ingest PDF'}
                </button>
              </form>
            </div>

            {/* Scheme builder Form */}
            <div className="glass-panel rounded-2xl border border-slate-800 p-6">
              <h3 className="text-lg font-bold text-slate-200">Register Welfare Scheme</h3>
              <p className="text-xs text-slate-400 mt-1">Configure eligibility rules and parameters for citizen-matching logic.</p>

              <form onSubmit={handleSaveScheme} className="mt-6 space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block mb-1">Scheme ID</label>
                    <input
                      type="text"
                      value={schemeId}
                      onChange={(e) => setSchemeId(e.target.value)}
                      placeholder="e.g. pm_kisan"
                      className="w-full bg-slate-950/60 border border-slate-850 rounded-xl px-3 py-2 text-xs text-slate-250 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block mb-1">Scheme Name</label>
                    <input
                      type="text"
                      value={schemeName}
                      onChange={(e) => setSchemeName(e.target.value)}
                      placeholder="e.g. PM Kisan Samman"
                      className="w-full bg-slate-950/60 border border-slate-850 rounded-xl px-3 py-2 text-xs text-slate-250 focus:outline-none"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block mb-1">Ministry</label>
                    <input
                      type="text"
                      value={ministry}
                      onChange={(e) => setMinistry(e.target.value)}
                      placeholder="e.g. Ministry of Agriculture"
                      className="w-full bg-slate-950/60 border border-slate-850 rounded-xl px-3 py-2 text-xs text-slate-250 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block mb-1">State / Scope</label>
                    <input
                      type="text"
                      value={stateName}
                      onChange={(e) => setStateName(e.target.value)}
                      placeholder="Central or State Name"
                      className="w-full bg-slate-950/60 border border-slate-850 rounded-xl px-3 py-2 text-xs text-slate-250 focus:outline-none"
                    />
                  </div>
                </div>

                {/* Eligibility parameters */}
                <div className="border-t border-slate-900 pt-4">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-brand-teal-400">Eligibility Rules Engine</h4>
                  <div className="grid grid-cols-2 gap-4 mt-3">
                    <div>
                      <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block mb-1">Allowed Occupations (comma sep)</label>
                      <input
                        type="text"
                        value={occupations}
                        onChange={(e) => setOccupations(e.target.value)}
                        placeholder="Farmer, Student, etc."
                        className="w-full bg-slate-950/60 border border-slate-850 rounded-xl px-3 py-2 text-xs text-slate-250"
                      />
                    </div>
                    <div>
                      <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block mb-1">Max Annual Income (Rs.)</label>
                      <input
                        type="number"
                        value={maxIncome}
                        onChange={(e) => setMaxIncome(e.target.value)}
                        placeholder="e.g. 250000"
                        className="w-full bg-slate-950/60 border border-slate-850 rounded-xl px-3 py-2 text-xs text-slate-250"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4 mt-3">
                    <div>
                      <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block mb-1">Min Age</label>
                      <input
                        type="number"
                        value={minAge}
                        onChange={(e) => setMinAge(e.target.value)}
                        placeholder="18"
                        className="w-full bg-slate-950/60 border border-slate-850 rounded-xl px-3 py-2 text-xs text-slate-250"
                      />
                    </div>
                    <div>
                      <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block mb-1">Max Age</label>
                      <input
                        type="number"
                        value={maxAge}
                        onChange={(e) => setMaxAge(e.target.value)}
                        placeholder="60"
                        className="w-full bg-slate-950/60 border border-slate-850 rounded-xl px-3 py-2 text-xs text-slate-250"
                      />
                    </div>
                  </div>
                </div>

                {/* Lists textareas */}
                <div className="border-t border-slate-900 pt-4 space-y-3">
                  <div>
                    <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block mb-1">Benefits (one per line)</label>
                    <textarea
                      value={benefits}
                      onChange={(e) => setBenefits(e.target.value)}
                      placeholder="Stipend of ₹2000 per month..."
                      rows={2}
                      className="w-full bg-slate-950/60 border border-slate-850 rounded-xl px-3 py-2 text-xs text-slate-250 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block mb-1">Required Documents (one per line)</label>
                    <textarea
                      value={requiredDocs}
                      onChange={(e) => setRequiredDocs(e.target.value)}
                      placeholder="Aadhaar Card&#10;Income Certificate"
                      rows={2}
                      className="w-full bg-slate-950/60 border border-slate-850 rounded-xl px-3 py-2 text-xs text-slate-250 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block mb-1">Application Steps (one per line)</label>
                    <textarea
                      value={appSteps}
                      onChange={(e) => setAppSteps(e.target.value)}
                      placeholder="Register on the portal...&#10;Upload verified certificates..."
                      rows={2}
                      className="w-full bg-slate-950/60 border border-slate-850 rounded-xl px-3 py-2 text-xs text-slate-250 focus:outline-none"
                    />
                  </div>
                </div>

                {error && (
                  <div className="p-3 bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs font-semibold rounded-xl">{error}</div>
                )}
                {success && (
                  <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold rounded-xl">{success}</div>
                )}

                <button
                  type="submit"
                  className="w-full bg-brand-teal-600 hover:bg-brand-teal-500 text-white font-bold py-3 px-4 rounded-xl transition-all shadow-md shadow-brand-teal-500/20 text-xs uppercase tracking-wider"
                >
                  Save Scheme Rules
                </button>
              </form>
            </div>
          </div>

          {/* Right panel: Active schemes table */}
          <div className="lg:col-span-5 w-full">
            <div className="glass-panel rounded-2xl border border-slate-800 p-6">
              <h3 className="text-lg font-bold text-slate-200">Active Schemes Database</h3>
              <p className="text-xs text-slate-400 mt-1">Review active policies matched during eligibility interviews.</p>
              
              <div className="mt-6 space-y-4 max-h-[600px] overflow-y-auto pr-1">
                {schemes.map((s) => (
                  <div key={s.scheme_id} className="p-3 bg-slate-900/40 border border-slate-850 rounded-xl flex items-center justify-between gap-4">
                    <div className="truncate">
                      <h4 className="text-sm font-bold text-slate-250 truncate">{s.scheme_name}</h4>
                      <p className="text-[10px] text-brand-teal-400 mt-0.5">{s.ministry} ({s.state})</p>
                    </div>
                    <button
                      onClick={() => handleDelete(s.scheme_id)}
                      className="text-xs font-bold text-rose-400 hover:text-rose-350 p-2 hover:bg-rose-500/5 rounded-lg border border-slate-850 hover:border-rose-500/10 transition-all flex-shrink-0"
                    >
                      Delete
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
