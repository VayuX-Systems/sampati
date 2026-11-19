import { Audit, Finding, Risk } from '@/types';

export interface DashboardStats {
  totalControls: number;
  passedControls: number;
  complianceScore: number;
  pendingFindings: number;
  nextAuditDate?: string;
  upcomingAudits: number;
}

export interface AuditStats {
  totalAudits: number;
  scheduled: number;
  inProgress: number;
  completed: number;
  overdue: number;
}

export interface FindingStats {
  total: number;
  critical: number;
  high: number;
  medium: number;
  low: number;
  open: number;
  resolved: number;
}

export interface RiskStats {
  total: number;
  highRisk: number;
  mediumRisk: number;
  lowRisk: number;
  mitigated: number;
}

export const MOCK_DASHBOARD_STATS: DashboardStats = {
  totalControls: 205,
  passedControls: 161,
  complianceScore: 87,
  pendingFindings: 12,
  nextAuditDate: '2026-11-28',
  upcomingAudits: 3,
};

export const MOCK_AUDIT_STATS: AuditStats = {
  totalAudits: 8,
  scheduled: 3,
  inProgress: 1,
  completed: 4,
  overdue: 0,
};

export const MOCK_FINDING_STATS: FindingStats = {
  total: 28,
  critical: 3,
  high: 7,
  medium: 12,
  low: 6,
  open: 18,
  resolved: 10,
};

export const MOCK_RISK_STATS: RiskStats = {
  total: 15,
  highRisk: 2,
  mediumRisk: 6,
  lowRisk: 7,
  mitigated: 4,
};

export interface ComplianceHistoryPoint {
  date: string;
  score: number;
}

export const MOCK_COMPLIANCE_HISTORY: ComplianceHistoryPoint[] = [
  { date: '2026-05-19', score: 82 },
  { date: '2026-06-19', score: 78 },
  { date: '2026-07-19', score: 85 },
  { date: '2026-08-19', score: 88 },
  { date: '2026-09-19', score: 84 },
  { date: '2026-10-19', score: 86 },
  { date: '2026-11-19', score: 87 },
];

export interface UpcomingEvent {
  id: string;
  title: string;
  date: string;
  type: 'audit' | 'deadline' | 'finding' | 'training';
  priority: 'low' | 'medium' | 'high' | 'critical';
}

export const MOCK_UPCOMING_EVENTS: UpcomingEvent[] = [
  {
    id: 'evt_1',
    title: 'ISO 27001 Internal Audit',
    date: '2026-11-28',
    type: 'audit',
    priority: 'high',
  },
  {
    id: 'evt_2',
    title: 'Privileged Access Control Remediation',
    date: '2026-11-25',
    type: 'finding',
    priority: 'critical',
  },
  {
    id: 'evt_3',
    title: 'PCI DSS Quarterly Assessment',
    date: '2026-12-01',
    type: 'audit',
    priority: 'critical',
  },
  {
    id: 'evt_4',
    title: 'Security Training Deadline',
    date: '2026-11-30',
    type: 'training',
    priority: 'medium',
  },
  {
    id: 'evt_5',
    title: 'Firewall Configuration Review',
    date: '2026-11-30',
    type: 'deadline',
    priority: 'high',
  },
];

export const getMockDashboardData = (): {
  stats: DashboardStats;
  auditStats: AuditStats;
  findingStats: FindingStats;
  riskStats: RiskStats;
  history: ComplianceHistoryPoint[];
  events: UpcomingEvent[];
} => ({
  stats: MOCK_DASHBOARD_STATS,
  auditStats: MOCK_AUDIT_STATS,
  findingStats: MOCK_FINDING_STATS,
  riskStats: MOCK_RISK_STATS,
  history: MOCK_COMPLIANCE_HISTORY,
  events: MOCK_UPCOMING_EVENTS,
});