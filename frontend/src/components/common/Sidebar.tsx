import React from 'react';
import { 
  ShieldAlert, 
  LayoutDashboard, 
  Search, 
  BookOpen, 
  BarChart3, 
  Wrench, 
  History, 
  FileText,
  Home,
  X,
  Radio,
  Cpu
} from 'lucide-react';

interface SidebarProps {
  currentPage: string;
  onNavigate: (page: string) => void;
  mobileOpen?: boolean;
  onCloseMobile?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ 
  currentPage, 
  onNavigate, 
  mobileOpen = false, 
  onCloseMobile 
}) => {
  const navItems = [
    { id: 'landing', label: 'Telemetry Overview', icon: Home, tag: 'LIVE' },
    { id: 'dashboard', label: 'Compliance Dashboard', icon: LayoutDashboard },
    { id: 'scan', label: 'Scan Website / Text', icon: Search, badge: 'EN·HI·TA' },
    { id: 'compliance', label: 'CCPA 2023 Library', icon: BookOpen, badge: '13 Rules' },
    { id: 'analytics', label: 'Risk Analytics', icon: BarChart3 },
    { id: 'remediation', label: 'Remediation Engine', icon: Wrench, tag: 'AI' },
    { id: 'history', label: 'Scan History', icon: History },
    { id: 'reports', label: 'Audit Reports', icon: FileText },
  ];

  const handleNavClick = (id: string) => {
    onNavigate(id);
    if (onCloseMobile) {
      onCloseMobile();
    }
  };

  return (
    <>
      {/* Mobile Backdrop Overlay */}
      {mobileOpen && (
        <div 
          onClick={onCloseMobile}
          className="fixed inset-0 bg-black/80 backdrop-blur-sm z-40 lg:hidden transition-opacity duration-300"
          aria-hidden="true"
        />
      )}

      {/* Sidebar Container */}
      <aside 
        className={`fixed lg:sticky top-0 inset-y-0 left-0 z-50 w-72 lg:w-64 h-screen flex flex-col 
          bg-obsidian-900/95 lg:bg-obsidian-900/80 backdrop-blur-2xl border-r border-slate-800/80 
          transform transition-transform duration-300 ease-in-out shrink-0
          ${mobileOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
        `}
      >
        {/* Brand Header */}
        <div className="p-5 border-b border-slate-800/80 flex items-center justify-between">
          <div 
            className="flex items-center space-x-3 cursor-pointer group" 
            onClick={() => handleNavClick('dashboard')}
          >
            <div className="relative p-2.5 bg-gradient-to-br from-cyber-cyan/20 to-cyber-emerald/20 border border-cyber-cyan/40 rounded-xl text-cyber-cyan shadow-glow-cyan group-hover:scale-105 transition-transform">
              <ShieldAlert className="w-5 h-5 text-cyber-cyan" />
              <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-cyber-emerald rounded-full animate-ping"></span>
            </div>
            <div>
              <div className="flex items-center space-x-1.5">
                <span className="font-extrabold text-white text-sm tracking-tight">DarkPattern</span>
                <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-cyber-cyan/15 text-cyber-cyan border border-cyber-cyan/30">AI</span>
              </div>
              <p className="text-[11px] text-slate-400 font-medium">CCPA 2023 Sentinel</p>
            </div>
          </div>

          {/* Mobile Close Button */}
          {onCloseMobile && (
            <button
              onClick={onCloseMobile}
              className="lg:hidden p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/80 transition-colors"
              aria-label="Close menu"
            >
              <X className="w-5 h-5" />
            </button>
          )}
        </div>

        {/* Live Engine Telemetry Pill */}
        <div className="mx-4 mt-4 p-3 rounded-xl bg-obsidian-850/80 border border-slate-800/80 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Radio className="w-3.5 h-3.5 text-cyber-emerald animate-pulse" />
            <span className="text-[11px] font-medium text-slate-300">Detection Engine</span>
          </div>
          <span className="text-[10px] font-bold text-cyber-emerald bg-cyber-emerald/10 px-2 py-0.5 rounded-full border border-cyber-emerald/30">
            ONLINE
          </span>
        </div>

        {/* Navigation List */}
        <nav className="flex-1 px-3 py-4 space-y-1.5 overflow-y-auto">
          {navItems.map((item) => {
            const Icon = item.icon;
            const active = currentPage === item.id;
            return (
              <button
                key={item.id}
                onClick={() => handleNavClick(item.id)}
                className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all duration-200 group ${
                  active 
                    ? 'bg-gradient-to-r from-cyber-cyan/20 to-transparent text-cyber-cyan border-l-2 border-cyber-cyan shadow-sm shadow-cyan-500/10' 
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
                }`}
              >
                <div className="flex items-center space-x-3 min-w-0">
                  <Icon className={`w-4 h-4 shrink-0 transition-transform group-hover:scale-110 ${
                    active ? 'text-cyber-cyan' : 'text-slate-400 group-hover:text-slate-200'
                  }`} />
                  <span className="truncate">{item.label}</span>
                </div>
                {item.tag && (
                  <span className="text-[9px] font-bold px-1.5 py-0.2 rounded bg-purple-500/20 text-purple-300 border border-purple-500/30">
                    {item.tag}
                  </span>
                )}
                {item.badge && (
                  <span className="text-[9px] font-medium px-1.5 py-0.2 rounded bg-slate-800 text-slate-400 border border-slate-700/50">
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>

        {/* Footer Hardware & Viva Badge */}
        <div className="p-4 border-t border-slate-800/80 bg-obsidian-950/60">
          <div className="flex items-center justify-between text-[11px] text-slate-400">
            <span className="flex items-center space-x-1.5">
              <Cpu className="w-3.5 h-3.5 text-cyber-cyan" />
              <span>Multi-lingual NLP</span>
            </span>
            <span className="text-[10px] font-mono text-slate-400">v2.4-IND</span>
          </div>
          <p className="mt-1.5 text-[10px] text-slate-400">
            Final Year Major Project • CCPA 2023
          </p>
        </div>
      </aside>
    </>
  );
};
