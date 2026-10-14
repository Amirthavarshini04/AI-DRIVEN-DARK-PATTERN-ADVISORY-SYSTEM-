import React, { useEffect, useState } from 'react';
import { FileText, Download, FileSpreadsheet, Code, ShieldCheck, Radio } from 'lucide-react';
import { getScans } from '../services/api';
import { Scan } from '../types';

export const ReportsPage: React.FC = () => {
  const [scans, setScans] = useState<Scan[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getScans()
      .then(res => {
        setScans(res.items);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 sm:space-y-8 max-w-7xl mx-auto w-full">
      {/* Banner */}
      <div className="cyber-glass-card p-5 sm:p-7 rounded-2xl border border-cyber-cyan/30 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <Radio className="w-4 h-4 text-cyber-cyan animate-pulse" />
            <span className="text-[11px] font-bold uppercase tracking-wider text-cyber-cyan">Document Engine</span>
          </div>
          <h2 className="text-xl sm:text-2xl font-extrabold text-white tracking-tight mt-1">
            Audit Reports & Document Export Generator
          </h2>
          <p className="text-xs text-slate-300 mt-1 max-w-2xl leading-relaxed">
            Generate verifiable compliance audit dossiers in PDF, CSV, and JSON formats for viva submission and major project evaluation.
          </p>
        </div>

        <div className="px-3 py-1.5 rounded-xl bg-obsidian-900/90 border border-slate-700/80 text-xs font-mono text-slate-300">
          Engine: ReportLab / UTF-8
        </div>
      </div>

      {/* 3 Export Formats Feature Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="cyber-glass-card p-5 sm:p-6 rounded-2xl space-y-3 hover:border-cyber-cyan/50 transition-all">
          <div className="p-3 bg-cyber-cyan/15 text-cyber-cyan rounded-xl w-fit border border-cyber-cyan/30">
            <FileText className="w-6 h-6" />
          </div>
          <h3 className="text-sm font-bold text-white">PDF Executive Audit Report</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Standard compliance report with metadata, risk score dial, findings table, CCPA clause citations, and legal disclaimer.
          </p>
        </div>

        <div className="cyber-glass-card p-5 sm:p-6 rounded-2xl space-y-3 hover:border-cyber-emerald/50 transition-all">
          <div className="p-3 bg-cyber-emerald/15 text-cyber-emerald rounded-xl w-fit border border-cyber-emerald/30">
            <FileSpreadsheet className="w-6 h-6" />
          </div>
          <h3 className="text-sm font-bold text-white">CSV Structured Dataset</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Raw findings data with text snippets, confidence scores, and CCPA clause references ready for spreadsheet processing.
          </p>
        </div>

        <div className="cyber-glass-card p-5 sm:p-6 rounded-2xl space-y-3 hover:border-purple-500/50 transition-all">
          <div className="p-3 bg-purple-500/15 text-purple-400 rounded-xl w-fit border border-purple-500/30">
            <Code className="w-6 h-6" />
          </div>
          <h3 className="text-sm font-bold text-white">JSON API Payload</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Standard JSON document containing complete scan metadata, findings array, and model output metrics.
          </p>
        </div>
      </div>

      {/* Available Downloads List */}
      <div className="cyber-glass-card rounded-2xl overflow-hidden space-y-4 p-5 sm:p-6">
        <h3 className="text-sm font-bold text-white tracking-tight">Available Audit Reports for Download</h3>

        {loading ? (
          <div className="text-xs text-slate-400">Loading audit records...</div>
        ) : scans.length === 0 ? (
          <div className="text-xs text-slate-400">No scans available yet to export.</div>
        ) : (
          <div className="divide-y divide-slate-800/60">
            {scans.slice(0, 10).map((s) => (
              <div key={s.id} className="py-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div className="space-y-1 min-w-0">
                  <div className="text-xs sm:text-sm font-bold text-white truncate font-mono">{s.url}</div>
                  <div className="text-[11px] text-slate-400">
                    Risk: <span className="text-rose-400 font-bold">{s.risk_score}/100</span> • {s.findings_count ?? (s.findings?.length ?? 0)} findings • {new Date(s.created_at).toLocaleDateString()}
                  </div>
                </div>

                <div className="flex flex-wrap items-center gap-2 shrink-0">
                  <a
                    href={`http://127.0.0.1:8000/api/v1/reports/${s.id}/pdf`}
                    download
                    className="px-3 py-1.5 bg-gradient-to-r from-cyber-cyan to-brand-600 hover:from-cyan-400 hover:to-indigo-500 text-white text-xs font-bold rounded-xl flex items-center space-x-1 shadow-glow-cyan transition-all"
                  >
                    <Download className="w-3.5 h-3.5" />
                    <span>PDF</span>
                  </a>
                  <a
                    href={`http://127.0.0.1:8000/api/v1/reports/${s.id}/csv`}
                    download
                    className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-xl border border-slate-700 flex items-center space-x-1 transition-colors"
                  >
                    <Download className="w-3.5 h-3.5" />
                    <span>CSV</span>
                  </a>
                  <a
                    href={`http://127.0.0.1:8000/api/v1/reports/${s.id}/json`}
                    download
                    className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-xl border border-slate-700 flex items-center space-x-1 transition-colors"
                  >
                    <Download className="w-3.5 h-3.5" />
                    <span>JSON</span>
                  </a>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
