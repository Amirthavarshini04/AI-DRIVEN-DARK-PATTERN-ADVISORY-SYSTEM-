import React, { useEffect, useState } from 'react';
import { 
  ShieldAlert, 
  CheckCircle2, 
  AlertTriangle, 
  FileText, 
  Download, 
  Copy, 
  Wrench, 
  ThumbsDown,
  ArrowLeft,
  Check,
  Radio,
  ExternalLink,
  Terminal,
  Scale
} from 'lucide-react';
import { getScanById, submitFeedback } from '../services/api';
import { Scan, Finding } from '../types';
import { Skeleton } from '../components/common/Skeleton';

interface ResultsPageProps {
  scanId: string;
  onNavigate: (page: string, param?: string) => void;
}

export const ResultsPage: React.FC<ResultsPageProps> = ({ scanId, onNavigate }) => {
  const [scan, setScan] = useState<Scan | null>(null);
  const [loading, setLoading] = useState(true);
  const [feedbackSent, setFeedbackSent] = useState<Record<string, boolean>>({});
  const [copiedId, setCopiedId] = useState<string | null>(null);

  useEffect(() => {
    getScanById(scanId)
      .then(res => {
        setScan(res);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, [scanId]);

  if (loading) {
    return (
      <div className="p-4 sm:p-6 lg:p-8 space-y-6 max-w-7xl mx-auto w-full">
        <Skeleton className="h-32 rounded-2xl bg-slate-800/40" />
        <Skeleton className="h-64 rounded-2xl bg-slate-800/40" />
      </div>
    );
  }

  if (!scan) {
    return (
      <div className="p-8 text-center text-slate-400">
        Scan record not found in database.
      </div>
    );
  }

  const handleCopySnippet = (id: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleFeedback = async (findingId: string) => {
    await submitFeedback(findingId, true, 'User flagged potential false positive.');
    setFeedbackSent(prev => ({ ...prev, [findingId]: true }));
  };

  const getRiskBadgeStyles = (score: number) => {
    if (score >= 75) return 'bg-rose-500/15 text-rose-400 border-rose-500/50 shadow-glow-rose';
    if (score >= 50) return 'bg-amber-500/15 text-amber-400 border-amber-500/50 shadow-glow-amber';
    if (score >= 25) return 'bg-cyber-cyan/15 text-cyber-cyan border-cyber-cyan/50 shadow-glow-cyan';
    return 'bg-cyber-emerald/15 text-cyber-emerald border-cyber-emerald/50 shadow-glow-emerald';
  };

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 sm:space-y-8 max-w-7xl mx-auto w-full">
      {/* Back button */}
      <button 
        onClick={() => onNavigate('dashboard')}
        className="flex items-center space-x-1.5 text-xs font-bold text-slate-400 hover:text-cyber-cyan cursor-pointer transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Return to Compliance Dashboard</span>
      </button>

      {/* Header Banner */}
      <div className="cyber-glass-card p-5 sm:p-7 rounded-2xl border border-slate-800/80 flex flex-col md:flex-row items-start md:items-center justify-between gap-5">
        <div className="space-y-1.5 min-w-0">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-[11px] font-mono font-bold uppercase tracking-wider text-cyber-cyan">
              COMPLIANCE DOSSIER
            </span>
            <span className="text-slate-600">•</span>
            <span className="text-xs font-mono text-slate-400">ID: {scan.id.substring(0, 8)}</span>
            <span className="text-slate-600">•</span>
            <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300">
              LANG: {scan.language.toUpperCase()}
            </span>
            <span className="text-slate-600">•</span>
            <span className={`text-[11px] font-mono px-2 py-0.5 rounded font-bold uppercase ${
              scan.status === 'completed' ? 'bg-cyber-emerald/15 text-cyber-emerald border border-cyber-emerald/30' :
              scan.status === 'partially_scanned' ? 'bg-amber-500/15 text-amber-300 border border-amber-500/30' :
              scan.status === 'insufficient_content' ? 'bg-rose-500/15 text-rose-300 border border-rose-500/30' :
              'bg-slate-800 text-slate-300'
            }`}>
              STATUS: {scan.status?.replace('_', ' ') || 'COMPLETED'}
            </span>
          </div>

          <h2 className="text-lg sm:text-2xl font-extrabold text-white tracking-tight break-all font-mono">
            {scan.url || 'Direct Text / DOM Snippet Audit'}
          </h2>
          {scan.page_title && scan.page_title !== scan.url && (
            <p className="text-xs text-cyber-cyan font-medium">
              Page Title: <span className="text-slate-300">{scan.page_title}</span>
            </p>
          )}
          <p className="text-xs text-slate-400">
            Assessed against CCPA Guidelines for Prevention and Regulation of Dark Patterns, 2023.
          </p>
        </div>

        {/* Risk Dial Score */}
        <div className={`p-4 sm:p-5 rounded-2xl border flex items-center space-x-4 shrink-0 ${getRiskBadgeStyles(scan.risk_score)}`}>
          <div className="text-right">
            <div className="text-[11px] font-semibold text-slate-300 uppercase tracking-wider">Combined Page Risk</div>
            <div className="text-sm sm:text-base font-extrabold uppercase">{scan.risk_category} RISK</div>
          </div>
          <div className="text-2xl sm:text-3xl font-black font-mono">
            {scan.risk_score}<span className="text-sm font-normal text-slate-400">/100</span>
          </div>
        </div>
      </div>

      {/* Telemetry & Coverage HUD */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="cyber-glass-card p-4 rounded-xl border border-slate-800 space-y-1">
          <div className="text-[10px] font-mono uppercase tracking-wider text-slate-400">Content Retrieval Method</div>
          <div className="text-xs font-bold text-white flex items-center space-x-1.5 font-mono">
            <Radio className="w-3.5 h-3.5 text-cyber-cyan animate-pulse" />
            <span>
              {scan.fetch_method === 'browser_headless' ? 'Headless Chromium Engine' :
               scan.fetch_method === 'text_input' ? 'Direct DOM Payload' :
               'HTTP/TLS Secure Client'}
            </span>
          </div>
        </div>

        <div className="cyber-glass-card p-4 rounded-xl border border-slate-800 space-y-1">
          <div className="text-[10px] font-mono uppercase tracking-wider text-slate-400">Content Volume Analyzed</div>
          <div className="text-xs font-bold text-white font-mono">
            {scan.content_length_analyzed ? `${scan.content_length_analyzed.toLocaleString()} characters extracted` : 'Direct text snippet'}
          </div>
        </div>

        <div className="cyber-glass-card p-4 rounded-xl border border-slate-800 space-y-1">
          <div className="text-[10px] font-mono uppercase tracking-wider text-slate-400">Audit Timestamp</div>
          <div className="text-xs font-bold text-slate-300 font-mono">
            {new Date(scan.created_at).toLocaleString()}
          </div>
        </div>
      </div>

      {/* Warnings & Notices Banner if any */}
      {scan.warnings && scan.warnings.length > 0 && (
        <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 text-xs space-y-2">
          <div className="flex items-center space-x-2 font-bold text-amber-400">
            <AlertTriangle className="w-4 h-4 shrink-0" />
            <span>Scan Coverage Notices & Limitations:</span>
          </div>
          <ul className="list-disc list-inside text-slate-300 space-y-1 text-[11px] font-mono">
            {scan.warnings.map((w, idx) => (
              <li key={idx}>{w}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Export Quick Bar */}
      <div className="cyber-glass-card p-4 sm:p-5 rounded-2xl border border-cyber-cyan/30 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center space-x-3 text-xs text-slate-300">
          <FileText className="w-5 h-5 text-cyber-cyan shrink-0" />
          <span>Download signed compliance audit report files for viva review & record-keeping:</span>
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          <a
            href={`http://127.0.0.1:8000/api/v1/reports/${scan.id}/pdf`}
            download
            className="px-3.5 py-1.5 bg-gradient-to-r from-cyber-cyan to-brand-600 hover:from-cyan-400 hover:to-indigo-500 text-white text-xs font-bold rounded-xl flex items-center space-x-1.5 shadow-glow-cyan cursor-pointer transition-all"
          >
            <Download className="w-3.5 h-3.5" />
            <span>PDF Dossier</span>
          </a>
          <a
            href={`http://127.0.0.1:8000/api/v1/reports/${scan.id}/csv`}
            download
            className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-xl border border-slate-700 flex items-center space-x-1 cursor-pointer transition-colors"
          >
            <Download className="w-3.5 h-3.5" />
            <span>CSV Dataset</span>
          </a>
          <a
            href={`http://127.0.0.1:8000/api/v1/reports/${scan.id}/json`}
            download
            className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-xl border border-slate-700 flex items-center space-x-1 cursor-pointer transition-colors"
          >
            <Download className="w-3.5 h-3.5" />
            <span>JSON</span>
          </a>
        </div>
      </div>

      {/* Findings List */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-base sm:text-lg font-bold text-white tracking-tight flex items-center space-x-2">
            <span>Detected Manipulative Patterns</span>
            <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-cyber-cyan font-mono border border-slate-700">
              {scan.findings.length} findings
            </span>
          </h3>
        </div>

        {scan.findings.length === 0 ? (
          scan.status === 'insufficient_content' ? (
            <div className="cyber-glass-card p-8 sm:p-10 rounded-2xl text-center space-y-3 border border-amber-500/30">
              <AlertTriangle className="w-10 h-10 text-amber-400 mx-auto" />
              <h4 className="text-base font-bold text-amber-300">Insufficient Page Content Retrieved</h4>
              <p className="text-xs text-slate-300 max-w-lg mx-auto leading-relaxed">
                The scanner could not extract sufficient readable text from this webpage ({scan.content_length_analyzed || 0} characters analyzed).
                The target site may be blocking automated requests with Cloudflare/CAPTCHA, requiring user login, or rendering content via protected APIs.
              </p>
              <div className="text-[11px] font-mono text-slate-400 pt-2">
                Note: A score of 0/100 under insufficient content indicates incomplete data, not confirmed compliance.
              </div>
            </div>
          ) : (
            <div className="cyber-glass-card p-8 sm:p-12 rounded-2xl text-center space-y-3 border border-cyber-emerald/30">
              <CheckCircle2 className="w-10 h-10 text-cyber-emerald mx-auto" />
              <h4 className="text-base font-bold text-white">No Dark Patterns Identified</h4>
              <p className="text-xs text-slate-300 max-w-md mx-auto">
                The inspected page elements ({scan.content_length_analyzed?.toLocaleString() || 'all'} characters) conform to transparent, non-deceptive interface standards under CCPA 2023.
              </p>
            </div>
          )
        ) : (
          scan.findings.map((f: Finding) => (
            <div key={f.id} className="cyber-glass-card p-5 sm:p-7 rounded-2xl space-y-5 hover:border-cyber-cyan/40 transition-all">
              {/* Category & Severity Header */}
              <div className="flex flex-wrap items-center justify-between gap-3">
                <div className="flex flex-wrap items-center gap-2.5">
                  <span className="px-3 py-1 bg-cyber-cyan/15 text-cyber-cyan text-xs font-extrabold rounded-xl border border-cyber-cyan/30">
                    {f.category}
                  </span>
                  <span className={`px-2.5 py-0.5 text-[11px] font-bold rounded-full border ${
                    f.severity === 'Critical' ? 'bg-rose-500/15 text-rose-400 border-rose-500/40' :
                    f.severity === 'High' ? 'bg-amber-500/15 text-amber-400 border-amber-500/40' :
                    'bg-slate-800 text-slate-300 border-slate-700'
                  }`}>
                    {f.severity} Severity
                  </span>
                </div>

                <div className="text-xs font-mono text-slate-400">
                  Confidence: <span className="text-white font-bold">{Math.round(f.confidence * 100)}%</span>
                </div>
              </div>

              {/* Exact Snippet Box */}
              <div className="p-4 bg-obsidian-900/90 border border-slate-800/80 rounded-xl relative group font-mono text-xs leading-relaxed text-slate-200">
                <div className="text-[10px] uppercase font-sans font-bold text-slate-400 mb-1.5 flex items-center space-x-1.5">
                  <Terminal className="w-3.5 h-3.5 text-cyber-cyan" />
                  <span>Triggering Evidence DOM Snippet</span>
                </div>
                <div className="pr-8 text-amber-300">
                  "{f.text_snippet}"
                </div>

                <button
                  onClick={() => handleCopySnippet(f.id, f.text_snippet)}
                  className="absolute right-3 top-3 p-1.5 rounded-lg text-slate-400 hover:text-white bg-slate-800/60 hover:bg-slate-700 transition-colors cursor-pointer"
                  title="Copy snippet"
                >
                  {copiedId === f.id ? <Check className="w-4 h-4 text-cyber-emerald" /> : <Copy className="w-4 h-4" />}
                </button>
              </div>

              {/* Legal Reference & Recommendation Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                {/* Legal Clause Box */}
                <div className="bg-obsidian-900/70 border border-amber-500/30 p-4 rounded-xl space-y-1.5">
                  <div className="font-bold text-amber-400 flex items-center space-x-1.5">
                    <ShieldAlert className="w-4 h-4 text-amber-400" />
                    <span>CCPA 2023 Guideline Citation</span>
                  </div>
                  <div className="text-amber-200 font-semibold font-mono">
                    {f.ccpa_clause} ({f.ccpa_category})
                  </div>
                  <p className="text-slate-300 text-[11px] leading-relaxed">
                    {f.rationale}
                  </p>
                </div>

                {/* Compliant Suggestion Box */}
                <div className="bg-obsidian-900/70 border border-cyber-emerald/30 p-4 rounded-xl space-y-1.5">
                  <div className="font-bold text-cyber-emerald flex items-center space-x-1.5">
                    <CheckCircle2 className="w-4 h-4 text-cyber-emerald" />
                    <span>Compliant Alternative Recommendation</span>
                  </div>
                  <p className="text-slate-200 text-[11px] leading-relaxed">
                    {f.recommendation}
                  </p>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-slate-800/80">
                <button
                  onClick={() => onNavigate('remediation', f.id)}
                  className="bg-gradient-to-r from-cyber-cyan to-brand-600 hover:from-cyan-400 hover:to-indigo-500 text-white text-xs font-bold px-4 py-2 rounded-xl flex items-center space-x-2 shadow-glow-cyan cursor-pointer transition-all"
                >
                  <Wrench className="w-3.5 h-3.5" />
                  <span>Launch Autonomous Remediation</span>
                </button>

                <button
                  onClick={() => handleFeedback(f.id)}
                  disabled={feedbackSent[f.id]}
                  className="text-slate-400 hover:text-slate-200 text-xs font-medium flex items-center space-x-1.5 cursor-pointer disabled:text-slate-600 transition-colors"
                >
                  <ThumbsDown className="w-3.5 h-3.5" />
                  <span>{feedbackSent[f.id] ? 'False Positive Logged' : 'Flag Potential False Positive'}</span>
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
