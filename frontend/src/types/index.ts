export interface Finding {
  id: string;
  scan_id: string;
  category: string;
  severity: 'Low' | 'Medium' | 'High' | 'Critical';
  confidence: number;
  text_snippet: string;
  dom_selector?: string;
  rationale: string;
  consumer_impact: string;
  ccpa_clause: string;
  ccpa_category: string;
  recommendation: string;
  is_reviewed: boolean;
}

export interface Scan {
  id: string;
  url?: string;
  scan_type: 'text' | 'url';
  language: string;
  status: 'completed' | 'partially_scanned' | 'insufficient_content' | 'failed' | string;
  risk_score: number;
  risk_category: 'Low Risk' | 'Moderate Risk' | 'High Risk' | 'Critical Risk';
  findings_count: number;
  created_at: string;
  fetch_method?: string;
  content_length_analyzed?: number;
  page_title?: string;
  warnings?: string[];
  findings?: Finding[];
}

export interface CCPAData {
  category_code: string;
  category_name: string;
  clause_reference: string;
  plain_explanation: string;
  problematic_examples: string[];
  compliant_alternative: string;
  official_url: string;
  last_reviewed: string;
}

export interface RemediationResult {
  id: string;
  finding_id: string;
  original_text: string;
  proposed_text: string;
  rationale: string;
  before_risk: number;
  after_risk: number;
  status: string;
  is_verified: boolean;
  risk_drop: number;
}

export interface AnalyticsOverview {
  total_scans: number;
  total_findings: number;
  high_risk_pages_count: number;
  avg_risk_score: number;
  category_distribution: Record<string, number>;
  severity_distribution: Record<string, number>;
  language_distribution: Record<string, number>;
  recent_scans: Array<{
    id: string;
    url: string;
    risk_score: number;
    risk_category: string;
    findings_count: number;
    created_at: string;
  }>;
}
