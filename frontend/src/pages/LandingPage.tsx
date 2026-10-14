import React, { useState } from 'react';
import { 
  ShieldCheck, 
  Search, 
  Scale, 
  ArrowRight, 
  Sparkles, 
  Globe, 
  Zap, 
  CheckCircle2, 
  AlertTriangle,
  Radio,
  FileCheck2,
  Terminal,
  Activity,
  ChevronRight,
  Layers
} from 'lucide-react';

interface LandingPageProps {
  onStartScan: () => void;
  onOpenDashboard: () => void;
}

export const LandingPage: React.FC<LandingPageProps> = ({ onStartScan, onOpenDashboard }) => {
  const [activeTab, setActiveTab] = useState<'demo' | 'multilingual' | 'ccpa'>('demo');

  const ccpaGuidelines = [
    { title: 'False Urgency', desc: 'Fabricating artificial scarcity or countdown clocks.', severity: 'High' },
    { title: 'Basket Sneaking', desc: 'Adding unrequested add-ons or charity fees to cart.', severity: 'Critical' },
    { title: 'Confirm Shaming', desc: 'Guilt-tripping user for declining opt-ins.', severity: 'Medium' },
    { title: 'Forced Action', desc: 'Mandating unrelated permissions or bundled purchases.', severity: 'Critical' },
    { title: 'Subscription Trap', desc: 'Concealing cancellation flows or auto-renewals.', severity: 'Critical' },
    { title: 'Interface Interference', desc: 'Deceptive visual styling or hidden checkboxes.', severity: 'High' },
    { title: 'Drip Pricing', desc: 'Revealing essential fees only at the final payment step.', severity: 'Critical' },
    { title: 'Bait & Switch', desc: 'Advertising one outcome but delivering another.', severity: 'High' },
    { title: 'Disguised Ads', desc: 'Camouflaging commercial ads as editorial content.', severity: 'Medium' },
    { title: 'Nagging', desc: 'Repeated disruption demanding unneeded choices.', severity: 'Low' },
    { title: 'Trick Wording', desc: 'Confusing double-negatives in privacy opt-outs.', severity: 'Medium' },
    { title: 'SaaS Billing', desc: 'Silent credit card charging without invoice notice.', severity: 'Critical' },
    { title: 'Deceptive Counting', desc: 'Stating fake views like "43 people looking now".', severity: 'High' },
  ];

  return (
    <div className="min-h-screen bg-obsidian-950 text-slate-100 cyber-mesh-bg flex flex-col selection:bg-cyber-cyan selection:text-obsidian-950">
      {/* Top Navbar */}
      <header className="border-b border-slate-800/80 bg-obsidian-900/60 backdrop-blur-xl sticky top-0 z-30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex items-center justify-between">
          <div className="flex items-center space-x-3 cursor-pointer group" onClick={onOpenDashboard}>
            <div className="p-2 bg-gradient-to-br from-cyber-cyan/20 to-cyber-emerald/20 border border-cyber-cyan/40 rounded-xl text-cyber-cyan shadow-glow-cyan group-hover:scale-105 transition-transform">
              <ShieldCheck className="w-5 h-5 text-cyber-cyan" />
            </div>
            <div>
              <span className="text-base font-extrabold tracking-tight text-white">DarkPattern AI</span>
              <span className="hidden sm:inline-block ml-2 text-[10px] font-mono text-cyber-emerald bg-cyber-emerald/10 px-2 py-0.5 rounded-full border border-cyber-emerald/30">
                CCPA 2023 COMPLIANT
              </span>
            </div>
          </div>

          <div className="flex items-center space-x-2 sm:space-x-4">
            <button 
              onClick={onOpenDashboard}
              className="text-xs font-semibold text-slate-300 hover:text-white px-3 py-2 rounded-lg hover:bg-slate-800/60 transition-colors cursor-pointer"
            >
              Dashboard
            </button>
            <button 
              onClick={onStartScan}
              className="bg-gradient-to-r from-cyber-cyan to-brand-600 hover:from-cyan-400 hover:to-indigo-500 text-white font-bold text-xs px-4 py-2 rounded-xl transition-all shadow-glow-cyan flex items-center space-x-1.5 cursor-pointer hover:scale-[1.02]"
            >
              <span>Launch Scanner</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative pt-12 pb-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full flex-1">
        {/* Glowing Decorative Background Badges */}
        <div className="text-center max-w-3xl mx-auto space-y-6">
          <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-slate-900/90 border border-cyber-cyan/40 shadow-glow-cyan text-xs">
            <Radio className="w-3.5 h-3.5 text-cyber-emerald animate-pulse" />
            <span className="text-slate-300 font-medium">Undergraduate 7th Sem Major Engineering Project</span>
            <span className="w-1.5 h-1.5 rounded-full bg-slate-600"></span>
            <span className="text-cyber-cyan font-semibold">Autonomous Legal Sentinel</span>
          </div>

          <h1 className="text-3xl sm:text-5xl lg:text-6xl font-black tracking-tight leading-[1.15] text-white">
            AI-Driven Dark Pattern Detection & <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyber-cyan via-brand-500 to-cyber-emerald">Legal Compliance</span> System
          </h1>

          <p className="text-sm sm:text-base text-slate-300 leading-relaxed max-w-2xl mx-auto">
            Detect manipulative e-commerce patterns across <span className="text-white font-semibold">English, Hindi (हिंदी), and Tamil (தமிழ்)</span>. 
            Calibrate risk under India's <span className="text-cyber-cyan font-semibold">CCPA Guidelines 2023</span> and generate autonomous text remediations.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
            <button 
              onClick={onStartScan}
              className="w-full sm:w-auto bg-gradient-to-r from-cyber-cyan to-brand-600 hover:from-cyan-400 hover:to-indigo-500 text-white font-bold text-sm px-7 py-3 rounded-xl transition-all shadow-glow-cyan flex items-center justify-center space-x-2 cursor-pointer hover:scale-[1.02]"
            >
              <Search className="w-4 h-4" />
              <span>Scan Website or Text</span>
              <ArrowRight className="w-4 h-4 ml-1" />
            </button>
            <button 
              onClick={onOpenDashboard}
              className="w-full sm:w-auto bg-slate-900/80 hover:bg-slate-800 text-slate-200 border border-slate-700/80 font-semibold text-sm px-6 py-3 rounded-xl transition-colors flex items-center justify-center space-x-2 cursor-pointer"
            >
              <Activity className="w-4 h-4 text-cyber-emerald" />
              <span>Open Compliance Dashboard</span>
            </button>
          </div>
        </div>

        {/* Live Interactive Telemetry Preview Card */}
        <div className="mt-12 sm:mt-16 cyber-glass-card rounded-2xl p-4 sm:p-6 lg:p-8 max-w-5xl mx-auto relative overflow-hidden border border-slate-800/90 shadow-cyber-card">
          {/* Holographic Header Bar */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-800/80 gap-3">
            <div className="flex items-center space-x-2 text-xs font-mono text-slate-300">
              <Terminal className="w-4 h-4 text-cyber-cyan" />
              <span className="text-cyber-cyan font-bold">SENTINEL-INSPECT:</span>
              <span className="truncate max-w-xs text-slate-400">https://quick-buy-india.example/checkout</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-[11px] font-bold px-2.5 py-1 rounded-full bg-rose-500/15 text-rose-400 border border-rose-500/30 flex items-center space-x-1">
                <AlertTriangle className="w-3 h-3" />
                <span>RISK SCORE: 76/100 (CRITICAL)</span>
              </span>
              <span className="text-[11px] font-mono text-slate-400 px-2 py-1 rounded bg-slate-800/80">
                TA·HI·EN
              </span>
            </div>
          </div>

          {/* Interactive Inspection Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6 mt-6">
            {/* Finding 1 */}
            <div className="p-4 rounded-xl bg-obsidian-900/90 border border-rose-500/30 space-y-2.5">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-bold text-rose-400 uppercase tracking-wider">False Urgency</span>
                <span className="text-[10px] font-mono text-slate-400 bg-slate-800 px-1.5 py-0.5 rounded">Clause 5(a)</span>
              </div>
              <p className="text-xs text-slate-200 font-medium italic bg-rose-950/20 p-2 rounded border border-rose-900/30">
                "விரையுங்கள்! 03 நிமிடங்களில் ஆஃபர் முடிகிறது! (Hurry! Offer expires in 3 mins!)"
              </p>
              <p className="text-[11px] text-slate-400">
                Fabricates artificial time pressure without real inventory constraint.
              </p>
            </div>

            {/* Finding 2 */}
            <div className="p-4 rounded-xl bg-obsidian-900/90 border border-amber-500/30 space-y-2.5">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-bold text-amber-400 uppercase tracking-wider">Confirm Shaming</span>
                <span className="text-[10px] font-mono text-slate-400 bg-slate-800 px-1.5 py-0.5 rounded">Clause 5(c)</span>
              </div>
              <p className="text-xs text-slate-200 font-medium italic bg-amber-950/20 p-2 rounded border border-amber-900/30">
                "No, I hate saving money and prefer paying full price"
              </p>
              <p className="text-[11px] text-slate-400">
                Emotionally manipulates consumer when declining membership upsell.
              </p>
            </div>

            {/* Finding 3 */}
            <div className="p-4 rounded-xl bg-obsidian-900/90 border border-cyber-cyan/30 space-y-2.5">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-bold text-cyber-cyan uppercase tracking-wider">Drip Pricing</span>
                <span className="text-[10px] font-mono text-slate-400 bg-slate-800 px-1.5 py-0.5 rounded">Clause 5(h)</span>
              </div>
              <p className="text-xs text-slate-200 font-medium italic bg-cyan-950/20 p-2 rounded border border-cyan-900/30">
                "अतिरिक्त पैकेजिंग और हैंडलिंग शुल्क ₹99 (Hidden Packaging Fee ₹99)"
              </p>
              <p className="text-[11px] text-slate-400">
                Essential transaction charges hidden until the final payment step.
              </p>
            </div>
          </div>

          {/* Autonomous Remediation Banner */}
          <div className="mt-6 p-4 rounded-xl bg-gradient-to-r from-cyber-emerald/15 via-slate-900/80 to-cyber-cyan/15 border border-cyber-emerald/30 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center space-x-3">
              <div className="p-2 rounded-lg bg-cyber-emerald/20 text-cyber-emerald">
                <Zap className="w-5 h-5" />
              </div>
              <div>
                <h4 className="text-xs font-bold text-white">Closed-Loop Remediation Engine</h4>
                <p className="text-[11px] text-slate-300">
                  Rewrites deceptive copy into CCPA-compliant phrasing and re-evaluates risk reduction.
                </p>
              </div>
            </div>
            <button 
              onClick={onStartScan}
              className="px-4 py-2 rounded-lg bg-cyber-emerald text-obsidian-950 font-bold text-xs hover:bg-emerald-400 transition-colors shadow-glow-emerald cursor-pointer shrink-0"
            >
              Test Live Remediation
            </button>
          </div>
        </div>

        {/* 13 CCPA 2023 Dark Pattern Matrix */}
        <div className="mt-20">
          <div className="text-center max-w-2xl mx-auto space-y-2">
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              India CCPA Guidelines 2023 Reference Matrix
            </h2>
            <p className="text-xs sm:text-sm text-slate-400">
              The Central Consumer Protection Authority notified guidelines defining 13 deceptive practices prohibited on digital platforms.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 mt-8">
            {ccpaGuidelines.map((item, idx) => (
              <div 
                key={idx}
                className="cyber-glass-card p-4 rounded-xl space-y-2 group hover:border-cyber-cyan/50 transition-all"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-white group-hover:text-cyber-cyan transition-colors">
                    {idx + 1}. {item.title}
                  </span>
                  <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${
                    item.severity === 'Critical' ? 'bg-rose-500/20 text-rose-400' :
                    item.severity === 'High' ? 'bg-amber-500/20 text-amber-400' :
                    'bg-slate-800 text-slate-400'
                  }`}>
                    {item.severity}
                  </span>
                </div>
                <p className="text-[11px] text-slate-400 leading-relaxed">
                  {item.desc}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Feature Highlights Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16">
          <div className="cyber-glass-card p-6 rounded-2xl">
            <div className="p-3 bg-cyber-cyan/15 text-cyber-cyan rounded-xl w-fit mb-4 border border-cyber-cyan/30">
              <Globe className="w-6 h-6" />
            </div>
            <h3 className="text-sm font-bold text-white mb-1.5">Multilingual NLP Classifier</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Trained detection rules and TF-IDF/IndicBERT models for English, Hindi, and Tamil e-commerce copy.
            </p>
          </div>

          <div className="cyber-glass-card p-6 rounded-2xl">
            <div className="p-3 bg-brand-500/15 text-brand-400 rounded-xl w-fit mb-4 border border-brand-500/30">
              <Scale className="w-6 h-6" />
            </div>
            <h3 className="text-sm font-bold text-white mb-1.5">Learned Combined-Risk Score</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              0–100 calibrated risk index factoring category severity, co-occurrence multipliers, and page context.
            </p>
          </div>

          <div className="cyber-glass-card p-6 rounded-2xl">
            <div className="p-3 bg-cyber-emerald/15 text-cyber-emerald rounded-xl w-fit mb-4 border border-cyber-emerald/30">
              <FileCheck2 className="w-6 h-6" />
            </div>
            <h3 className="text-sm font-bold text-white mb-1.5">Enterprise Audit Reports</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              One-click export of verified scan dossiers into ReportLab PDF, CSV, and JSON with legal citations.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 bg-obsidian-950/80 px-4 sm:px-6 lg:px-8 py-6">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between text-xs text-slate-400 gap-3">
          <div>
            <span className="font-bold text-slate-200">DarkPattern AI</span> — Major Project Final Year Viva Submission
          </div>
          <div className="text-center sm:text-right text-[11px] text-slate-400">
            CCPA Guidelines 2023 • Academic Decision-Support System (Not definitive legal advice)
          </div>
        </div>
      </footer>
    </div>
  );
};
