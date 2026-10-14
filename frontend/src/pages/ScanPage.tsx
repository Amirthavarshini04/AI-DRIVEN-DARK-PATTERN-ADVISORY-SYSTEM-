import React, { useState } from 'react';
import { 
  Search, 
  Globe, 
  FileText, 
  Sparkles, 
  AlertCircle, 
  CheckCircle, 
  Loader2,
  Radio,
  ShieldCheck,
  Zap,
  Layers,
  Terminal,
  Activity
} from 'lucide-react';
import { scanText, scanUrl } from '../services/api';

interface ScanPageProps {
  onScanComplete: (scanId: string) => void;
}

export const ScanPage: React.FC<ScanPageProps> = ({ onScanComplete }) => {
  const [scanMode, setScanMode] = useState<'url' | 'text'>('url');
  const [urlInput, setUrlInput] = useState('https://books.toscrape.com');
  const [textInput, setTextInput] = useState('Hurry! Only 2 items left in stock - Offer expires in 04m 12s!');
  const [language, setLanguage] = useState('auto');
  const [isScanning, setIsScanning] = useState(false);
  const [currentStep, setCurrentStep] = useState<string | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const sampleUrls = [
    {
      label: 'Sample Store: Books Catalog',
      url: 'https://books.toscrape.com',
    },
    {
      label: 'Demonstrate SSRF Protection (Blocked)',
      url: 'http://169.254.169.254/latest/meta-data/',
    },
    {
      label: 'Demonstrate Localhost Block (Protected)',
      url: 'http://127.0.0.1:8000/api/v1/health',
    }
  ];

  const sampleSnippets = [
    {
      lang: 'en',
      label: 'English: False Urgency',
      text: 'Hurry! Only 2 items left in stock - Deal expires in 04m 12s! 45 other people are looking at this.',
    },
    {
      lang: 'ta',
      label: 'Tamil (தமிழ்): False Urgency',
      text: 'விரையுங்கள்! இன்னும் 2 பொருட்கள் மட்டுமே உள்ளன - சலுகை 03 நிமிடங்களில் முடிகிறது! இப்போதே முன்பதிவு செய்யுங்கள்.',
    },
    {
      lang: 'hi',
      label: 'Hindi (हिंदी): Drip Pricing',
      text: 'अंतिम चेकआउट मूल्य में अतिरिक्त सुविधा शुल्क ₹99 और अनिवार्य पैकेजिंग शुल्क ₹49 जोड़ा गया है।',
    },
    {
      lang: 'en',
      label: 'English: Confirm Shaming',
      text: 'No thanks, I hate saving money and prefer paying full price for this product.',
    },
    {
      lang: 'en',
      label: 'English: Basket Sneaking',
      text: 'Order summary: Premium device protection plan included automatically for ₹299. Pre-checked insurance added.',
    }
  ];

  const handleRunScan = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);
    setIsScanning(true);

    try {
      let result;
      if (scanMode === 'url') {
        setCurrentStep('Validating Target URL & SSRF Protocol Security...');
        await new Promise(r => setTimeout(r, 300));
        setCurrentStep('Rendering Dynamic DOM via Headless Chromium & Extracting Elements...');
        result = await scanUrl(urlInput, language);
      } else {
        setCurrentStep('Executing Multilingual Classifier (IndicBERT / NLP Engine)...');
        await new Promise(r => setTimeout(r, 300));
        setCurrentStep('Evaluating CCPA 2023 Guidelines & Computing Combined-Risk Score...');
        result = await scanText(textInput, language);
      }

      setIsScanning(false);
      onScanComplete(result.id);
    } catch (err: any) {
      setIsScanning(false);
      setErrorMsg(err.message || 'Scan failed. Check backend connection or URL.');
    }
  };

  const applySample = (sample: typeof sampleSnippets[0]) => {
    setScanMode('text');
    setTextInput(sample.text);
    setLanguage(sample.lang);
  };

  const applyUrlSample = (sample: typeof sampleUrls[0]) => {
    setScanMode('url');
    setUrlInput(sample.url);
  };

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 sm:space-y-8 max-w-7xl mx-auto w-full">
      {/* Top Section Banner */}
      <div className="cyber-glass-card p-5 sm:p-6 rounded-2xl border border-cyber-cyan/30 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <Radio className="w-4 h-4 text-cyber-cyan animate-pulse" />
            <span className="text-[11px] font-bold uppercase tracking-wider text-cyber-cyan">Sentinel Inspector</span>
          </div>
          <h2 className="text-xl sm:text-2xl font-extrabold text-white tracking-tight mt-1">
            Multilingual Threat & Compliance Scanner
          </h2>
          <p className="text-xs text-slate-300 mt-1 max-w-2xl leading-relaxed">
            Analyze Indian e-commerce web URLs or paste checkout DOM snippets in English, Tamil, and Hindi under CCPA Guidelines 2023.
          </p>
        </div>

        <div className="flex items-center space-x-2 bg-obsidian-900/90 border border-slate-700/80 px-3 py-1.5 rounded-xl text-xs font-mono text-slate-300">
          <ShieldCheck className="w-4 h-4 text-cyber-emerald" />
          <span>SSRF Guard: ACTIVE</span>
        </div>
      </div>

      {/* Main Grid: Form Left, Radar Telemetry Right */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Form (7 cols on lg) */}
        <div className="lg:col-span-7 cyber-glass-card p-5 sm:p-7 rounded-2xl space-y-6">
          {/* Scan Mode Toggle Tabs */}
          <div className="flex border-b border-slate-800/80 gap-4">
            <button
              type="button"
              onClick={() => setScanMode('url')}
              className={`pb-3 text-xs font-bold border-b-2 flex items-center space-x-2 transition-all cursor-pointer ${
                scanMode === 'url'
                  ? 'border-cyber-cyan text-cyber-cyan'
                  : 'border-transparent text-slate-400 hover:text-slate-200'
              }`}
            >
              <Globe className="w-4 h-4" />
              <span>Web Page URL Analysis</span>
            </button>

            <button
              type="button"
              onClick={() => setScanMode('text')}
              className={`pb-3 text-xs font-bold border-b-2 flex items-center space-x-2 transition-all cursor-pointer ${
                scanMode === 'text'
                  ? 'border-cyber-cyan text-cyber-cyan'
                  : 'border-transparent text-slate-400 hover:text-slate-200'
              }`}
            >
              <FileText className="w-4 h-4" />
              <span>Direct Text / DOM Snippet</span>
            </button>
          </div>

          {/* Form */}
          <form onSubmit={handleRunScan} className="space-y-5">
            {scanMode === 'url' ? (
              <div className="space-y-1.5">
                <label className="block text-xs font-bold text-slate-300">
                  Target E-Commerce URL (Protected against SSRF & Metadata Exploits)
                </label>
                <div className="relative">
                  <input
                    type="url"
                    required
                    value={urlInput}
                    onChange={(e) => setUrlInput(e.target.value)}
                    placeholder="https://example-ecommerce-india.in/product/123"
                    className="w-full px-4 py-3 text-xs bg-obsidian-900/90 text-white border border-slate-700/80 rounded-xl focus:border-cyber-cyan focus:ring-1 focus:ring-cyber-cyan focus:outline-none transition-colors font-mono"
                  />
                </div>
                <p className="text-[11px] text-slate-400">
                  Localhost, private subnets (RFC 1918), AWS metadata endpoints (169.254.169.254) are strictly blocked.
                </p>
              </div>
            ) : (
              <div className="space-y-1.5">
                <label className="block text-xs font-bold text-slate-300">
                  Pasted Page Content / UI Snippet (English, Hindi, Tamil)
                </label>
                <textarea
                  rows={5}
                  required
                  value={textInput}
                  onChange={(e) => setTextInput(e.target.value)}
                  placeholder="Paste text snippets from shopping cart, discount modals, countdown banners..."
                  className="w-full px-4 py-3 text-xs bg-obsidian-900/90 text-white border border-slate-700/80 rounded-xl focus:border-cyber-cyan focus:ring-1 focus:ring-cyber-cyan focus:outline-none transition-colors leading-relaxed"
                />
              </div>
            )}

            {/* Quick Test Demo Chips */}
            <div className="space-y-2 pt-1">
              <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider flex items-center space-x-1">
                <Zap className="w-3.5 h-3.5 text-cyber-cyan" />
                <span>Quick Test Samples (Viva & Demonstration):</span>
              </span>
              <div className="flex flex-wrap gap-2">
                {scanMode === 'url' ? (
                  sampleUrls.map((s, idx) => (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => applyUrlSample(s)}
                      className="text-[11px] px-2.5 py-1.5 rounded-lg bg-obsidian-850/90 hover:bg-slate-800 text-slate-300 hover:text-white border border-slate-700/80 hover:border-cyber-cyan/50 transition-all cursor-pointer text-left"
                    >
                      {s.label}
                    </button>
                  ))
                ) : (
                  sampleSnippets.map((s, idx) => (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => applySample(s)}
                      className="text-[11px] px-2.5 py-1.5 rounded-lg bg-obsidian-850/90 hover:bg-slate-800 text-slate-300 hover:text-white border border-slate-700/80 hover:border-cyber-cyan/50 transition-all cursor-pointer text-left"
                    >
                      {s.label}
                    </button>
                  ))
                )}
              </div>
            </div>

            {/* Language Selector */}
            <div className="space-y-1.5">
              <label className="block text-xs font-bold text-slate-300">
                Language Analysis Engine
              </label>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="w-full sm:w-auto px-4 py-2.5 text-xs bg-obsidian-900/90 text-white border border-slate-700/80 rounded-xl focus:border-cyber-cyan focus:outline-none font-medium cursor-pointer"
              >
                <option value="auto">Auto-Detect Language (Recommended)</option>
                <option value="en">English (en)</option>
                <option value="hi">Hindi - हिंदी (hi)</option>
                <option value="ta">Tamil - தமிழ் (ta)</option>
              </select>
            </div>

            {errorMsg && (
              <div className="p-3 bg-rose-500/15 border border-rose-500/40 text-rose-300 rounded-xl text-xs flex items-center space-x-2">
                <AlertCircle className="w-4 h-4 shrink-0 text-rose-400" />
                <span>{errorMsg}</span>
              </div>
            )}

            <button
              type="submit"
              disabled={isScanning}
              className="w-full bg-gradient-to-r from-cyber-cyan to-brand-600 hover:from-cyan-400 hover:to-indigo-500 text-white font-bold text-xs py-3.5 rounded-xl shadow-glow-cyan flex items-center justify-center space-x-2 transition-all cursor-pointer disabled:opacity-50 hover:scale-[1.01]"
            >
              <Sparkles className="w-4 h-4" />
              <span>{isScanning ? 'Executing Multilingual Scan...' : 'Analyze Dark Pattern Compliance'}</span>
            </button>
          </form>
        </div>

        {/* Right Radar Telemetry HUD (5 cols on lg) */}
        <div className="lg:col-span-5 cyber-glass-card p-5 sm:p-7 rounded-2xl flex flex-col justify-between space-y-6">
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-white tracking-tight flex items-center space-x-2">
                <Activity className="w-4 h-4 text-cyber-cyan" />
                <span>Sentinel Scanning Radar</span>
              </h3>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-cyber-emerald border border-slate-700">
                ACTIVE
              </span>
            </div>
            <p className="text-[11px] text-slate-400">
              Live inspection stream monitoring DOM hierarchy and classifying deceptive patterns against CCPA 2023.
            </p>
          </div>

          {/* Animated Radar Visualizer */}
          <div className="relative my-4 flex items-center justify-center h-48 sm:h-56">
            {/* Outer Ring */}
            <div className="w-44 h-44 sm:w-52 sm:h-52 rounded-full border border-cyber-cyan/30 relative flex items-center justify-center">
              {/* Inner Ring */}
              <div className="w-32 h-32 sm:w-36 sm:h-36 rounded-full border border-slate-700/60 flex items-center justify-center">
                {/* Core */}
                <div className="w-16 h-16 sm:w-20 sm:h-20 rounded-full bg-cyber-cyan/10 border border-cyber-cyan/50 flex items-center justify-center">
                  <Radio className={`w-6 h-6 text-cyber-cyan ${isScanning ? 'animate-pulse' : ''}`} />
                </div>
              </div>

              {/* Crosshairs */}
              <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                <div className="w-full h-[1px] bg-cyber-cyan/20"></div>
              </div>
              <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                <div className="h-full w-[1px] bg-cyber-cyan/20"></div>
              </div>

              {/* Rotating Sweep Beam when Scanning */}
              {isScanning && (
                <div className="absolute inset-0 rounded-full animate-radar-sweep pointer-events-none bg-gradient-to-tr from-transparent via-cyber-cyan/25 to-transparent"></div>
              )}
            </div>
          </div>

          {/* Live Progress or Status Checklist */}
          {isScanning ? (
            <div className="p-4 rounded-xl bg-obsidian-900/90 border border-cyber-cyan/40 space-y-2">
              <div className="flex items-center space-x-2 text-xs font-bold text-cyber-cyan">
                <Loader2 className="w-4 h-4 animate-spin text-cyber-cyan" />
                <span>Scan In Progress...</span>
              </div>
              <p className="text-[11px] text-slate-300 font-mono">{currentStep}</p>
            </div>
          ) : (
            <div className="p-4 rounded-xl bg-obsidian-900/70 border border-slate-800/80 space-y-2.5">
              <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                Compliance Engine Specifications:
              </span>
              <ul className="text-[11px] text-slate-300 space-y-1.5 font-mono">
                <li className="flex items-center space-x-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-cyber-emerald"></span>
                  <span>13 CCPA 2023 Categories Supported</span>
                </li>
                <li className="flex items-center space-x-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-cyber-cyan"></span>
                  <span>Indic Multilingual Tokenizer (EN·HI·TA)</span>
                </li>
                <li className="flex items-center space-x-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-purple-400"></span>
                  <span>Learned Combined Risk Scoring (0–100)</span>
                </li>
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
