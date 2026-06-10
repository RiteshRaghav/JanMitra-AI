import React from 'react';

export default function ActionPlanView({ actionPlan }) {
  const steps = actionPlan.steps || [];
  const totalDays = actionPlan.estimated_completion_days || 0;

  return (
    <div className="glass-panel rounded-2xl border border-slate-800 p-6 shadow-xl">
      {/* Action Plan Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-800/80">
        <div>
          <h3 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <svg className="w-5.5 h-5.5 text-brand-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
            </svg>
            Personalized Action Plan
          </h3>
          <p className="text-sm text-slate-400 mt-1">Sequential checklist to obtain missing documents and secure benefits.</p>
        </div>

        <div className="bg-brand-amber-500/10 border border-brand-amber-500/30 rounded-xl px-4 py-2 flex flex-col items-center justify-center text-center">
          <span className="text-xs text-slate-400 font-medium uppercase tracking-wider">Estimated Time</span>
          <span className="text-lg font-bold text-brand-amber-400">{totalDays} Days</span>
        </div>
      </div>

      {/* Checklist Summary */}
      <p className="text-sm text-slate-300 mt-4 leading-relaxed bg-slate-900/30 p-3 rounded-lg border border-slate-850">
        {actionPlan.summary || "Complete the steps below to make yourself fully ready for application submissions."}
      </p>

      {/* Steps List */}
      <div className="mt-6 relative border-l-2 border-brand-teal-500/25 ml-4 pl-6 space-y-8">
        {steps.map((step, idx) => {
          const isApplyStep = step.title.toLowerCase().startsWith('apply');
          
          return (
            <div key={idx} className="relative group">
              {/* Step Timeline Indicator Node */}
              <div className={`absolute -left-[31px] top-1 w-4 h-4 rounded-full border-2 transition-all ${
                isApplyStep 
                  ? 'bg-brand-teal-500 border-brand-teal-600 scale-100 group-hover:scale-125' 
                  : 'bg-brand-amber-500 border-brand-amber-600 scale-100 group-hover:scale-125'
              }`} />
              
              {/* Card Container */}
              <div className="bg-slate-900/30 border border-slate-850 rounded-xl p-4 transition-all hover:border-slate-800">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">Step {step.step_number}</span>
                    <span className={`px-2 py-0.5 text-[10px] font-bold rounded-full ${
                      isApplyStep ? 'bg-brand-teal-500/10 text-brand-teal-400' : 'bg-brand-amber-500/10 text-brand-amber-400'
                    }`}>
                      {isApplyStep ? 'Application' : 'Document Prep'}
                    </span>
                  </div>
                  <span className="text-xs font-medium text-slate-400 flex items-center gap-1">
                    <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    {step.estimated_time}
                  </span>
                </div>

                <h4 className="text-base font-bold text-slate-200 mt-1">{step.title}</h4>
                <p className="text-sm text-slate-400 mt-1 leading-relaxed">{step.description}</p>

                {/* Sub-steps */}
                <div className="mt-3 bg-slate-950/40 p-3 rounded-lg border border-slate-900/60">
                  <h5 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Required Actions</h5>
                  <div className="space-y-2">
                    {step.actions.map((act, actIdx) => (
                      <div key={actIdx} className="flex items-start gap-2.5">
                        <input
                          type="checkbox"
                          className="w-4 h-4 rounded border-slate-800 text-brand-teal-600 bg-slate-900 focus:ring-0 focus:ring-offset-0 mt-0.5 flex-shrink-0 cursor-pointer"
                          id={`check-${idx}-${actIdx}`}
                        />
                        <label 
                          htmlFor={`check-${idx}-${actIdx}`}
                          className="text-xs text-slate-300 leading-relaxed cursor-pointer select-none"
                        >
                          {act}
                        </label>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Action Link */}
                {step.official_link && (
                  <div className="mt-3 text-right">
                    <a
                      href={step.official_link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 text-xs text-brand-teal-400 hover:text-brand-teal-300 font-semibold"
                    >
                      Visit portal to proceed
                      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </a>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
