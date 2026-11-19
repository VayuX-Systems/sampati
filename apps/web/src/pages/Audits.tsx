'use client';

import { useState, useMemo } from 'react';
import { Calendar, CheckCircle, Clock, FileDown, Filter, Search, Shield, Bug, AlertCircle, Download } from 'lucide-react';
import { format, parseISO, isToday, isTomorrow, isPast } from 'date-fns';
import { cn } from '@/lib/utils';

// Type definitions
type AuditStatus = 'Pending' | 'In Progress' | 'Completed';
type AuditFindingsStatus = 'Pass' | 'Conditional Pass' | 'Fail';
type FindingSeverity = 'Critical' | 'Major' | 'Minor';
type FindingStatus = 'Open' | 'In Progress' | 'Resolved' | 'Closed';
type ReportType = 'Executive Summary' | 'Technical' | 'Compliance Gap Analysis';
type ExportFormat = 'PDF' | 'CSV' | 'Excel';

interface Audit {
  id: string;
  name: string;
  framework: string;
  scheduledDate: Date;
  dueDate: Date;
  auditor: string;
  status: AuditStatus;
  readinessScore: number;
  evidenceCount: number;
  controlCount: number;
}

interface AuditHistoryItem {
  id: string;
  name: string;
  auditor: string;
  dateCompleted: Date;
  findings: {
    critical: number;
    major: number;
    minor: number;
  };
  status: AuditFindingsStatus;
  reportUrl?: string;
}

interface Finding {
  id: string;
  title: string;
  severity: FindingSeverity;
  status: FindingStatus;
  assignedTo: string;
  dueDate: Date;
  controlId: string;
  controlName: string;
  description: string;
}

interface RemediationItem {
  id: string;
  findingId: string;
  description: string;
  owner: string;
  dueDate: Date;
  status: 'Not Started' | 'In Progress' | 'Completed';
  progress: number;
}

// Sample data
const sampleAudits: Audit[] = [
  {
    id: '1',
    name: 'SOC 2 Type II Audit',
    framework: 'SOC 2',
    scheduledDate: new Date('2026-12-15'),
    dueDate: new Date('2026-12-30'),
    auditor: 'Deloitte & Touche',
    status: 'In Progress',
    readinessScore: 85,
    evidenceCount: 42,
    controlCount: 108,
  },
  {
    id: '2',
    name: 'ISO 27001 Internal Audit',
    framework: 'ISO 27001',
    scheduledDate: new Date('2026-11-28'),
    dueDate: new Date('2026-12-10'),
    auditor: 'EY',
    status: 'Pending',
    readinessScore: 68,
    evidenceCount: 35,
    controlCount: 93,
  },
  {
    id: '3',
    name: 'DPDP Annual Compliance Review',
    framework: 'DPDP',
    scheduledDate: new Date('2026-11-20'),
    dueDate: new Date('2026-12-05'),
    auditor: 'Grant Thornton',
    status: 'Completed',
    readinessScore: 92,
    evidenceCount: 28,
    controlCount: 45,
  },
  {
    id: '4',
    name: 'CERT-In Compliance Audit',
    framework: 'CERT-In',
    scheduledDate: new Date('2026-12-01'),
    dueDate: new Date('2026-12-15'),
    auditor: 'PwC India',
    status: 'Completed',
    readinessScore: 78,
    evidenceCount: 19,
    controlCount: 52,
  },
  {
    id: '5',
    name: 'RBI CSCRF Quarterly Review',
    framework: 'RBI CSCRF',
    scheduledDate: new Date('2026-12-10'),
    dueDate: new Date('2026-12-25'),
    auditor: 'KPMG Enterprise',
    status: 'Pending',
    readinessScore: 55,
    evidenceCount: 24,
    controlCount: 67,
  },
];

const sampleAuditHistory: AuditHistoryItem[] = [
  {
    id: '1',
    name: 'SOC 2 Type II Audit',
    auditor: 'Deloitte & Touche',
    dateCompleted: new Date('2026-10-15'),
    findings: { critical: 1, major: 3, minor: 5 },
    status: 'Pass',
    reportUrl: '/reports/soc2-2026-deloitte.pdf',
  },
  {
    id: '2',
    name: 'ISO 27001 Internal Audit',
    auditor: 'EY',
    dateCompleted: new Date('2026-09-28'),
    findings: { critical: 0, major: 2, minor: 4 },
    status: 'Conditional Pass',
    reportUrl: '/reports/iso27001-2026-ey.pdf',
  },
  {
    id: '3',
    name: 'DPDP Compliance Audit',
    auditor: 'Grant Thornton',
    dateCompleted: new Date('2026-08-10'),
    findings: { critical: 0, major: 1, minor: 3 },
    status: 'Pass',
    reportUrl: '/reports/dpdp-2026-grantthornton.pdf',
  },
  {
    id: '4',
    name: 'CERT-In Security Audit',
    auditor: 'PwC India',
    dateCompleted: new Date('2026-07-22'),
    findings: { critical: 2, major: 4, minor: 7 },
    status: 'Fail',
    reportUrl: '/reports/certin-2026-pwc.pdf',
  },
];

const sampleFindings: Finding[] = [
  {
    id: 'f1',
    title: 'Multi-factor authentication not enforced for admin accounts',
    severity: 'Critical',
    status: 'Open',
    assignedTo: 'Priya Sharma',
    dueDate: new Date('2026-11-25'),
    controlId: 'C-001',
    controlName: 'Access Control - Admin Authentication',
    description: 'Admin accounts do not have MFA enforced, creating a single point of failure for critical systems.',
  },
  {
    id: 'f2',
    title: 'Third-party vendor risk assessment overdue',
    severity: 'Major',
    status: 'In Progress',
    assignedTo: 'Rajesh Kumar',
    dueDate: new Date('2026-11-28'),
    controlId: 'C-045',
    controlName: 'Vendor Risk Management',
    description: 'Annual risk assessment for cloud storage vendor has not been completed.',
  },
  {
    id: 'f3',
    title: 'Security awareness training completion rate below threshold',
    severity: 'Major',
    status: 'Open',
    assignedTo: 'Ananya Patel',
    dueDate: new Date('2026-11-30'),
    controlId: 'C-012',
    controlName: 'Personnel Security Training',
    description: 'Only 78% of staff have completed annual security awareness training.',
  },
  {
    id: 'f4',
    title: 'Data retention policy not documented',
    severity: 'Minor',
    status: 'Resolved',
    assignedTo: 'Vikram Singh',
    dueDate: new Date('2026-11-20'),
    controlId: 'C-023',
    controlName: 'Data Retention Policy',
    description: 'No formal data retention policy exists for customer data.',
  },
  {
    id: 'f5',
    title: 'Incident response plan testing overdue',
    severity: 'Critical',
    status: 'Open',
    assignedTo: 'Meera Iyer',
    dueDate: new Date('2026-11-22'),
    controlId: 'C-005',
    controlName: 'Incident Response',
    description: 'Annual incident response plan tabletop exercise was not conducted.',
  },
  {
    id: 'f6',
    title: 'Evidence freshness check for access logs',
    severity: 'Minor',
    status: 'Closed',
    assignedTo: 'Karthik Rao',
    dueDate: new Date('2026-11-18'),
    controlId: 'C-008',
    controlName: 'Access Log Monitoring',
    description: 'Access logs are being maintained but need quarterly review.',
  },
];

const sampleRemediationItems: RemediationItem[] = [
  {
    id: 'r1',
    findingId: 'f1',
    description: 'Implement MFA for all admin accounts and enforce via IAM policies',
    owner: 'Priya Sharma',
    dueDate: new Date('2026-11-25'),
    status: 'In Progress',
    progress: 40,
  },
  {
    id: 'r2',
    findingId: 'f5',
    description: 'Conduct tabletop exercise for incident response plan',
    owner: 'Meera Iyer',
    dueDate: new Date('2026-11-22'),
    status: 'Not Started',
    progress: 0,
  },
  {
    id: 'r3',
    findingId: 'f2',
    description: 'Complete third-party risk assessment and update vendor register',
    owner: 'Rajesh Kumar',
    dueDate: new Date('2026-11-28'),
    status: 'In Progress',
    progress: 65,
  },
  {
    id: 'r4',
    findingId: 'f3',
    description: 'Schedule and complete security awareness training for all staff',
    owner: 'Ananya Patel',
    dueDate: new Date('2026-11-30'),
    status: 'Not Started',
    progress: 0,
  },
];

// Available frameworks
const AVAILABLE_FRAMEWORKS = ['SOC 2', 'ISO 27001', 'DPDP', 'CERT-In', 'RBI CSCRF', 'SEBI CSCRF', 'IRDAI'];

// Status colors
const STATUS_COLORS: Record<AuditStatus, { bg: string; text: string; badge: string; border: string }> = {
  Pending: {
    bg: 'bg-amber-50',
    text: 'text-amber-700',
    badge: 'bg-amber-100 text-amber-800',
    border: 'border-amber-200',
  },
  'In Progress': {
    bg: 'bg-blue-50',
    text: 'text-blue-700',
    badge: 'bg-blue-100 text-blue-800',
    border: 'border-blue-200',
  },
  Completed: {
    bg: 'bg-emerald-50',
    text: 'text-emerald-700',
    badge: 'bg-emerald-100 text-emerald-800',
    border: 'border-emerald-200',
  },
};

const FINDING_STATUS_COLORS: Record<FindingStatus, { bg: string; text: string; badge: string; border: string }> = {
  Open: {
    bg: 'bg-red-50',
    text: 'text-red-700',
    badge: 'bg-red-100 text-red-800',
    border: 'border-red-200',
  },
  'In Progress': {
    bg: 'bg-blue-50',
    text: 'text-blue-700',
    badge: 'bg-blue-100 text-blue-800',
    border: 'border-blue-200',
  },
  Resolved: {
    bg: 'bg-yellow-50',
    text: 'text-yellow-700',
    badge: 'bg-yellow-100 text-yellow-800',
    border: 'border-yellow-200',
  },
  Closed: {
    bg: 'bg-emerald-50',
    text: 'text-emerald-700',
    badge: 'bg-emerald-100 text-emerald-800',
    border: 'border-emerald-200',
  },
};

const SEVERITY_COLORS: Record<FindingSeverity, { bg: string; text: string; badge: string; icon: string }> = {
  Critical: {
    bg: 'bg-red-50',
    text: 'text-red-700',
    badge: 'bg-red-100 text-red-800',
    icon: 'danger',
  },
  Major: {
    bg: 'bg-amber-50',
    text: 'text-amber-700',
    badge: 'bg-amber-100 text-amber-800',
    icon: 'warning',
  },
  Minor: {
    bg: 'bg-slate-50',
    text: 'text-slate-700',
    badge: 'bg-slate-100 text-slate-800',
    icon: 'info',
  },
};

export default function AuditsPage() {
  const [activeTab, setActiveTab] = useState<'schedule' | 'history' | 'findings' | 'remediation' | 'reports'>('schedule');
  const [frameworkFilter, setFrameworkFilter] = useState<string>('All');
  const [statusFilter, setStatusFilter] = useState<AuditStatus | 'All'>('All');

  const filteredAudits = useMemo(() => {
    return sampleAudits.filter((audit) => {
      const matchesFramework = frameworkFilter === 'All' || audit.framework === frameworkFilter;
      const matchesStatus = statusFilter === 'All' || audit.status === statusFilter;
      return matchesFramework && matchesStatus;
    });
  }, [frameworkFilter, statusFilter]);

  const pendingCount = sampleAudits.filter(a => a.status === 'Pending').length;
  const inProgressCount = sampleAudits.filter(a => a.status === 'In Progress').length;
  const completedCount = sampleAudits.filter(a => a.status === 'Completed').length;

  const overallReadiness = Math.round(
    sampleAudits.reduce((sum, audit) => sum + audit.readinessScore, 0) / sampleAudits.length
  );

  const upcomingDeadlines = sampleAudits
    .filter(a => a.dueDate > new Date() && a.status !== 'Completed')
    .sort((a, b) => a.dueDate.getTime() - b.dueDate.getTime())
    .slice(0, 3);

  const totalFindings = sampleFindings.length;
  const criticalFindings = sampleFindings.filter(f => f.severity === 'Critical').length;
  const openFindings = sampleFindings.filter(f => f.status === 'Open').length;

  return (
    <div className="min-h-screen bg-slate-50 p-4 sm:p-6 lg:p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900">Audit & Reports Management</h1>
        <p className="mt-1 text-sm text-slate-600">
          Monitor audit schedules, track findings, and generate compliance reports
        </p>
      </div>

      {/* Quick Stats Overview */}
      <div className="mb-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <div className="rounded-lg border border-slate-200 bg-white p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-600">Pending Audits</p>
              <p className="text-2xl font-bold text-slate-900">{pendingCount}</p>
            </div>
            <Clock className="h-8 w-8 text-amber-500" />
          </div>
        </div>
        <div className="rounded-lg border border-slate-200 bg-white p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-600">In Progress</p>
              <p className="text-2xl font-bold text-slate-900">{inProgressCount}</p>
            </div>
            <Shield className="h-8 w-8 text-blue-500" />
          </div>
        </div>
        <div className="rounded-lg border border-slate-200 bg-white p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-600">Completed</p>
              <p className="text-2xl font-bold text-slate-900">{completedCount}</p>
            </div>
            <CheckCircle className="h-8 w-8 text-emerald-500" />
          </div>
        </div>
        <div className="rounded-lg border border-slate-200 bg-white p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-600">Readiness Score</p>
              <p className="text-2xl font-bold text-slate-900">{overallReadiness}%</p>
            </div>
            <Shield className="h-8 w-8 text-primary-600" />
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="mb-6 border-b border-slate-200">
        <nav className="-mb-px flex gap-4">
          {[
            { id: 'schedule', label: 'Audit Schedules', icon: Calendar },
            { id: 'history', label: 'Audit History', icon: CheckCircle },
            { id: 'findings', label: 'Findings & Issues', icon: Bug },
            { id: 'remediation', label: 'Remediation Tracking', icon: Shield },
            { id: 'reports', label: 'Report Generation', icon: FileDown },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={cn(
                'flex items-center gap-2 border-b-2 px-4 py-2 text-sm font-medium transition-colors',
                activeTab === tab.id
                  ? 'border-primary-600 text-primary-600'
                  : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
              )}
            >
              <tab.icon className="h-4 w-4" />
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      {activeTab === 'schedule' && (
        <div className="space-y-6">
          {/* Filters */}
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-center gap-4">
              <div className="relative">
                <Filter className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                <select
                  value={frameworkFilter}
                  onChange={(e) => setFrameworkFilter(e.target.value)}
                  className="relative w-40 rounded-lg border border-slate-300 bg-white pl-10 pr-4 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                >
                  <option value="All">All Frameworks</option>
                  {AVAILABLE_FRAMEWORKS.map((framework) => (
                    <option key={framework} value={framework}>
                      {framework}
                    </option>
                  ))}
                </select>
              </div>

              <div className="relative">
                <Filter className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                <select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value as AuditStatus | 'All')}
                  className="relative w-32 rounded-lg border border-slate-300 bg-white pl-10 pr-4 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                >
                  <option value="All">All Status</option>
                  <option value="Pending">Pending</option>
                  <option value="In Progress">In Progress</option_value>
                  <option value="Completed">Completed</option>
                </select>
              </div>
            </div>

            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
              <input
                type="text"
                placeholder="Search audits..."
                className="w-64 rounded-lg border border-slate-300 bg-white pl-10 pr-4 py-2 text-sm shadow-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
              />
            </div>
          </div>

          {/* Upcoming Deadlines */}
          <div>
            <h2 className="text-xl font-semibold text-slate-900 mb-4">Upcoming Deadlines</h2>
            {upcomingDeadlines.length > 0 ? (
              <div className="space-y-4">
                {upcomingDeadlines.map((audit) => (
                  <div
                    key={audit.id}
                    className="rounded-lg border border-slate-200 bg-white p-6"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-slate-900">{audit.name}</h3>
                        <p className="text-sm text-slate-600">
                          <span className="font-medium">Auditor:</span> {audit.auditor}
                        </p>
                        <p className="text-sm text-slate-600">
                          <span className="font-medium">Framework:</span> {audit.framework}
                        </p>
                      </div>
                      <div className="text-right">
                        <div className={cn(
                          'inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium',
                          STATUS_COLORS[audit.status].badge
                        )}>
                          {audit.status}
                        </div>
                        <p className="mt-1 text-sm text-slate-600">
                          <Calendar className="inline h-4 w-4 mr-1" />
                          Due {format(audit.dueDate, 'MMM d, yyyy')}
                        </p>
                      </div>
                    </div>
                    <div className="mt-4">
                      <div className="flex items-center gap-4 text-sm text-slate-600">
                        <span>Readiness: {audit.readinessScore}%</span>
                        <span>Evidence: {audit.evidenceCount}/{audit.controlCount} controls</span>
                      </div>
                      <div className="mt-2 h-2 w-full rounded-full bg-slate-200">
                        <div
                          className="h-2 rounded-full transition-all duration-300"
                          style={{
                            width: `${(audit.evidenceCount / audit.controlCount) * 100}%`,
                            backgroundColor: audit.readinessScore >= 80 ? '#10b981' : audit.readinessScore >= 60 ? '#f59e0b' : '#ef4444',
                          }}
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="rounded-lg border border-slate-200 bg-white p-12 text-center">
                <CheckCircle className="mx-auto h-12 w-12 text-slate-300" />
                <h3 className="mt-4 text-lg font-medium text-slate-900">No upcoming audits</h3>
                <p className="mt-2 text-sm text-slate-600">All scheduled audits have been completed.</p>
              </div>
            )}
          </div>

          {/* Audit Schedule Calendar */}
          <div>
            <h2 className="text-xl font-semibold text-slate-900 mb-4">Audit Calendar</h2>
            <div className="rounded-lg border border-slate-200 bg-white p-6">
              <div className="grid grid-cols-7 gap-px bg-slate-200">
                {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((day) => (
                  <div key={day} className="bg-slate-100 p-2 text-center text-sm font-semibold text-slate-600">
                    {day}
                  </div>
                ))}
                {/* Calendar grid - simplified view */}
                <div className="col-span-7 mt-4 grid grid-cols-7 gap-px bg-slate-100">
                  <div className="bg-white p-2 min-h-[80px] border border-slate-200">
                    <div className="text-xs text-slate-400">19</div>
                  </div>
                  <div className="bg-white p-2 min-h-[80px] border border-slate-200">
                    <div className="text-xs text-slate-400">20</div>
                  </div>
                  <div className="bg-white p-2 min-h:[80px] border border-slate-200">
                    <div className="text-xs text-slate-400">21</div>
                  </div>
                  <div className="bg-primary-50 p-2 min-h:[80px] border border-slate-200">
                    <div className="text-xs text-slate-500">22</div>
                    <div className="mt-1 text-xs font-medium text-primary-700">DPDP</div>
                  </div>
                  <div className="bg-white p-2 min-h:[80px] border border-slate-200">
                    <div className="text-xs text-slate-400">23</div>
                  </div>
                  <div className="bg-amber-50 p-2 min-h:[80px] border border-slate-200">
                    <div className="text-xs text-slate-500">24</div>
                    <div className="mt-1 text-xs font-medium text-amber-700">RBI</div>
                  </div>
                  <div className="bg-white p-2 min-h:[80px] border border-slate-200">
                    <div className="text-xs text-slate-400">25</div>
                  </div>
                </div>
              </div>
              <div className="mt-4 flex items-center gap-6 text-sm">
                <div className="flex items-center gap-2">
                  <div className="h-3 w-3 rounded-full bg-emerald-100"></div>
                  <span className="text-slate-600">Completed</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="h-3 w-3 rounded-full bg-amber-100"></div>
                  <span className="text-slate-600">Upcoming</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="h-3 w-3 rounded-full bg-blue-100"></div>
                  <span className="text-slate-600">Due Soon</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'history' && (
        <div>
          <h2 className="text-xl font-semibold text-slate-900 mb-4">Audit History</h2>

          {/* History Table */}
          <div className="rounded-lg border border-slate-200 bg-white shadow-sm">
            <table className="w-full">
              <thead>
                <tr className="border-b border-slate-200 bg-slate-50">
                  <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">
                    Audit Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">
                    Auditor
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">
                    Date Completed
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">
                    Findings
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">
                    Status
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-semibold uppercase tracking-wider text-slate-600">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200">
                {sampleAuditHistory.map((audit) => (
                  <tr key={audit.id} className="hover:bg-slate-50 transition-colors">
                    <td className="px-6 py-4">
                      <div className="font-medium text-slate-900">{audit.name}</div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm text-slate-700">{audit.auditor}</div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm text-slate-700">
                        {format(audit.dateCompleted, 'MMM d, yyyy')}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2">
                        {audit.findings.critical > 0 && (
                          <span className="inline-flex items-center rounded-full bg-red-100 px-2 py-0.5 text-xs font-medium text-red-800">
                            Critical: {audit.findings.critical}
                          </span>
                        )}
                        {audit.findings.major > 0 && (
                          <span className="inline-flex items-center rounded-full bg-amber-100 px-2 py-0.5 text-xs font-medium text-amber-800">
                            Major: {audit.findings.major}
                          </span>
                        )}
                        {audit.findings.minor > 0 && (
                          <span className="inline-flex items-center rounded-full bg-slate-100 px-2 py-0.5 text-xs font-medium text-slate-800">
                            Minor: {audit.findings.minor}
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span
                        className={cn(
                          'inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium',
                          audit.status === 'Pass' && 'bg-emerald-100 text-emerald-800',
                          audit.status === 'Conditional Pass' && 'bg-amber-100 text-amber-800',
                          audit.status === 'Fail' && 'bg-red-100 text-red-800'
                        )}
                      >
                        {audit.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <button
                        className="rounded-lg p-1.5 text-slate-400 hover:text-primary-600 hover:bg-primary-50"
                        title="Download Report"
                      >
                        <Download className="h-4 w-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {activeTab === 'findings' && (
        <div>
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-xl font-semibold text-slate-900">Findings & Issues</h2>
            <div className="flex items-center gap-2 text-sm text-slate-600">
              <Bug className="h-4 w-4" />
              <span>{totalFindings} total findings, {openFindings} open</span>
            </div>
          </div>

          {/* Findings Summary */}
          <div className="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div className="rounded-lg border border-red-200 bg-red-50 p-4">
              <div className="flex items-center gap-2">
                <div className="h-8 w-8 rounded-full bg-red-500 flex items-center justify-center">
                  <span className="text-xs font-bold text-white">{criticalFindings}</span>
                </div>
                <div>
                  <p className="text-sm font-medium text-red-900">Critical</p>
                  <p className="text-xs text-red-700">{criticalFindings} open issues</p>
                </div>
              </div>
            </div>
            <div className="rounded-lg border border-amber-200 bg-amber-50 p-4">
              <div className="flex items-center gap-2">
                <div className="h-8 w-8 rounded-full bg-amber-500 flex items-center justify-center">
                  <span className="text-xs font-bold text-white">5</span>
                </div>
                <div>
                  <p className="text-sm font-medium text-amber-900">Major</p>
                  <p className="text-xs text-amber-700">5 open issues</p>
                </div>
              </div>
            </div>
            <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
              <div className="flex items-center gap-2">
                <div className="h-8 w-8 rounded-full bg-slate-500 flex items-center justify-center">
                  <span className="text-xs font-bold text-white">2</span>
                </div>
                <div>
                  <p className="text-sm font-medium text-slate-900">Minor</p>
                  <p className="text-xs text-slate-700">2 open issues</p>
                </div>
              </div>
            </div>
          </div>

          {/* Findings List */}
          <div className="space-y-4">
            {sampleFindings.map((finding) => (
              <div
                key={finding.id}
                className="rounded-lg border border-slate-200 bg-white p-6"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <span
                        className={cn(
                          'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium',
                          SEVERITY_COLORS[finding.severity].badge
                        )}
                      >
                        {finding.severity}
                      </span>
                      <span
                        className={cn(
                          'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium',
                          FINDING_STATUS_COLORS[finding.status].badge
                        )}
                      >
                        {finding.status}
                      </span>
                    </div>
                    <h3 className="text-lg font-semibold text-slate-900 mb-1">{finding.title}</h3>
                    <p className="text-sm text-slate-600 mb-3">{finding.description}</p>
                    <div className="flex items-center gap-4 text-sm text-slate-500">
                      <div>
                        <span className="font-medium text-slate-700">Control:</span>{' '}
                        {finding.controlName} ({finding.controlId})
                      </div>
                      <div>
                        <span className="font-medium text-slate-700">Assigned to:</span>{' '}
                        {finding.assignedTo}
                      </div>
                      <div>
                        <span className="font-medium text-slate-700">Due:</span>{' '}
                        {format(finding.dueDate, 'MMM d, yyyy')}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'remediation' && (
        <div>
          <h2 className="text-xl font-semibold text-slate-900 mb-4">Remediation Tracking</h2>

          {/* Remediation Overview */}
          <div className="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-4">
            <div className="rounded-lg border border-slate-200 bg-white p-4">
              <p className="text-sm font-medium text-slate-600">Not Started</p>
              <p className="text-2xl font-bold text-slate-900">2</p>
            </div>
            <div className="rounded-lg border border-slate-200 bg-white p-4">
              <p className="text-sm font-medium text-slate-600">In Progress</p>
              <p className="text-2xl font-bold text-slate-900">2</p>
            </div>
            <div className="rounded-lg border border-slate-200 bg-white p-4">
              <p className="text-sm font-medium text-slate-600">Completed</p>
              <p className="text-2xl font-bold text-slate-900">1</p>
            </div>
            <div className="rounded-lg border border-slate-200 bg-white p-4">
              <p className="text-sm font-medium text-slate-600">Avg Progress</p>
              <p className="text-2xl font-bold text-slate-900">35%</p>
            </div>
          </div>

          {/* Remediation Items Table */}
          <div className="rounded-lg border border-slate-200 bg-white shadow-sm">
            <table className="w-full">
              <thead>
                <tr className="border-b border-slate-200 bg-slate-50">
                  <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">
                    Action Item
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">
                    Owner
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">
                    Due Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">
                    Progress
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-semibold uppercase tracking-wider text-slate-600">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200">
                {sampleRemediationItems.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-50 transition-colors">
                    <td className="px-6 py-4">
                      <div className="font-medium text-slate-900">{item.description}</div>
                      <div className="text-xs text-slate-500">
                        Related to: {sampleFindings.find(f => f.id === item.findingId)?.title.substring(0, 50)}...
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm text-slate-700">{item.owner}</div>
                    </td>
                    <td className="px-6 py-4">
                      {isPast(item.dueDate) && item.status !== 'Completed' ? (
                        <span className="text-sm text-red-600 font-medium">
                          Overdue: {format(item.dueDate, 'MMM d')}
                        </span>
                      ) : (
                        <span className="text-sm text-slate-700">
                          {format(item.dueDate, 'MMM d, yyyy')}
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        <div className="w-24 rounded-full bg-slate-200 h-2">
                          <div
                            className={cn(
                              'h-2 rounded-full transition-all duration-300',
                              item.status === 'Completed' ? 'bg-emerald-500' :
                              item.status === 'In Progress' ? 'bg-primary-500' : 'bg-slate-400'
                            )}
                            style={{ width: `${item.progress}%` }}
                          />
                        </div>
                        <span className="text-xs text-slate-600">{item.progress}%</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <select
                        className="rounded-lg border border-slate-300 bg-white px-3 py-1 text-sm focus:ring-2 focus:ring-primary-500"
                        defaultValue={item.status}
                      >
                        <option value="Not Started">Not Started</option>
                        <option value="In Progress">In Progress</option>
                        <option value="Completed">Completed</option>
                      </select>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {activeTab === 'reports' && (
        <div>
          <h2 className="text-xl font-semibold text-slate-900 mb-4">Report Generation</h2>

          <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            {/* Report Configuration */}
            <div className="rounded-lg border border-slate-200 bg-white p-6">
              <h3 className="text-lg font-semibold text-slate-900 mb-4">Report Settings</h3>

              <div className="space-y-4">
                {/* Framework Selection */}
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Choose Framework(s)
                  </label>
                  <div className="grid grid-cols-2 gap-2">
                    {AVAILABLE_FRAMEWORKS.map((framework) => (
                      <label key={framework} className="flex items-center gap-2 cursor-pointer">
                        <input
                          type="checkbox"
                          className="h-4 w-4 rounded border-slate-300 text-primary-600 focus:ring-primary-500"
                          defaultChecked={framework === 'SOC 2' || framework === 'ISO 27001' || framework === 'DPDP'}
                        />
                        <span className="text-sm text-slate-700">{framework}</span>
                      </label>
                    ))}
                  </div>
                </div>

                {/* Date Range */}
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Date Range
                  </label>
                  <select className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500">
                    <option value="last-quarter">Last Quarter (Oct - Dec 2026)</option>
                    <option value="custom">Custom Range</option>
                    <option value="ytd">Year to Date (Jan 2026 - Dec 2026)</option>
                    <option value="last-6-months">Last 6 Months</option>
                    <option value="last-12-months">Last 12 Months</option>
                  </select>
                </div>

                {/* Report Type */}
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Report Type
                  </label>
                  <div className="space-y-2">
                    {[
                      { id: 'summary', name: 'Executive Summary', desc: 'High-level overview for executives' },
                      { id: 'technical', name: 'Technical', desc: 'Detailed control and evidence analysis' },
                      { id: 'gap', name: 'Compliance Gap Analysis', desc: 'Identify gaps and remediation recommendations' },
                    ].map((type) => (
                      <label key={type.id} className="flex cursor-pointer rounded-lg border border-slate-200 p-3 hover:bg-slate-50">
                        <input
                          type="radio"
                          name="reportType"
                          className="mr-3 h-4 w-4 text-primary-600 border-slate-300"
                          defaultChecked={type.id === 'summary'}
                        />
                        <div>
                          <div className="font-medium text-slate-900">{type.name}</div>
                          <div className="text-xs text-slate-500">{type.desc}</div>
                        </div>
                      </label>
                    ))}
                  </div>
                </div>

                {/* Export Options */}
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Export Format
                  </label>
                  <div className="flex gap-2">
                    {[
                      { id: 'pdf', name: 'PDF' },
                      { id: 'csv', name: 'CSV' },
                      { id: 'excel', name: 'Excel' },
                    ].map((format) => (
                      <label key={format.id} className="flex items-center gap-2 cursor-pointer">
                        <input
                          type="checkbox"
                          className="h-4 w-4 rounded border-slate-300 text-primary-600 focus:ring-primary-500"
                          defaultChecked={format.id === 'pdf'}
                        />
                        <span className="text-sm text-slate-700">{format.name}</span>
                      </label>
                    ))}
                  </div>
                </div>

                <button className="w-full rounded-lg bg-primary-600 px-4 py-2 text-sm font-semibold text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2">
                  Generate Report
                </button>
              </div>
            </div>

            {/* Recent Reports */}
            <div className="rounded-lg border border-slate-200 bg-white p-6">
              <h3 className="text-lg font-semibold text-slate-900 mb-4">Recent Reports</h3>

              <div className="space-y-4">
                {[
                  { name: 'SOC 2 Type II Audit - Deloitte', date: 'Oct 15, 2026', size: '1.2 MB' },
                  { name: 'ISO 27001 Internal Audit - EY', date: 'Sep 28, 2026', size: '845 KB' },
                  { name: 'DPDP Annual Compliance - Grant Thornton', date: 'Aug 10, 2026', size: '512 KB' },
                  { name: 'CERT-In Security Audit - PwC', date: 'Jul 22, 2026', size: '2.1 MB' },
                ].map((report, idx) => (
                  <div key={idx} className="flex items-center justify-between rounded-lg border border-slate-200 p-3">
                    <div className="min-w-0">
                      <p className="text-sm font-medium text-slate-900 truncate">{report.name}</p>
                      <p className="text-xs text-slate-500">{report.date} • {report.size}</p>
                    </div>
                    <button
                      className="rounded-lg p-1.5 text-slate-400 hover:text-primary-600 hover:bg-primary-50"
                      title="Download"
                    >
                      <Download className="h-4 w-4" />
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}