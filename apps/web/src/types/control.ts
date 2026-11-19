export type ControlStatus = 'pass' | 'fail' | 'review' | 'pending' | 'not_applicable';

export type ControlCategory = 'access-control' | 'incident-response' | 'data-protection' | 'network-security' | 'system-configuration' | 'third-party' | 'monitoring' | 'other';

export type EvidenceStatus = 'valid' | 'expired' | 'pending-review' | 'invalid';

export interface Control {
  id: string;
  name: string;
  description: string;
  category: ControlCategory;
  frameworkId: string;
  standardId?: string;
  isCustom: boolean;
  status: ControlStatus;
  evidenceCount: number;
  evidenceAttached: boolean;
  lastUpdatedBy?: string;
  lastUpdatedAt: string;
  nextReviewDate?: string;
  dueDate?: string;
  ownerId?: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
  tags: string[];
  requirements: ControlRequirement[];
  createdAt: string;
  updatedAt: string;
}

export interface ControlRequirement {
  id: string;
  description: string;
  evidenceRequired: boolean;
  evidenceType?: EvidenceType;
  dueDate?: string;
  completed: boolean;
}

export interface Evidence {
  id: string;
  controlId: string;
  name: string;
  type: EvidenceType;
  mimeType: string;
  fileSize: number;
  url?: string;
  storagePath?: string;
  description?: string;
  attachedAt: string;
  attachedBy: string;
  expiryDate?: string;
  status: EvidenceStatus;
  verified: boolean;
  verificationNotes?: string;
  tags: string[];
  version: number;
  createdAt: string;
  updatedAt: string;
}

export type EvidenceType = 'policy' | 'procedure' | 'screenshot' | 'log' | 'report' | 'certificate' | 'assessment' | 'training' | 'contract' | 'other';

export const EVIDENCE_TYPE_LABELS: Record<EvidenceType, string> = {
  policy: 'Policy Document',
  procedure: 'Procedure Document',
  screenshot: 'Screenshot/Image',
  log: 'Log File',
  report: 'Report',
  certificate: 'Certificate',
  assessment: 'Assessment',
  training: 'Training Record',
  contract: 'Contract',
  other: 'Other Document',
};

export interface ControlGroup {
  id: string;
  name: string;
  description: string;
  controls: Control[];
  createdAt: string;
}

export interface ControlSearchParams {
  search?: string;
  frameworkId?: string;
  status?: ControlStatus;
  category?: ControlCategory;
  ownerId?: string;
  dateFrom?: string;
  dateTo?: string;
  sortBy?: keyof Control;
  sortOrder?: 'asc' | 'desc';
  limit?: number;
  offset?: number;
}