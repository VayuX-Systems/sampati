'use client';

import { useState } from 'react';
import { cn } from '@/lib/utils';
import { Shield, Download, Play, AlertCircle, CheckCircle, Clock } from 'lucide-react';

interface Framework {
  id: string;
  name: string;
  displayName: string;
  controls: number;
  evidenceRequired: number;
  evidenceCollected: number;
  compliance: number;
  lastAudit: Date;
  nextDeadline: Date;
  status: 'active' | 'pending' | 'overdue';
  region: string;
  description: string;
}

const FRAMEWORKS: Framework[] = [
  {
    id: 'iso27001',
    name: 'ISO 27001',
    displayName: 'ISO/IEC 27001:2013 Information Security Management',
    controls: 93,
    evidenceRequired: 93,
    evidenceCollected: 81,
    compliance: 87,
    lastAudit: new Date('2026-09-15'),
    nextDeadline: new Date('2026-11-28'),
    status: 'active',
    region: 'Global',
    description: 'International standard for information security management systems'
  },
  {
    id: 'soc2',
    name: 'SOC 2',
    displayName: 'SOC 2 Type II - Security and Availability',
    controls: 108,
    evidenceRequired: 108,
    evidenceCollected: 92,
    compliance: 85,
    lastAudit: new Date('2026-10-15'),
    nextDeadline: new Date('2026-12-15'),
    status: 'active',
    region: 'US',
    description: 'Service Organization Control for US businesses'
  },
  {
    id: 'dpdp',
    name: 'DPDP',
    displayName: 'Digital Personal Data Protection Act',
    controls: 45,
    evidenceRequired: 45,
    evidenceCollected: 42,
    compliance: 93,
    lastAudit: new Date('2026-08-10'),
    nextDeadline: new Date('2026-12-05'),
    status: 'active',
    region: 'India',
    description: 'India\'s comprehensive data protection law'
  },
  {
    id: 'certin',
    name: 'CERT-In',
    displayName: 'Information Technology Act - Security Practices',
    controls: 52,
    evidenceRequired: 52,
    evidenceCollected: 41,
    compliance: 79,
    lastAudit: new Date('2026-07-22'),
    nextDeadline: new Date('2026-12-15'),
    status: 'active',
    region: 'India',
    description: 'Indian cybersecurity regulations for critical sectors'
  },
  {
    id: 'rbi-cscrf',
    name: 'RBI CSCRF',
    displayName: 'RBI Cyber Security Framework for NBFCs',
    controls: 67,
    evidenceRequired: 67,
    evidenceCollected: 37,
    compliance: 55,
    lastAudit: new Date('2026-06-30'),
    nextDeadline: new Date('2026-12-25'),
    status: 'overdue',
    region: 'India',
    description: 'Reserve Bank of India cybersecurity requirements for NBFCs'
  }
];

export function FrameworksPage() {
  const [filter, setFilter] = useState<'all' | 'active' | 'compliant' | 'needs-attention'>('all');

  const filteredFrameworks = FRAMEWORKS.filter(framework => {
    if (filter === 'all') return true;
    if (filter === 'active') return framework.status === 'active';
    if (filter === 'compliant') return framework.compliance >= 85;
    if (filter === 'needs-attention') return framework.compliance < 75 || framework.status === 'overdue';
    return true;
  });

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8 flex flex-col justify-between gap-4 sm:items-center sm:flex-row">
          <div>
            <h1 className="text-3xl font-bold text-slate-900">Frameworks</h1>
            <p className="mt-1 text-sm text-slate-600">
              Manage compliance frameworks, controls, and evidence collection
            </p>
          </div>
          <button className="inline-flex items-center gap-2 rounded-lg bg-primary-600 px-4 py-2 text-sm font-semibold text-white hover:bg-primary-700">
            <Shield className="h-4 w-4" />
            <span>Install New Pack</span>
          </button>
        </div>

        {/* Filters */}
        <div className="mb-6 flex items-center gap-3">
          <div className="flex items-center gap-2 rounded-lg border border-slate-300 bg-white p-1">
            {[
              { id: 'all', label: 'All Frameworks' },
              { id: 'active', label: 'Active Only' },
              { id: 'compliant', label: 'Highly Compliant' },
              { id: 'needs-attention', label: 'Needs Attention' }
            ].map((f) => (
              <button
                key={f.id}
                onClick={() => setFilter(f.id as any)}
                className={cn(
                  "px-3 py-1 text-sm rounded-lg transition-colors",
                  filter === f.id
                    ? "bg-primary-600 text-white"
                    : "text-slate-600 hover:bg-slate-100"
                )}
              >
                {f.label}
              </button>
            ))}
          </div>
        </div>

        {/* Framework Cards Grid */}
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
          {filteredFrameworks.map((framework) => {
            const getStatusColor = (status: string, compliance: number) => {
              if (status === 'overdue') return 'border-red-200 bg-white';
              if (compliance >= 85) return 'border-emerald-200 bg-white';
              if (compliance >= 75) return 'border-amber-200 bg-white';
              return 'border-red-200 bg-white';
            };

            const getStatusBadgeColor = (compliance: number, status: string) => {
              if (status === 'overdue') return 'bg-red-100 text-red-800';
              if (compliance >= 85) return 'bg-emerald-100 text-emerald-800';
              if (compliance >= 75) return 'bg-amber-100 text-amber-800';
              return 'bg-red-100 text-red-800';
            };

            return (
              <div
                key={framework.id}
                className={cn(
                  "rounded-lg border p-6 shadow-sm",
                  getStatusColor(framework.status, framework.compliance)
                )}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <Shield className="h-6 w-6 text-primary-600" />
                      <h2 className="text-xl font-semibold text-slate-900">{framework.displayName}</h2>
                    </div>
                    <p className="text-sm text-slate-600 mb-4">{framework.description}</p>

                    <div className="grid grid-cols-2 gap-4 mb-4">
                      <div>
                        <p className="text-xs text-slate-500">Controls</p>
                        <p className="text-sm font-medium text-slate-900">
                          {framework.evidenceCollected} / {framework.evidenceRequired}
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-slate-500">Compliance</p>
                        <p className="text-sm font-medium text-slate-900">
                          {framework.compliance}%
                        </p>
                      </div>
                    </div>

                    <div className="mb-4">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs text-slate-600">Progress</span>
                        <span className="text-xs text-slate-500">
                          {framework.evidenceCollected}/{framework.evidenceRequired} evidence collected
                        </span>
                      </div>
                      <div className="h-2 w-full rounded-full bg-slate-200">
                        <div
                          className="h-2 rounded-full transition-all duration-300"
                          style={{
                            width: `${(framework.evidenceCollected / framework.evidenceRequired) * 100}%`,
                            backgroundColor: framework.compliance >= 85 ? '#10b981' :
                            framework.compliance >= 75 ? '#f59e0b' : '#ef4444'
                          }}
                        />
                      </div>
                    </div>

                    <div className="flex items-center gap-4 text-xs text-slate-500">
                      <span>Last audit: {framework.lastAudit.toLocaleDateString()}</span>
                      <span>Next deadline: {framework.nextDeadline.toLocaleDateString()}</span>
                    </div>
                  </div>

                  <div className="flex flex-col items-center gap-2">
                    <span
                      className={cn(
                        "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium",
                        getStatusBadgeColor(framework.compliance, framework.status)
                      )}
                    >
                      {framework.status === 'overdue' ? 'Overdue' :
                       framework.compliance >= 85 ? 'Compliant' :
                       'Progressing'}
                    </span>
                    <a
                      href={`/controls?framework=${framework.id}`}
                      className="rounded-lg p-2 text-primary-600 hover:bg-primary-50"
                      title="View controls"
                    >
                      <Shield className="h-4 w-4" />
                    </a>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Action Items */}
        <div className="mt-8">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">Action Items</h3>

          {FRAMEWORKS.filter(f => f.compliance < 75 || f.status === 'overdue').length > 0 ? (
            <div className="rounded-lg border border-red-200 bg-red-50 p-4 sm:p-6">
              <div className="flex items-start gap-3">
                <AlertCircle className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" />
                <div className="flex-1">
                  <h4 className="text-sm font-medium text-red-900 mb-2">
                    Frameworks needing attention
                  </h4>
                  <ul className="space-y-2">
                    {FRAMEWORKS.filter(f => f.compliance < 75 || f.status === 'overdue').map(f => (
                      <li key={f.id} className="text-sm text-red-800">
                        <span className="font-medium">{f.displayName}</span> - {f.compliance}% compliant, due {f.nextDeadline.toLocaleDateString()}
                      </li>
                    ))}
                  </ul>
                  <button className="mt-3 text-sm font-medium text-red-800 hover:underline">
                    View remediation plan
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <div className="rounded-lg border border-emerald-200 bg-emerald-50 p-6 text-center">
              <CheckCircle className="mx-auto h-12 w-12 text-emerald-600" />
              <h4 className="mt-4 text-lg font-medium text-emerald-900">All frameworks compliant</h4>
              <p className="mt-2 text-sm text-emerald-700">
                All compliance frameworks are at or above 75% compliance.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}