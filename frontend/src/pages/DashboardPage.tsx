import React, { useEffect, useState } from 'react';
import { 
  ShieldAlert, 
  Search, 
  AlertTriangle, 
  CheckCircle2, 
  TrendingUp, 
  Globe, 
  ArrowUpRight,
  Sparkles,
  Radio,
  Activity,
  Layers
} from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip } from 'recharts';
import { getAnalytics } from '../services/api';
import { AnalyticsOverview } from '../types';
import { Skeleton } from '../components/common/Skeleton';

interface DashboardProps {
  onNavigate: (page: string, param?: string) => void;
}

const CYBER_COLORS = ['#f43f5e', '#f59e0b', '#06b6d4', '#10b981', '#a855f7', '#6366f1'];

export const DashboardPage: React.FC<DashboardProps> = ({ onNavigate }) => {
  const [data, setData] = useState<AnalyticsOverview | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAnalytics()
      .then(res => {
        setData(res);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="p-4 sm:p-6 lg:p-8 space-y-6 max-w-7xl mx-auto w-full">
        <Skeleton className="h-28 w-full rounded-2xl bg-slate-800/40" />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <Skeleton className="h-28 rounded-xl bg-slate-800/40" />
          <Skeleton className="h-28 rounded-xl bg-slate-800/40" />
          <Skeleton className="h-28 rounded-xl bg-slate-800/40" />
          <Skeleton className="h-28 rounded-xl bg-slate-800/40" />
        </div>
      </div>
    );
  }

  const categoryChartData = data?.category_distribution 
    ? Object.entries(data.category_distribution).map(([name, value]) => ({ name, value }))
    : [];

  const severityChartData = data?.severity_distribution
    ? Object.entries(data.severity_distribution).map(([name, value]) => ({ name, value }))
    : [];

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-obsidian-900/95 border border-slate-700/80 p-2.5 rounded-lg shadow-xl text-xs backdrop-blur-md">
          <p className="font-bold text-white">{label || payload[0].name}</p>
          <p className="text-cyber-cyan font-mono font-semibold">{payload[0].value} findings</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 sm:space-y-8 max-w-7xl mx-auto w-full">
      {/* Top Cyber Telemetry Quick Banner */}
      <div className="cyber-glass-card p-5 sm:p-6 rounded-2xl border border-cyber-cyan/30 shadow-glow-cyan flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center space-x-2">
            <Radio className="w-4 h-4 text-cyber-emerald animate-pulse" />
            <span className="text-[11px] font-bold tracking-wider uppercase text-cyber-emerald">Telemetry Active</span>
            <span className="text-slate-500">•</span>
            <span className="text-xs text-slate-300 font-mono">CCPA Guidelines 2023 Enforcement</span>
          </div>
          <h2 className="text-lg sm:text-xl font-extrabold text-white tracking-tight">
            Compliance Sentinel Dashboard
          </h2>
          <p className="text-xs text-slate-300 max-w-2xl leading-relaxed">
            Real-time analytics evaluating manipulative patterns across English, Hindi & Tamil e-commerce platforms.
          </p>
        </div>

        <button
          onClick={() => onNavigate('scan')}
          className="bg-gradient-to-r from-cyber-cyan to-brand-600 hover:from-cyan-400 hover:to-indigo-500 text-white font-bold text-xs px-5 py-2.5 rounded-xl shadow-glow-cyan flex items-center space-x-2 cursor-pointer transition-all hover:scale-[1.02] shrink-0"
        >
          <Search className="w-4 h-4" />
          <span>Launch New Scan</span>
        </button>
      </div>

      {/* Holographic Metric Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
        {/* Card 1 */}
        <div className="cyber-glass-card p-5 rounded-2xl hover:border-cyber-cyan/50 transition-all">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400">Total Scans</span>
            <div className="p-2 bg-cyber-cyan/15 text-cyber-cyan rounded-xl border border-cyber-cyan/30">
              <Search className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl sm:text-3xl font-extrabold text-white mt-3 font-mono">
            {data?.total_scans || 0}
          </div>
          <p className="text-[11px] text-slate-400 mt-1 flex items-center space-x-1">
            <span className="text-cyber-cyan font-semibold">100%</span>
            <span>recorded in database</span>
          </p>
        </div>

        {/* Card 2 */}
        <div className="cyber-glass-card p-5 rounded-2xl hover:border-amber-500/50 transition-all">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400">Dark Pattern Detections</span>
            <div className="p-2 bg-amber-500/15 text-amber-400 rounded-xl border border-amber-500/30">
              <AlertTriangle className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl sm:text-3xl font-extrabold text-amber-400 mt-3 font-mono">
            {data?.total_findings || 0}
          </div>
          <p className="text-[11px] text-slate-400 mt-1">
            Manipulative elements detected
          </p>
        </div>

        {/* Card 3 */}
        <div className="cyber-glass-card p-5 rounded-2xl hover:border-rose-500/50 transition-all">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400">High Risk Pages</span>
            <div className="p-2 bg-rose-500/15 text-rose-400 rounded-xl border border-rose-500/30">
              <ShieldAlert className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl sm:text-3xl font-extrabold text-rose-400 mt-3 font-mono">
            {data?.high_risk_pages_count || 0}
          </div>
          <p className="text-[11px] text-slate-400 mt-1">
            Pages exceeding 50/100 risk score
          </p>
        </div>

        {/* Card 4 */}
        <div className="cyber-glass-card p-5 rounded-2xl hover:border-cyber-emerald/50 transition-all">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400">Average Risk Score</span>
            <div className="p-2 bg-cyber-emerald/15 text-cyber-emerald rounded-xl border border-cyber-emerald/30">
              <TrendingUp className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl sm:text-3xl font-extrabold text-white mt-3 font-mono">
            {data?.avg_risk_score || 0} <span className="text-xs text-slate-400 font-normal">/ 100</span>
          </div>
          <p className="text-[11px] text-slate-400 mt-1">
            Calibrated multi-factor index
          </p>
        </div>
      </div>

      {/* Visual Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Category Breakdown Pie */}
        <div className="cyber-glass-card p-5 sm:p-6 rounded-2xl space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-white tracking-tight">Dark Pattern Category Breakdown</h3>
              <p className="text-[11px] text-slate-400">Distribution across 13 CCPA 2023 Guidelines</p>
            </div>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-cyber-cyan border border-slate-700">
              CCPA-CATEGORIES
            </span>
          </div>

          <div className="h-64 sm:h-72 w-full">
            {categoryChartData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={categoryChartData}
                    cx="50%"
                    cy="50%"
                    innerRadius={55}
                    outerRadius={85}
                    paddingAngle={4}
                    dataKey="value"
                  >
                    {categoryChartData.map((_, index) => (
                      <Cell key={`cell-${index}`} fill={CYBER_COLORS[index % CYBER_COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip content={<CustomTooltip />} />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-xs text-slate-400">No findings data recorded</div>
            )}
          </div>
        </div>

        {/* Severity Distribution Bar */}
        <div className="cyber-glass-card p-5 sm:p-6 rounded-2xl space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-white tracking-tight">Findings Severity Distribution</h3>
              <p className="text-[11px] text-slate-400">Weighted impact of identified manipulative elements</p>
            </div>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-amber-400 border border-slate-700">
              SEVERITY-INDEX
            </span>
          </div>

          <div className="h-64 sm:h-72 w-full">
            {severityChartData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={severityChartData}>
                  <XAxis dataKey="name" stroke="#64748b" fontSize={11} />
                  <YAxis stroke="#64748b" fontSize={11} />
                  <Tooltip content={<CustomTooltip />} />
                  <Bar dataKey="value" fill="#06b6d4" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-xs text-slate-400">No severity metrics recorded</div>
            )}
          </div>
        </div>
      </div>

      {/* Recent Scans Activity Feed */}
      <div className="cyber-glass-card rounded-2xl overflow-hidden">
        <div className="p-5 sm:p-6 border-b border-slate-800/80 flex items-center justify-between">
          <div>
            <h3 className="text-sm font-bold text-white tracking-tight">Recent Compliance Scans</h3>
            <p className="text-[11px] text-slate-400">Live stream of audited e-commerce endpoints</p>
          </div>
          <button 
            onClick={() => onNavigate('history')} 
            className="text-xs font-semibold text-cyber-cyan hover:text-cyan-300 flex items-center space-x-1 cursor-pointer transition-colors"
          >
            <span>Full History</span>
            <ArrowUpRight className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="divide-y divide-slate-800/60">
          {data?.recent_scans && data.recent_scans.length > 0 ? (
            data.recent_scans.map(s => (
              <div 
                key={s.id} 
                onClick={() => onNavigate('results', s.id)}
                className="p-4 sm:p-5 hover:bg-slate-800/30 flex flex-col sm:flex-row sm:items-center justify-between gap-3 cursor-pointer transition-colors"
              >
                <div className="space-y-1 min-w-0">
                  <div className="text-xs sm:text-sm font-bold text-white truncate font-mono">
                    {s.url}
                  </div>
                  <div className="text-[11px] text-slate-400 flex items-center space-x-2">
                    <span className="text-rose-400 font-semibold">{s.findings_count} dark patterns found</span>
                    <span>•</span>
                    <span className="capitalize">{s.url ? 'URL analysis' : 'Text analysis'}</span>
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
                  <ArrowUpRight className="w-4 h-4 text-slate-400" />
                </div>
              </div>
            ))
          ) : (
            <div className="p-8 text-center text-xs text-slate-400">No scan history recorded in database.</div>
          )}
        </div>
      </div>
    </div>
  );
};
