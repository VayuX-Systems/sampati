'use client';

import { useState } from 'react';
import { cn } from '@/lib/utils';
import {
  Shield,
  CheckCircle,
  AlertCircle,
  Clock,
  TrendingUp,
  FileText,
  Users,
  Calendar,
  Download
} from 'lucide-react';

interface StatCard {
  title: string;
  value: string | number;
  change?: string;
  changeType?: 'positive' | 'negative' | 'neutral';
  icon: React.ElementType;
  color: string;
}

interface AuditItem {
  id: string;
  name: string;
  framework: string;
  dueDate: Date;
  readinessScore: number;
  evidenceCount: number;
  controlCount: number;
}

interface FrameworkItem {
  id: string;
  name: string;
  controls: number;
  compliance: number;
  nextDeadline: Date;
}

interface FindingItem {
  id: string;
  title: string;
  severity: 'critical' | 'major' | 'minor';
  status: 'open' | 'resolved';
  dueDate: Date;
}

const STAT_CARDS: StatCard[] = [
  {
    title: 'Controls Passed',
    value: 856,
    change: '+12 from last month',
    changeType: 'positive',
    icon: CheckCircle,
    color: 'text-emerald-600'
  },
  {
    title: 'Compliance Score',
    value: '87%',
    change: '+3% improvement',
    changeType: 'positive',
    icon: Shield,
    color: 'text-primary-600'
  },
  {
    title: 'Pending Findings',
    value: 8,
    change: '-2 from last audit',
    changeType: 'positive',
    icon: AlertCircle,
    color: 'text-amber-600'
  },
  {
    title: 'Next Audit Due',
    value: '15 days',
    change: 'ISO 27001 Internal',
    changeType: 'neutral',
    icon: Calendar,
    color: 'text-blue-600'
  }
];

const SAMPLE_AUDITS: AuditItem[] = [
  {
    id: '1',
    name: 'ISO 27001 Internal Audit',
    framework: 'ISO 27001',
    dueDate: new Date('2026-11-28'),
    readinessScore: 68,
    evidenceCount: 35,
    controlCount: 93
  },
  {
    id: '2',
    name: 'SOC 2 Type II Audit',
    framework: 'SOC 2',
    dueDate: new Date('2026-12-15'),
    readinessScore: 85,
    evidenceCount: 42,
    controlCount: 108
  },
  {
    id: '3',
    name: 'DPDP Annual Review',
    framework: 'DPDP',
    dueDate: new Date('2026-12-05'),
    readinessScore: 92,
    evidenceCount: 28,
    controlCount: 45
  }
];

const SAMPLE_FRAMEWORKS: FrameworkItem[] = [
  {
    id: '1',
    name: 'ISO 27001',
    controls: 93,
    compliance: 87,
    nextDeadline: new Date('2026-11-28')
  },
  {
    id: '2',
    name: 'SOC 2',
    controls: 108,
    compliance: 92,
    nextDeadline: new Date('2026-12-15')
  },
  {
    id: '3',
    name: 'DPDP',
    controls: 45,
    compliance: 95,
    nextDeadline: new Date('2026-12-05')
  },
  {
    id: '4',
    name: 'CERT-In',
    controls: 52,
    compliance: 78,
    nextDeadline: new Date('2026-12-15')
  }
];

const SAMPLE_FINDINGS: FindingItem[] = [
  {
    id: '1',
    title: 'Multi-factor authentication not enforced for admin accounts',
    severity: 'critical',
    status: 'open',
    dueDate: new Date('2026-11-25')
  },
  {
    id: '2',
    title: 'Incident response plan testing overdue',
    severity: 'critical',
    status: 'open',
    dueDate: new Date('2026-11-22')
  },
  {
    id: '3',
    title: 'Third-party vendor risk assessment overdue',
    severity: 'major',
    status: 'open',
    dueDate: new Date('2026-11-28')
  },
  {
    id: '4',
    title: 'Security awareness training completion rate below threshold',
    severity: 'major',
    status: 'open',
    dueDate: new Date('2026-11-30')
  }
];

export function DashboardPage() {
  const [timeRange, setTimeRange] = useState<'7d' | '30d' | '90d'>('30d');

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8 flex flex-col justify-between gap-4 sm:items-center sm:flex-row">
          <div>
            <h1 className="text-3xl font-bold text-slate-900">Dashboard</h1>
            <p className="mt-1 text-sm text-slate-600">
              Overview of your compliance programme status
            </p>
          </div>
          <div className="flex items-center gap-3">
            <select
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value as any)}
              className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
            >
              <option value="7d">Last 7 days</option>
              <option value="30d">Last 30 days</option>
              <option value="90d">Last 90 days</option>
            </select>
            <button className="inline-flex items-center gap-2 rounded-lg bg-primary-600 px-4 py-2 text-sm font-semibold text-white hover:bg-primary-700">
              <Download className="h-4 w-4" />
              Export Report
            </button>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="mb-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {STAT_CARDS.map((card) => {
            const Icon = card.icon;
            return (
              <div
                key={card.title}
                className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-slate-600">{card.title}</p>
                    <p className="text-2xl font-bold text-slate-900">{card.value}</p>
                    {card.change && (
                      <p className={cn(
                        "text-xs",
                        card.changeType === 'positive' ? 'text-emerald-600' :
                        card.changeType === 'negative' ? 'text-red-600' :
                        'text-slate-500'
                      )}>
                        {card.change}
                      </p>
                    )}
                  </div>
                  <div className={cn("rounded-lg p-3", card.color)}>
                    <Icon className="h-6 w-6" />
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Quick Actions */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-slate-900 mb-4">Quick Actions</h2>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {[
              { name: 'Run Evidence Check', icon: Shield, href: '/' },
              { name: 'Prepare for Audit', icon: FileText, href: '/audits' },
              { name: 'Add New Control', icon: CheckCircle, href: '/controls' },
              { name: 'Invite Users', icon: Users, href: '/users' }
            ].map((action) => (
              <a
                key={action.name}
                href={action.href}
                className="flex items-center gap-3 rounded-lg border border-slate-200 bg-white p-4 hover:border-primary-200 transition-colors"
              >
                <action.icon className="h-5 w-5 text-primary-600" />
                <span className="font-medium text-slate-900">{action.name}</span>
              </a>
            ))}
          </div>
        </div>

        {/* Framework Progress */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-slate-900">Framework Progress</h2>
            <a href="/frameworks" className="text-sm font-medium text-primary-600 hover:underline">
              View all frameworks
            </a>
          </div>
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            {SAMPLE_FRAMEWORKS.map((framework) => (
              <div key={framework.id} className="rounded-lg border border-slate-200 bg-white p-6">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h3 className="text-lg font-semibold text-slate-900">{framework.name}</h3>
                    <p className="text-sm text-slate-500">
                      {framework.controls} controls • {framework.compliance}% compliant
                    </p>
                  </div>
                  <div className="text-right">
                    <span className={cn(
                      "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium",
                      framework.compliance >= 90 ? 'bg-emerald-100 text-emerald-800' :
                      framework.compliance >= 75 ? 'bg-amber-100 text-amber-800' :
                      'bg-red-100 text-red-800'
                    )}>
                      {framework.compliance}%
                    </span>
                  </div>
                </div>
                <div className="h-2 w-full rounded-full bg-slate-200">
                  <div
                    className="h-2 rounded-full transition-all duration-300"
                    style={{
                      width: `${framework.compliance}%`,
                      backgroundColor: framework.compliance >= 90 ? '#10b981' :
                      framework.compliance >= 75 ? '#f59e0b' : '#ef4444'
                    }}
                  />
                </div>
                <p className="mt-2 text-xs text-slate-500">
                  Next deadline: {framework.nextDeadline.toLocaleDateString()}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Upcoming Audits */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-slate-900">Upcoming Audits</h2>
            <a href="/audits" className="text-sm font-medium text-primary-600 hover:underline">
              View all audits
            </a>
          </div>
          <div className="grid grid-cols-1 gap-4">
            {SAMPLE_AUDITS.map((audit) => (
              <div
                key={audit.id}
                className="rounded-lg border border-slate-200 bg-white p-4 sm:p-6"
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-slate-900">{audit.name}</h3>
                    <p className="text-sm text-slate-600">
                      <span className="font-medium">Framework:</span> {audit.framework}
                    </p>
                    <p className="text-sm text-slate-500">
                      <span className="font-medium">Evidence:</span> {audit.evidenceCount}/{audit.controlCount} controls
                    </p>
                  </div>
                  <div className="text-right">
                    <div className="mb-2">
                      <span className={cn(
                        "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium",
                        audit.readinessScore >= 80 ? 'bg-emerald-100 text-emerald-800' :
                        audit.readinessScore >= 60 ? 'bg-amber-100 text-amber-800' :
                        'bg-red-100 text-red-800'
                      )}>
                        Readiness: {audit.readinessScore}%
                      </span>
                    </div>
                    <p className="text-sm text-slate-500">
                      Due: {audit.dueDate.toLocaleDateString()}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Critical Findings */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-slate-900">Critical Findings</h2>
            <a href="/audits#findings" className="text-sm font-medium text-primary-600 hover:underline">
              View all findings
            </a>
          </div>
          <div className="grid grid-cols-1 gap-4">
            {SAMPLE_FINDINGS.filter(f => f.severity === 'critical').map((finding) => (
              <div
                key={finding.id}
                className="rounded-lg border border-red-200 bg-red-50 p-4 sm:p-6"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="text-sm font-semibold text-red-900">{finding.title}</h3>
                    <p className="mt-1 text-xs text-red-700">
                      Due: {finding.dueDate.toLocaleDateString()}
                    </p>
                  </div>
                  <span className="inline-flex items-center rounded-full bg-red-100 px-2.5 py-0.5 text-xs font-medium text-red-800">
                    Critical
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}