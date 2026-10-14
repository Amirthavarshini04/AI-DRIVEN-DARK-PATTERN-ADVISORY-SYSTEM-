import React, { useState } from 'react';
import { Sidebar } from './components/common/Sidebar';
import { Header } from './components/common/Header';

import { LandingPage } from './pages/LandingPage';
import { DashboardPage } from './pages/DashboardPage';
import { ScanPage } from './pages/ScanPage';
import { ResultsPage } from './pages/ResultsPage';
import { CompliancePage } from './pages/CompliancePage';
import { RiskAnalyticsPage } from './pages/RiskAnalyticsPage';
import { RemediationPage } from './pages/RemediationPage';
import { HistoryPage } from './pages/HistoryPage';
import { ReportsPage } from './pages/ReportsPage';

export function App() {
  const [currentPage, setCurrentPage] = useState<string>('landing');
  const [selectedScanId, setSelectedScanId] = useState<string | null>(null);
  const [selectedFindingId, setSelectedFindingId] = useState<string | undefined>(undefined);
  const [mobileMenuOpen, setMobileMenuOpen] = useState<boolean>(false);

  const handleNavigate = (page: string, param?: string) => {
    setCurrentPage(page);
    setMobileMenuOpen(false);
    if (page === 'results' && param) {
      setSelectedScanId(param);
    }
    if (page === 'remediation' && param) {
      setSelectedFindingId(param);
    }
    // Scroll to top upon page navigation
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  if (currentPage === 'landing') {
    return (
      <LandingPage
        onStartScan={() => handleNavigate('scan')}
        onOpenDashboard={() => handleNavigate('dashboard')}
      />
    );
  }

  const getPageTitle = () => {
    switch (currentPage) {
      case 'dashboard': return 'Compliance Sentinel Overview';
      case 'scan': return 'Multi-lingual Threat Scanner';
      case 'results': return 'Scan Audit & Evidence Dossier';
      case 'compliance': return 'CCPA Guidelines 2023 Knowledge Base';
      case 'analytics': return 'Learned Risk Scoring & Co-occurrence';
      case 'remediation': return 'Autonomous Remediation & Verification';
      case 'history': return 'Platform Audit History';
      case 'reports': return 'Compliance Export Engine (PDF / CSV / JSON)';
      default: return 'Compliance Advisory System';
    }
  };

  return (
    <div className="flex min-h-screen bg-obsidian-950 text-slate-100 cyber-mesh-bg antialiased selection:bg-cyber-cyan selection:text-obsidian-950">
      {/* Responsive Sidebar (Persistent Desktop, Off-canvas Mobile/Tablet) */}
      <Sidebar 
        currentPage={currentPage} 
        onNavigate={handleNavigate}
        mobileOpen={mobileMenuOpen}
        onCloseMobile={() => setMobileMenuOpen(false)}
      />

      {/* Main Content Viewport */}
      <div className="flex-1 flex flex-col min-w-0">
        <Header
          title={getPageTitle()}
          subtitle="Indian E-Commerce Compliance Advisory System • CCPA Guidelines 2023"
          onQuickScan={() => handleNavigate('scan')}
          onToggleMobileMenu={() => setMobileMenuOpen(prev => !prev)}
        />

        <main className="flex-1 overflow-y-auto w-full">
          {currentPage === 'dashboard' && <DashboardPage onNavigate={handleNavigate} />}
          {currentPage === 'scan' && (
            <ScanPage 
              onScanComplete={(scanId) => {
                setSelectedScanId(scanId);
                handleNavigate('results', scanId);
              }} 
            />
          )}
          {currentPage === 'results' && selectedScanId && (
            <ResultsPage scanId={selectedScanId} onNavigate={handleNavigate} />
          )}
          {currentPage === 'compliance' && <CompliancePage />}
          {currentPage === 'analytics' && <RiskAnalyticsPage />}
          {currentPage === 'remediation' && (
            <RemediationPage findingId={selectedFindingId} onNavigate={handleNavigate} />
          )}
          {currentPage === 'history' && <HistoryPage onNavigate={handleNavigate} />}
          {currentPage === 'reports' && <ReportsPage />}
        </main>
      </div>
    </div>
  );
}

export default App;
