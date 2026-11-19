export type AuditStatus = 'scheduled' | 'in-progress' | 'completed' | 'cancelled' | 'failed';

export type AuditType = 'internal' | 'external' | 'pre-assessment' | 'remediation' | 'continuous';

export type FindingSeverity = 'critical' | 'major' | 'minor';

export type FindingStatus = 'open' | 'in-progress' | 'resolved' | 'closed';

export type FindingStatusType = 'pass' | 'fail' | 'review';

export interface Audit {
  id: string;
  name: string;
  type: AuditType;
  status: AuditStatus;
  frameworkId: string;
  auditorId?: string;
  scheduledDate: string;
  actualStartDate?: string;
  actualEndDate?: string;
  durationHours?: number;
  readinessScore: number;
  findings: AuditFinding[];
  evidencePrepared: number;
  evidenceTotal: number;
  lastReportedAt?: string;
  nextScheduledDate?: string;
  createdAt: string;
  updatedAt: string;
}

export interface AuditFinding {
  id: string;
  auditId: string;
  controlId?: string;
  title: string;
  description: string;
  severity: FindingSeverity;
  status: FindingStatus;
  statusType: FindingStatusType;
  assignedTo?: string;
  dueDate?: string;
  createdAt: string;
  updatedAt: string;
}

export interface AuditReport {
  id: string;
  auditId: string;
  generatedAt: string;
  generatedBy: string;
  frameworkId: string;
  format: 'pdf' | 'csv' | 'excel';
  sections: AuditReportSection[];
  overallScore: number;
  executiveSummary?: string;
  downloadUrl?: string;
}

export interface AuditReportSection {
  id: string;
  name: string;
  pages: number;
  findingsCount: number;
}

export interface RemediationAction {
  id: string;
  findingId: string;
  description: string;
  assignedTo?: string;
  dueDate: string;
  status: 'pending' | 'in-progress' | 'completed' | 'overdue';
  createdAt: string;
  completedAt?: string;
}

export interface RemediationPlan {
  id: string;
  auditId: string;
  findings: RemediationAction[];
  createdAt: string;
  updatedAt: string;
  completionPercentage: number;
}

export interface AuditSearchParams {
  search?: string;
  status?: AuditStatus;
  type?: AuditType;
  frameworkId?: string;
  auditorId?: string;
  dateFrom?: string;
  dateTo?: string;
  sortBy?: keyof Audit;
  sortOrder?: 'asc' | 'desc';
  limit?: number;
  offset?: number;
}