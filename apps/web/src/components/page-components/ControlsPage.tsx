'use client';

import { useState } from 'react';
import { cn } from '@/lib/utils';
import {
  Shield,
  CheckCircle,
  AlertCircle,
  Clock,
  Download,
  Filter,
  Search
} from 'lucide-react';

interface Control {
  id: string;
  name: string;
  description: string;
  framework: string;
  evidenceCount: number;
  evidenceRequired: number;
  lastTested: Date | null;
  status: 'compliant' | 'non-compliant' | 'pending';
  owner: string;
  nextReview: Date;
  criticality: 'high' | 'medium' | 'low';
}

const CONTROLS: Control[] = [
  {
    id: 'C-001',
    name: 'Access Control - Admin Authentication',
    description: 'Multi-factor authentication for all administrator accounts',
    framework: 'ISO 27001',
    evidenceCount: 3,
    evidenceRequired: 3,
    lastTested: new Date('2026-11-15'),
    status: 'compliant',
    owner: 'Priya Sharma',
    nextReview: new Date('2027-05-15'),
    criticality: 'high'
  },
  {
    id: 'C-002',
    name: 'Access Control - User Provisioning',
    description: 'Automated user provisioning with role-based access control',
    framework: 'ISO 27001',
    evidenceCount: 2,
    evidenceRequired: 3,
    lastTested: new Date('2026-11-10'),
    status: 'pending',
    owner: 'Rajesh Kumar',
    nextReview: new Date('2027-02-10'),
    criticality: 'high'
  },
  {
    id: 'C-003',
    name: 'Access Control - Privileged Accounts',
    description: 'Management of privileged access with just-in-time approval',
    framework: 'ISO 27001',
    evidenceCount: 3,
    evidenceRequired: 3,
    lastTested: new Date('2026-11-12'),
    status: 'compliant',
    owner: 'Ananya Patel',
    nextReview: new Date('2027-05-12'),
    criticality: 'high'
  },
  {
    id: 'C-004',
    name: 'Incident Response - Plan',
    description: 'Incident response plan with defined roles and escalation paths',
    framework: 'ISO 27001',
    evidenceCount: 1,
    evidenceRequired: 3,
    lastTested: null,
    status: 'non-compliant',
    owner: 'Vikram Singh',
    nextReview: new Date('2026-12-01'),
    criticality: 'high'
  },
  {
    id: 'C-005',
    name: 'Data Encryption - At Rest',
    description: 'All sensitive data encrypted at rest using AES-256',
    framework: 'SOC 2',
    evidenceCount: 4,
    evidenceRequired: 4,
    lastTested: new Date('2026-11-18'),
    status: 'compliant',
    owner: 'Meera Iyer',
    nextReview: new Date('2027-05-18'),
    criticality: 'high'
  },
  {
    id: 'C-006',
    name: 'Data Encryption - In Transit',
    description: 'All data in transit encrypted using TLS 1.2+',
    framework: 'SOC 2',
    evidenceCount: 3,
    evidenceRequired: 3,
    lastTested: new Date('2026-11-16'),
    status: 'compliant',
    owner: 'Karthik Rao',
    nextReview: new Date('2027-05-16'),
    criticality: 'high'
  },
  {
    id: 'C-007',
    name: 'Vendor Risk Management',
    description: 'Third-party vendor risk assessments and monitoring',
    framework: 'SOC 2',
    evidenceCount: 0,
    evidenceRequired: 4,
    lastTested: null,
    status: 'non-compliant',
    owner: 'Shreya Joshi',
    nextReview: new Date('2026-11-28'),
    criticality: 'medium'
  },
  {
    id: 'C-008',
    name: 'Access Log Monitoring',
    description: 'Continuous monitoring and alerting of access logs',
    framework: 'ISO 27001',
    evidenceCount: 4,
    evidenceRequired: 4,
    lastTested: new Date('2026-11-18'),
    status: 'compliant',
    owner: 'Amit Trivedi',
    nextReview: new Date('2027-05-18'),
    criticality: 'medium'
  },
  {
    id: 'C-009',
    name: 'Security Awareness Training',
    description: 'Annual security awareness training for all employees',
    framework: 'ISO 27001',
    evidenceCount: 0,
    evidenceRequired: 3,
    lastTested: null,
    status: 'non-compliant',
    owner: 'Neha Verma',
    nextReview: new Date('2026-11-20'),
    criticality: 'medium'
  },
  {
    id: 'C-010',
    name: 'Backup and Recovery',
    description: 'Regular backups with tested recovery procedures',
    framework: 'DPDP',
    evidenceCount: 2,
    evidenceRequired: 3,
    lastTested: new Date('2026-11-14'),
    status: 'pending',
    owner: 'Deepak Patel',
    nextReview: new Date('2027-05-14'),
    criticality: 'medium'
  }
];

const FRAMEWORKS = ['ISO 27001', 'SOC 2', 'DPDP', 'CERT-In', 'RBI CSCRF'];
const STATUSES = ['All', 'Compliant', 'Pending', 'Non-Compliant'];
const CRITICALITIES = ['All', 'High', 'Medium', 'Low'];

export function ControlsPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [frameworkFilter, setFrameworkFilter] = useState('All');
  const [statusFilter, setStatusFilter] = useState('All');
  const [criticalityFilter, setCriticalityFilter] = useState('All');

  const filteredControls = CONTROLS.filter(control => {
    const matchesSearch =
      control.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      control.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      control.owner.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesFramework = frameworkFilter === 'All' || control.framework === frameworkFilter;

    const matchesStatus =
      statusFilter === 'All' ||
      (statusFilter === 'Compliant' && control.status === 'compliant') ||
      (statusFilter === 'Pending' && control.status === 'pending') ||
      (statusFilter === 'Non-Compliant' && control.status === 'non-compliant');

    const matchesCriticality =
      criticalityFilter === 'All' ||
      (criticalityFilter === 'High' && control.criticality === 'high') ||
      (criticalityFilter === 'Medium' && control.criticality === 'medium') ||
      (criticalityFilter === 'Low' && control.criticality === 'low');

    return matchesSearch && matchesFramework && matchesStatus && matchesCriticality;
  });

  const stats = {
    total: CONTROLS.length,
    compliant: CONTROLS.filter(c => c.status === 'compliant').length,
    pending: CONTROLS.filter(c => c.status === 'pending').length,
    nonCompliant: CONTROLS.filter(c => c.status === 'non-compliant').length
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8 flex flex-col justify-between gap-4 sm:items-center sm:flex-row">
          <div>
            <h1 className="text-3xl font-bold text-slate-900">Controls</h1>
            <p className="mt-1 text-sm text-slate-600">
              Manage compliance controls, track evidence, and monitor test results
            </p>
          </div>
          <button className="inline-flex items-center gap-2 rounded-lg bg-primary-600 px-4 py-2 text-sm font-semibold text-white hover:bg-primary-700">
            <Shield className="h-4 w-4" />
            <span>Add Control</span>
          </button>
        </div>

        {/* Stats Overview */}
        <div className="mb-8 grid grid-cols-1 gap-6 sm:grid-cols-4">
          <div className="rounded-lg border border-slate-200 bg-white p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-slate-600">Total Controls</p>
                <p className="text-2xl font-bold text-slate-900">{stats.total}</p>
              </div>
              <Shield className="h-8 w-8 text-primary-600" />
            </div>
          </div>
          <div className="rounded-lg border border-slate-200 bg-white p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-slate-600">Compliant</p>
                <p className="text-2xl font-bold text-emerald-600">{stats.compliant}</p>
              </div>
              <CheckCircle className="h-8 w-8 text-emerald-600" />
            </div>
          </div>
          <div className="rounded-lg border border-slate-200 bg-white p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-slate-600">Pending Evidence</p>
                <p className="text-2xl font-bold text-amber-600">{stats.pending}</p>
              </div>
              <Clock className="h-8 w-8 text-amber-600" />
            </div>
          </div>
          <div className="rounded-lg border border-slate-200 bg-white p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-slate-600">Non-Compliant</p>
                <p className="text-2xl font-bold text-red-600">{stats.nonCompliant}</p>
              </div>
              <AlertCircle className="h-8 w-8 text-red-600" />
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="mb-6">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
              <input
                type="text"
                placeholder="Search by control name, ID, or owner..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full rounded-lg border border-slate-300 bg-white pl-10 pr-4 py-2 text-sm shadow-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
              />
            </div>

            <div className="flex gap-3">
              <div className="relative">
                <Filter className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                <select
                  value={frameworkFilter}
                  onChange={(e) => setFrameworkFilter(e.target.value)}
                  className="relative w-40 rounded-lg border border-slate-300 bg-white pl-10 pr-4 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                >
                  <option value="All">All Frameworks</option>
                  {FRAMEWORKS.map(f => <option key={f} value={f}>{f}</option>)}
                </select>
              </div>

              <div className="relative">
                <Filter className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                <select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                  className="relative w-40 rounded-lg border border-slate-300 bg-white pl-10 pr-4 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                >
                  <option value="All">All Status</option>
                  <option value="Compliant">Compliant</option>
                  <option value="Pending">Pending</option>
                  <option value="Non-Compliant">Non-Compliant</option>
                </select>
              </div>

              <div className="relative">
                <Filter className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                <select
                  value={criticalityFilter}
                  onChange={(e) => setCriticalityFilter(e.target.value)}
                  className="relative w-40 rounded-lg border border-slate-300 bg-white pl-10 pr-4 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                >
                  <option value="All">All Criticality</option>
                  <option value="High">High</option>
                  <option value="Medium">Medium</option>
                  <option value="Low">Low</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        {/* Controls Table */}
        <div className="rounded-lg border border-slate-200 bg-white shadow-sm">
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-200 bg-slate-50">
                <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">
                  Control
                </th>
                <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">
                  Framework
                </th>
                <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">
                  Evidence
                </th>
                <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">
                  Owner
                </th>
                <th className="px-6 py-3 text-right text-xs font-semibold uppercase tracking-wider text-slate-600">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {filteredControls.map((control) => (
                <tr key={control.id} className="hover:bg-slate-50 transition-colors">
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className={cn(
                        "h-8 w-8 rounded-full flex items-center justify-center",
                        control.criticality === 'high' ? 'bg-red-100' :
                        control.criticality === 'medium' ? 'bg-amber-100' :
                        'bg-slate-100'
                      )}>
                        <Shield className={cn(
                          "h-4 w-4",
                          control.criticality === 'high' ? 'text-red-600' :
                          control.criticality === 'medium' ? 'text-amber-600' :
                          'text-slate-600'
                        )} />
                      </div>
                      <div>
                        <div className="font-medium text-slate-900">{control.id}</div>
                        <div className="text-xs text-slate-500">{control.name}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className="text-sm text-slate-700">{control.framework}</span>
                  </td>
                  <td className="px-6 py-4">
                    <span
                      className={cn(
                        "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium",
                        control.status === 'compliant' && 'bg-emerald-100 text-emerald-800',
                        control.status === 'pending' && 'bg-amber-100 text-amber-800',
                        control.status === 'non-compliant' && 'bg-red-100 text-red-800'
                      )}
                    >
                      {control.status === 'compliant' ? 'Compliant' :
                       control.status === 'pending' ? 'Pending' : 'Non-Compliant'}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span className="text-sm text-slate-600">
                      {control.evidenceCount} / {control.evidenceRequired}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span className="text-sm text-slate-600">{control.owner}</span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <div className="flex items-center gap-2">
                      <button
                        className="rounded-lg p-1.5 text-slate-400 hover:text-primary-600 hover:bg-primary-50"
                        title="View evidence"
                      >
                        <Download className="h-4 w-4" />
                      </button>
                      <button
                        className="rounded-lg p-1.5 text-slate-400 hover:text-primary-600 hover:bg-primary-50"
                        title="View details"
                      >
                        <Shield className="h-4 w-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* No results */}
        {filteredControls.length === 0 && (
          <div className="rounded-lg border border-slate-200 bg-white p-12 text-center">
            <Shield className="mx-auto h-12 w-12 text-slate-300" />
            <h3 className="mt-4 text-lg font-medium text-slate-900">No controls found</h3>
            <p className="mt-2 text-sm text-slate-600">
              Try adjusting your filters or search term.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}