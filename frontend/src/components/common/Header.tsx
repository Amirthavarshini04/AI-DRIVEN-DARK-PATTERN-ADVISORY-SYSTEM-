import React from 'react';
import { Menu, Sparkles, Globe, ShieldCheck } from 'lucide-react';

interface HeaderProps {
  title: string;
  subtitle?: string;
  onQuickScan?: () => void;
  onToggleMobileMenu?: () => void;
}

export const Header: React.FC<HeaderProps> = ({ 
  title, 
  subtitle, 
  onQuickScan, 
  onToggleMobileMenu 
}) => {
  return (
    <header className="sticky top-0 z-30 bg-obsidian-900/80 backdrop-blur-xl border-b border-slate-800/80 px-4 sm:px-6 lg:px-8 py-3.5 flex items-center justify-between transition-colors">
      {/* Left: Mobile Hamburger & Page Title */}
      <div className="flex items-center space-x-3.5 min-w-0">
        {onToggleMobileMenu && (
          <button
            onClick={onToggleMobileMenu}
            className="lg:hidden p-2 rounded-xl bg-slate-800/60 border border-slate-700/60 text-slate-300 hover:text-white hover:bg-slate-700/60 transition-colors"
            aria-label="Open navigation menu"
          >
            <Menu className="w-5 h-5" />
          </button>
        )}

        <div className="min-w-0">
          <h1 className="text-base sm:text-lg font-bold text-white tracking-tight truncate flex items-center space-x-2">
            <span>{title}</span>
          </h1>
          {subtitle && (
            <p className="text-[11px] sm:text-xs text-slate-400 truncate mt-0.5">
              {subtitle}
            </p>
          )}
        </div>
      </div>

      {/* Right: Live Sentinel Status & Quick Scan */}
      <div className="flex items-center space-x-2.5 sm:space-x-3 shrink-0">
        {/* CCPA 2023 Live Status */}
        <span className="hidden md:inline-flex items-center space-x-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-cyber-emerald/10 text-cyber-emerald border border-cyber-emerald/30 shadow-xs">
          <span className="w-2 h-2 rounded-full bg-cyber-emerald animate-pulse"></span>
          <span>CCPA 2023 Active</span>
        </span>

        {/* Indic Languages Badge */}
        <span className="inline-flex items-center space-x-1 px-2.5 py-1 rounded-lg text-[11px] sm:text-xs font-medium bg-slate-800/70 text-slate-300 border border-slate-700/60">
          <Globe className="w-3.5 h-3.5 text-cyber-cyan" />
          <span className="hidden sm:inline">EN • हिंदी • தமிழ்</span>
          <span className="sm:hidden">EN·HI·TA</span>
        </span>

        {/* New Scan CTA */}
        {onQuickScan && (
          <button
            onClick={onQuickScan}
            className="flex items-center space-x-1.5 bg-gradient-to-r from-cyber-cyan to-brand-600 hover:from-cyan-400 hover:to-indigo-500 text-white text-xs font-bold px-3.5 sm:px-4 py-1.5 sm:py-2 rounded-xl transition-all shadow-glow-cyan hover:scale-[1.02] active:scale-[0.98] cursor-pointer"
          >
            <Sparkles className="w-3.5 h-3.5 animate-pulse" />
            <span className="hidden xs:inline">Run Scan</span>
            <span className="xs:hidden">Scan</span>
          </button>
        )}
      </div>
    </header>
  );
};
