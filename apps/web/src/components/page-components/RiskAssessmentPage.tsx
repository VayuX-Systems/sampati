'use client';

import { useState } from 'react';
import { cn } from '@/lib/utils';
import {
  Shield,
  AlertTriangle,
  CheckCircle,
  TrendingDown,
  BarChart3,
  Calendar,
  Download
} from 'lucide-react';

interface RiskItem {
  id: string;
  name: string;
  description: string;
  framework: string;
  likelihood: 'low' | 'medium' | 'high';
  impact: 'low' | 'medium' | 'high';
  riskScore: number;
  status: 'mitigated' | 'accept' | 'treat' | 'transfer';
  owner: string;
  nextReview: Date;
  controlId?: string;
}

const RISK_ITEMS: RiskItem[] = [
  {
    id: 'R-001',
    name: 'Data Breach - Customer PII Exposure',
    description: 'Risk of unauthorized access to personally identifiable information',
    framework: 'ISO 27001',
    likelihood: 'medium',
    impact: 'high',
    riskScore: 15,
    status: 'mitigated',
    owner: 'Priya Sharma',
    nextReview: new Date('2026-11-28'),
    controlId: 'C-001'
  },
  {
    id: 'R-002',
    name: 'Third-Party Vendor Risk',
    description: 'Security vulnerabilities in vendor software and services',
    framework: 'SOC 2',
    likelihood: 'high',
    impact: 'high',
    riskScore: 20,
    status: 'treating',
    owner: 'Rajesh Kumar',
    nextReview: new Date('2026-12-05'),
    controlId: 'C-007'
  },
  {
    id: 'R-003',
    name: 'Regulatory Non-Compliance',
    description: 'Failure to comply with DPDP Act requirements',
    framework: 'DPDP',
    likelihood: 'high',
    impact: 'high',
    riskScore: 25,
    status: 'treat',
    owner: 'Vikram Singh',
    nextReview: new Date('2026-12-01'),
    controlId: 'C-010'
  },
  {
    id: 'R-004',
    name: 'Incident Response Gap',
    description: 'Insufficient incident detection and response capabilities',
    framework: 'ISO 27001',
    likelihood: 'medium',
    impact: 'medium',
    riskScore: 6,
    status: 'accept',
    owner: 'Ananya Patel',
    nextReview: new Date('2027-05-01'),
    controlId: 'C-004'
  },
  {
    id: 'R-005',
    name: 'Unauthorized Access',
    description: 'Privilege escalation and unauthorized system access',
    framework: 'SOC 2',
    likelihood: 'medium',
    impact: 'high',
    riskScore: 18,
    status: 'mitigated',
    owner: 'Meera Iyer',
    nextReview: new Date('2026-11-25'),
    controlId: 'C-003'
  },
  {
    id: 'R-006',
    name: 'Data Loss - Backup Failure',
    description: 'Loss of critical business data due to backup system failure',
    framework: 'DPDP',
    likelihood: 'low',
    impact: 'high',
    riskScore: 9,
    status: 'mitigated',
    owner: 'Karthik Rao',
    nextReview: new Date('2026-12-15'),
    controlId: 'C-010'
  }
];

const RISKS = ['All', 'Critical (15+)', 'High (10-14)', 'Medium (5-9)', 'Low (<5)'];
const STATUSES = ['All', 'Mitigated', 'Treating', 'Treat', 'Accept'];

function getRiskLevel(score: number): { level: 'critical' | 'high' | 'medium' | 'low'; color: string } {
  if (score >= 15) return { level: 'critical', color: 'text-red-600 bg-red-50 border-red-200' };
  if (score >= 10) return { level: 'high', color: 'text-amber-600 bg-amber-50 border-amber-200' };
  if (score >= 5) return { level: 'medium', color: 'text-blue-600 bg-blue-50 border-blue-200' };
  return { level: 'low', color: 'text-emerald-600 bg-emerald-50 border-emerald-200' };
}

function getLikelihoodColor(likelihood: string): string {
  switch (likelihood) {
    case 'high': return 'text-red-600';
    case 'medium': return 'text-amber-600';
    default: return 'text-emerald-600';
  }
}

function getImpactColor(impact: string): string {
  switch (impact) {
    case 'high': return 'text-red-600';
    case 'medium': return 'text-amber-600';
    default: return 'text-emerald-600';
  }
}

export function RiskAssessmentPage() {
  const [riskFilter, setRiskFilter] = useState('All');
  const [statusFilter, setStatusFilter] = useState('All');

  const filteredRisks = RISK_ITEMS.filter(risk => {
    const matchesRiskLevel = riskFilter === 'All' ||
      (riskFilter === 'Critical (15+)' && risk.riskScore >= 15) ||
      (riskFilter === 'High (10-14)' && risk.riskScore >= 10 && risk.riskScore < 15) ||
      (riskFilter === 'Medium (5-9)' && risk.riskScore >= 5 && risk.riskScore < 10) ||
      (riskFilter === 'Low (<5)' && risk.riskScore < 5);

    const matchesStatus = statusFilter === 'All' ||
      (statusFilter === 'Mitigated' && risk.status === 'mitigated') ||
      (statusFilter === 'Treating' && risk.status === 'treating') ||
      (statusFilter === 'Treat' && risk.status === 'treat') ||
      (statusFilter === 'Accept' && risk.status === 'accept');

    return matchesRiskLevel && matchesStatus;
  });

  const riskStats = {
    critical: RISK_ITEMS.filter(r => getRiskLevel(r.riskScore).level === 'critical').length,
    high: RISK_ITEMS.filter(r => getRiskLevel(r.riskScore).level === 'high').length,
    medium: RISK_ITEMS.filter(r => getRiskLevel(r.riskScore).level === 'medium').length,
    low: RISK_ITEMS.filter(r => getRiskLevel(r.riskScore).level === 'low').length
  };

  const avgRiskScore = Math.round(
    RISK_ITEMS.reduce((sum, r) => sum + r.riskScore, 0) / RISK_ITEMS.length
  );

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8 flex flex-col justify-between gap-4 sm:items-center sm:flex-row">
          <div>
            <h1 className="text-3xl font-bold text-slate-900">Risk Assessment</h1>
            <p className="mt-1 text-sm text-slate-600">
              Identify, assess, and manage compliance risks across frameworks
            </p>
          </div>
          <button className="inline-flex items-center gap-2 rounded-lg bg-primary-600 px-4 py-2 text-sm font-semibold text-white hover:bg-primary-700">
            <BarChart3 className="h-4 w-4" />
            <span>Generate Risk Report</span>
          </button>
        </div>

        {/* Risk Summary */}
        <div className="mb-8 grid grid-cols-1 gap-6 sm:grid-cols-4">
          <div className="rounded-lg border border-red-200 bg-red-50 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-red-700">Critical</p>
                <p className="text-3xl font-bold text-red-900">{riskStats.critical}</p>
              </div>
              <AlertTriangle className="h-8 w-8 text-red-600" />
            </div>
          </div>
          <div className="rounded-lg border border-amber-200 bg-amber-50 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-amber-700">High</p>
                <p className="text-3xl font-bold text-amber-900">{riskStats.high}</p>
              </div>
              <TrendingDown className="h-8 w-8 text-amber-600" />
            </div>
          </div>
          <div className="rounded-lg border border-blue-200 bg-blue-50 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-blue-700">Medium</p>
                <p className="text-3xl font-bold text-blue-900">{riskStats.medium}</p>
              </div>
              <Shield className="h-8 w-8 text-blue-600" />
            </div>
          </div>
          <div className="rounded-lg border border-emerald-200 bg-emerald-50 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-emerald-700">Low</p>
                <p className="text-3xl font-bold text-emerald-900">{riskStats.low}</p>
              </div>
              <CheckCircle className="h-8 w-8 text-emerald-600" />
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="mb-6 flex items-center gap-3">
          <div className="flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-3 py-2">
            <Shield className="h-4 w-4 text-slate-400" />
            <span className="text-sm font-medium text-slate-700">Filter by:</span>
          </div>
          <select
            value={riskFilter}
            onChange={(e) => setRiskFilter(e.target.value)}
            className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
          >
            {RISKS.map(r => <option key={r} value={r}>{r}</option>)}
          </select>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
          >
            {STATUSES.map(s => <option key={s} value={s}>{s}</option>)}
          </select>
        </div>

        {/* Risk Items */}
        <div className="space-y-4">
          {filteredRisks.map((risk) => {
            const riskInfo = getRiskLevel(risk.riskScore);
            return (
              <div
                key={risk.id}
                className={cn(
                  "rounded-lg border p-4 sm:p-6",
                  riskInfo.color
                )}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <span className={cn("text-xs font-medium", riskInfo.color.replace('bg-', 'text-'))}>
                        Risk Score: {risk.riskScore}
                      </span>
                      <span className="text-xs text-slate-500">
                        {risk.framework}
                      </span>
                    </div>
                    <h3 className="text-lg font-semibold text-slate-900 mb-2">{risk.name}</h3>
                    <p className="text-sm text-slate-600 mb-4">{risk.description}</p>

                    <div className="grid grid-cols-2 gap-4 mb-4 sm:grid-cols-4">
                      <div>
                        <p className="text-xs text-slate-500">Likelihood</p>
                        <p className={cn("text-sm font-medium", getLikelihoodColor(risk.likelihood))}>
                          {risk.likelihood.charAt(0).toUpperCase() + risk.likelihood.slice(1)}
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-slate-500">Impact</p>
                        <p className={cn("text-sm font-medium", getImpactColor(risk.impact))}>
                          {risk.impact.charAt(0).toUpperCase() + risk.impact.slice(1)}
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-slate-500">Owner</p>
                        <p className="text-sm font-medium text-slate-900">{risk.owner}</p>
                      </div>
                      <div>
                        <p className="text-xs text-slate-500">Next Review</p>
                        <p className="text-sm font-medium text-slate-900">
                          {risk.nextReview.toLocaleDateString()}
                        </p>
                      </div>
                    </div>

                    <div className="flex items-center gap-2">
                      <a
                        href={risk.controlId ? `/controls/${risk.controlId}` : '#'}
                        className="text-xs text-primary-600 hover:underline"
                      >
                        Related Control: {risk.controlId || 'N/A'}
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* No results */}
        {filteredRisks.length === 0 && (
          <div className="rounded-lg border border-slate-200 bg-white p-12 text-center">
            <Shield className="mx-auto h-12 w-12 text-slate-300" />
            <h3 className="mt-4 text-lg font-medium text-slate-900">No risks found</h3>
            <p className="mt-2 text-sm text-slate-600">
              Try adjusting your filters to see more risks.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}