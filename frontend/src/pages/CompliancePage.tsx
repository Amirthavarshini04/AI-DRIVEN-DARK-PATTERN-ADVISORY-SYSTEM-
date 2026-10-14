import React, { useEffect, useState } from 'react';
import { BookOpen, Search, ExternalLink, ShieldCheck, CheckCircle2, AlertTriangle, Scale, Radio } from 'lucide-react';
import { getCCPAData } from '../services/api';
import { CCPAData } from '../types';
import { Skeleton } from '../components/common/Skeleton';

export const CompliancePage: React.FC = () => {
  const [guidelines, setGuidelines] = useState<CCPAData[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getCCPAData()
      .then(res => {
        setGuidelines(res);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  const filtered = guidelines.filter(g => 
    g.category_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    g.plain_explanation.toLowerCase().includes(searchTerm.toLowerCase()) ||
    g.clause_reference.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 sm:space-y-8 max-w-7xl mx-auto w-full">
      {/* Banner */}
      <div className="cyber-glass-card p-5 sm:p-7 rounded-2xl border border-cyber-cyan/30 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <Radio className="w-4 h-4 text-cyber-cyan animate-pulse" />
            <span className="text-[11px] font-bold uppercase tracking-wider text-cyber-cyan">Legal Reference Codex</span>
            <span className="text-slate-600">•</span>
            <span className="text-xs font-mono text-slate-300">Gazette Notification 2023</span>
          </div>
          <h2 className="text-xl sm:text-2xl font-extrabold text-white tracking-tight mt-1">
            CCPA Guidelines for Prevention of Dark Patterns, 2023
          </h2>
          <p className="text-xs text-slate-300 mt-1 max-w-2xl leading-relaxed">
            Notified by the Central Consumer Protection Authority under Section 18 of the Consumer Protection Act, 2019.
          </p>
        </div>

        <a
          href="https://consumeraffairs.nic.in/sites/default/files/Dark_Patterns_Guidelines_2023.pdf"
          target="_blank"
          rel="noreferrer"
          className="px-4 py-2 bg-obsidian-900/90 hover:bg-slate-800 text-cyber-cyan text-xs font-bold rounded-xl border border-cyber-cyan/40 flex items-center space-x-2 shadow-glow-cyan transition-all cursor-pointer shrink-0"
        >
          <span>Official Gazette PDF</span>
          <ExternalLink className="w-3.5 h-3.5" />
        </a>
      </div>

      {/* Search Input Bar */}
      <div className="relative">
        <Search className="w-4 h-4 text-cyber-cyan absolute left-4 top-3.5" />
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Search guideline clauses (e.g. False Urgency, Drip Pricing, Clause 5(c), Sneaking...)"
          className="w-full pl-11 pr-4 py-3 bg-obsidian-900/80 text-white text-xs border border-slate-700/80 rounded-xl focus:border-cyber-cyan focus:outline-none transition-colors"
        />
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Skeleton className="h-64 rounded-2xl bg-slate-800/40" />
          <Skeleton className="h-64 rounded-2xl bg-slate-800/40" />
          <Skeleton className="h-64 rounded-2xl bg-slate-800/40" />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {filtered.map((g) => (
            <div key={g.category_code} className="cyber-glass-card p-5 sm:p-6 rounded-2xl space-y-4 hover:border-cyber-cyan/50 transition-all flex flex-col justify-between">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono font-bold text-cyber-cyan bg-cyber-cyan/10 px-2 py-0.5 rounded border border-cyber-cyan/20">
                    {g.clause_reference}
                  </span>
                  <span className="text-[10px] font-mono text-slate-400">CCPA 2023</span>
                </div>

                <h3 className="text-sm font-bold text-white tracking-tight">
                  {g.category_name}
                </h3>

                <p className="text-xs text-slate-300 leading-relaxed">
                  {g.plain_explanation}
                </p>
              </div>

              {/* Problematic vs Compliant Examples */}
              <div className="space-y-2.5 pt-2 border-t border-slate-800/80 text-[11px]">
                {g.problematic_examples && g.problematic_examples.length > 0 && (
                  <div className="bg-rose-500/10 border border-rose-500/20 p-2.5 rounded-xl space-y-0.5">
                    <span className="text-rose-400 font-bold block uppercase text-[10px]">Deceptive Behavior:</span>
                    <p className="text-rose-200">{g.problematic_examples[0]}</p>
                  </div>
                )}

                {g.compliant_alternative && (
                  <div className="bg-cyber-emerald/10 border border-cyber-emerald/20 p-2.5 rounded-xl space-y-0.5">
                    <span className="text-cyber-emerald font-bold block uppercase text-[10px]">Compliant Standard:</span>
                    <p className="text-emerald-200">{g.compliant_alternative}</p>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
