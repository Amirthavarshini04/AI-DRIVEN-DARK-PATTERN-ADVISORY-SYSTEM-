import { Scan, CCPAData, RemediationResult, AnalyticsOverview } from '../types';

const API_BASE = 'http://127.0.0.1:8000/api/v1';

export async function scanText(text: string, language: string = 'auto'): Promise<Scan> {
  const res = await fetch(`${API_BASE}/scans/text`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, language }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Failed to analyze text snippet');
  }
  return res.json();
}

export async function scanUrl(url: string, language: string = 'auto'): Promise<Scan> {
  const res = await fetch(`${API_BASE}/scans/url`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url, language }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Failed to scan website URL');
  }
  return res.json();
}

export async function getScans(query?: string): Promise<{ total: number; items: Scan[] }> {
  const q = query ? `?query=${encodeURIComponent(query)}` : '';
  const res = await fetch(`${API_BASE}/scans${q}`);
  if (!res.ok) throw new Error('Failed to fetch scans');
  return res.json();
}

export async function getScanById(scanId: string): Promise<Scan> {
  const res = await fetch(`${API_BASE}/scans/${scanId}`);
  if (!res.ok) throw new Error('Failed to fetch scan detail');
  return res.json();
}

export async function deleteScan(scanId: string): Promise<void> {
  const res = await fetch(`${API_BASE}/scans/${scanId}`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Failed to delete scan');
}

export async function getCCPAData(): Promise<CCPAData[]> {
  const res = await fetch(`${API_BASE}/compliance/guidelines`);
  if (!res.ok) throw new Error('Failed to fetch CCPA guidelines');
  return res.json();
}

export async function getAnalytics(): Promise<AnalyticsOverview> {
  const res = await fetch(`${API_BASE}/analytics/overview`);
  if (!res.ok) throw new Error('Failed to fetch analytics');
  return res.json();
}

export async function generateRemediation(findingId: string): Promise<RemediationResult> {
  const res = await fetch(`${API_BASE}/remediation/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ finding_id: findingId }),
  });
  if (!res.ok) throw new Error('Failed to generate remediation');
  return res.json();
}

export async function verifyCustomRemediation(findingId: string, proposedText: string): Promise<RemediationResult> {
  const res = await fetch(`${API_BASE}/remediation/verify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ finding_id: findingId, proposed_text: proposedText }),
  });
  if (!res.ok) throw new Error('Failed to verify remediation');
  return res.json();
}

export async function submitFeedback(findingId: string, isFalsePositive: boolean, comment?: string): Promise<void> {
  await fetch(`${API_BASE}/findings/${findingId}/feedback`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ is_false_positive: isFalsePositive, comment }),
  });
}
