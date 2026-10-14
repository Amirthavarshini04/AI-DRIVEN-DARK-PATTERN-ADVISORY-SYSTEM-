import React from 'react';
import { BarChart3, Scale, Zap, Info, ShieldAlert, Cpu, Radio, Network } from 'lucide-react';

export const RiskAnalyticsPage: React.FC = () => {
  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 sm:space-y-8 max-w-7xl mx-auto w-full">
      {/* Banner */}
      <div className="cyber-glass-card p-5 sm:p-7 rounded-2xl border border-cyber-cyan/30 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <Radio className="w-4 h-4 text-cyber-cyan animate-pulse" />
            <span className="text-[11px] font-bold uppercase tracking-wider text-cyber-cyan">Mathematical Telemetry</span>
          </div>
          <h2 className="text-xl sm:text-2xl font-extrabold text-white tracking-tight mt-1">
            Learned Combined-Risk Scoring Engine
          </h2>
          <p className="text-xs text-slate-300 mt-1 max-w-2xl leading-relaxed">
            Mathematical formulation and multi-factor co-occurrence mechanics for 7th-semester major engineering project evaluation.
          </p>
        </div>

        <div className="px-3 py-1.5 rounded-xl bg-obsidian-900/90 border border-slate-700/80 text-xs font-mono text-slate-300">
          Model: Logistic Regression + Co-occurrence Multiplier
        </div>
      </div>

      {/* Mathematical Formula Card */}
      <div className="cyber-glass-card p-5 sm:p-7 rounded-2xl space-y-4 border border-cyber-cyan/40 shadow-glow-cyan">
        <div className="flex items-center space-x-2 text-cyber-cyan">
          <Cpu className="w-5 h-5 text-cyber-cyan" />
          <h3 className="text-sm font-extrabold tracking-tight">Scoring Formulation & Feature Aggregation</h3>
        </div>

        <div className="p-4 sm:p-5 bg-obsidian-950/90 rounded-xl font-mono text-xs sm:text-sm text-cyber-cyan border border-cyber-cyan/30 shadow-inner overflow-x-auto">
          Page Risk Score S = Min( 100 , ∑ ( SeverityWeight_i ) × Multiplier_CoOccurrence )
        </div>

        <p className="text-xs text-slate-300 leading-relaxed">
          The risk scoring module calculates page-level risk using calibrated severity weights (<span className="text-rose-400 font-bold">Critical: 35.0</span>, <span className="text-amber-400 font-bold">High: 25.0</span>, <span className="text-cyber-cyan font-bold">Medium: 15.0</span>, <span className="text-cyber-emerald font-bold">Low: 8.0</span>) and applies non-linear interaction coefficients when compound patterns (e.g., False Urgency + Drip Pricing) co-occur on the same e-commerce page.
        </p>
      </div>

      {/* Risk Threshold Bands */}
      <div className="cyber-glass-card p-5 sm:p-7 rounded-2xl space-y-4">
        <h3 className="text-sm font-bold text-white tracking-tight">Risk Threshold Classification Bands</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-4 rounded-xl bg-cyber-emerald/10 border border-cyber-emerald/30 text-center space-y-1">
            <div className="text-xs font-mono font-bold text-cyber-emerald">0 – 25</div>
            <div className="text-sm font-black text-white">Low Risk</div>
            <div className="text-[11px] text-slate-400">Transparent or clean user flow</div>
          </div>

          <div className="p-4 rounded-xl bg-cyber-cyan/10 border border-cyber-cyan/30 text-center space-y-1">
            <div className="text-xs font-mono font-bold text-cyber-cyan">26 – 50</div>
            <div className="text-sm font-black text-white">Moderate Risk</div>
            <div className="text-[11px] text-slate-400">Single low-impact deceptive element</div>
          </div>

          <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 text-center space-y-1">
            <div className="text-xs font-mono font-bold text-amber-400">51 – 75</div>
            <div className="text-sm font-black text-white">High Risk</div>
            <div className="text-[11px] text-slate-400">Multiple deceptive patterns present</div>
          </div>

          <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-center space-y-1">
            <div className="text-xs font-mono font-bold text-rose-400">76 – 100</div>
            <div className="text-sm font-black text-white">Critical Risk</div>
            <div className="text-[11px] text-slate-400">Compound coercion (Drip fees + False rush)</div>
          </div>
        </div>
      </div>

      {/* Co-occurrence Multiplier Matrix */}
      <div className="cyber-glass-card p-5 sm:p-7 rounded-2xl space-y-4">
        <div className="flex items-center space-x-2 text-white">
          <Network className="w-4 h-4 text-cyber-cyan" />
          <h3 className="text-sm font-bold tracking-tight">Pattern Co-Occurrence Interaction Multipliers</h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div className="p-4 rounded-xl bg-obsidian-900/90 border border-slate-800/80 space-y-1.5">
            <div className="font-bold text-cyber-cyan">False Urgency + Drip Pricing</div>
            <div className="font-mono text-xs text-rose-400 font-bold">Multiplier: 1.35x</div>
            <p className="text-[11px] text-slate-400 leading-relaxed">
              Hurries the consumer into checkout so they do not scrutinize hidden add-on fees.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-obsidian-900/90 border border-slate-800/80 space-y-1.5">
            <div className="font-bold text-cyber-cyan">Confirm Shaming + Basket Sneaking</div>
            <div className="font-mono text-xs text-amber-400 font-bold">Multiplier: 1.25x</div>
            <p className="text-[11px] text-slate-400 leading-relaxed">
              Sneaks unwanted insurance/warranty and guilt-trips the consumer upon opt-out.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-obsidian-900/90 border border-slate-800/80 space-y-1.5">
            <div className="font-bold text-cyber-cyan">Interface Interference + Trick Wording</div>
            <div className="font-mono text-xs text-amber-400 font-bold">Multiplier: 1.20x</div>
            <p className="text-[11px] text-slate-400 leading-relaxed">
              Camouflages action buttons and uses confusing double-negatives to trap choices.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
