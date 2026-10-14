import React, { useEffect, useState } from 'react';
import { History, Search, Trash2, ArrowUpRight, Download, RefreshCw, Radio } from 'lucide-react';
import { getScans, deleteScan } from '../services/api';
import { Scan } from '../types';
import { Skeleton } from '../components/common/Skeleton';

interface HistoryPageProps {
  onNavigate: (page: string, param?: string) => void;
}

export const HistoryPage: React.FC<HistoryPageProps> = ({ onNavigate }) => {
  const [scans, setScans] = useState<Scan[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);

  const fetchHistory = () => {
    setLoading(true);
    getScans(searchTerm)
      .then(res => {
        setScans(res.items);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchHistory();
  }, [searchTerm]);

  const handleDelete = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    if (window.confirm('Delete this compliance scan audit record from SQLite database?')) {
      await deleteScan(id);
      fetchHistory();
    }
  };

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 sm:space-y-8 max-w-7xl mx-auto w-full">
      {/* Banner */}
      <div className="cyber-glass-card p-5 sm:p-7 rounded-2xl border border-cyber-cyan/30 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <Radio className="w-4 h-4 text-cyber-cyan animate-pulse" />
            <span className="text-[11px] font-bold uppercase tracking-wider text-cyber-cyan">Database Ledger</span>
          </div>
          <h2 className="text-xl sm:text-2xl font-extrabold text-white tracking-tight mt-1">
            Compliance Audit History
          </h2>
          <p className="text-xs text-slate-300 mt-1 max-w-2xl leading-relaxed">
            Persisted historical logs of analyzed Indian e-commerce web URLs and text snippets stored in SQLite/PostgreSQL.
          </p>
        </div>

        <div className="relative w-full sm:w-72">
          <Search className="w-4 h-4 text-cyber-cyan absolute left-3.5 top-3" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search by URL or keyword..."
            className="w-full pl-10 pr-4 py-2.5 bg-obsidian-900/90 text-white border border-slate-700/80 rounded-xl text-xs font-mono focus:border-cyber-cyan focus:outline-none transition-colors"
          />
        </div>
      </div>

      {/* History Table / Cards */}
      <div className="cyber-glass-card rounded-2xl overflow-hidden">
        {loading ? (
          <div className="p-6 space-y-4">
            <Skeleton className="h-16 rounded-xl bg-slate-800/40" />
            <Skeleton className="h-16 rounded-xl bg-slate-800/40" />
            <Skeleton className="h-16 rounded-xl bg-slate-800/40" />
          </div>
        ) : scans.length === 0 ? (
          <div className="p-12 text-center text-xs text-slate-400">
            No compliance scan records found matching "{searchTerm}".
          </div>
        ) : (
          <div className="divide-y divide-slate-800/60">
            {scans.map((s) => (
              <div
                key={s.id}
                onClick={() => onNavigate('results', s.id)}
                className="p-4 sm:p-5 hover:bg-slate-800/30 flex flex-col sm:flex-row sm:items-center justify-between gap-4 cursor-pointer transition-colors"
              >
                <div className="space-y-1.5 min-w-0">
                  <div className="text-xs sm:text-sm font-bold text-white truncate font-mono">
                    {s.url}
                  </div>
                  <div className="flex flex-wrap items-center gap-2 text-[11px] text-slate-400">
                    <span className="text-rose-400 font-semibold">{s.findings_count ?? (s.findings?.length ?? 0)} dark patterns</span>
                    <span>•</span>
                    <span className="capitalize">{s.scan_type} analysis</span>
                    <span>•</span>
                    <span className="uppercase font-mono">{s.language}</span>
                    <span>•</span>
                    <span className="font-mono text-slate-400">{new Date(s.created_at).toLocaleString()}</span>
                  </div>
                </div>

                <div className="flex items-center space-x-3 self-end sm:self-auto shrink-0">
                  <span className={`px-3 py-1 rounded-full text-xs font-bold font-mono border ${
                    s.risk_score >= 75 ? 'bg-rose-500/15 text-rose-400 border-rose-500/40' :
                    s.risk_score >= 50 ? 'bg-amber-500/15 text-amber-400 border-amber-500/40' :
                    'bg-cyber-emerald/15 text-cyber-emerald border-cyber-emerald/40'
                  }`}>
                    {s.risk_score}/100 ({s.risk_category})
                  </span>

                  <button
                    onClick={(e) => handleDelete(e, s.id)}
                    className="p-2 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 transition-colors"
                    title="Delete record"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>

                  <ArrowUpRight className="w-4 h-4 text-slate-400" />
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
