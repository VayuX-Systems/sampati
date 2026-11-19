export type ComplianceStatus = 'compliant' | 'non-compliant' | 'in-progress' | 'not-started' | 'at-risk';

export type FrameworkCategory = 'security' | 'privacy' | 'finance' | 'healthcare' | 'government' | 'other';

export interface Framework {
  id: string;
  name: string;
  code: string;
  description: string;
  category: FrameworkCategory;
  version: string;
  status: ComplianceStatus;
  totalControls: number;
  passedControls: number;
  failedControls: number;
  pendingControls: number;
  complianceScore: number;
  firstAuditDate?: string;
  nextAuditDate?: string;
  lastAuditDate?: string;
  auditFrequencyMonths: number;
  ownerId: string;
  tags: string[];
  customControls: number;
  createdAt: string;
  updatedAt: string;
}

export interface FrameworkCategoryConfig {
  id: string;
  name: string;
  code: string;
  description: string;
  icon: string;
  defaultControls: number;
}

export const FRAMEWORK_CATEGORIES: FrameworkCategoryConfig[] = [
  { id: 'security', name: 'Security', code: 'SEC', description: 'Information security standards', defaultControls: 100, icon: 'shield' },
  { id: 'privacy', name: 'Privacy', code: 'PRIV', description: 'Data privacy regulations', defaultControls: 50, icon: 'lock' },
  { id: 'finance', name: 'Financial', code: 'FIN', description: 'Financial industry standards', defaultControls: 75, icon: 'bank' },
  { id: 'healthcare', name: 'Healthcare', code: 'HC', description: 'Healthcare regulations', defaultControls: 80, icon: 'stethoscope' },
  { id: 'government', name: 'Government', code: 'GOV', description: 'Government compliance', defaultControls: 60, icon: 'government' },
];

export const STANDARD_FRAMEWORKS: Partial<Framework>[] = [
  { name: 'SOC 2 Type II', code: 'SOC2-T2', description: 'Trust Services Criteria', category: 'security', version: '2017', totalControls: 108, auditFrequencyMonths: 12 },
  { name: 'ISO 27001', code: 'ISO27001', description: 'Information Security Management', category: 'security', version: '2022', totalControls: 93, auditFrequencyMonths: 36 },
  { name: 'GDPR', code: 'GDPR', description: 'General Data Protection Regulation', category: 'privacy', version: '2018', totalControls: 45, auditFrequencyMonths: 36 },
  { name: 'HIPAA', code: 'HIPAA', description: 'Health Insurance Portability', category: 'healthcare', version: '2003', totalControls: 52, auditFrequencyMonths: 36 },
  { name: 'PCI DSS', code: 'PCI-DSS', description: 'Payment Card Industry', category: 'finance', version: '4.0', totalControls: 67, auditFrequencyMonths: 12 },
  { name: 'DPDP Act', code: 'DPDP', description: 'Digital Personal Data Protection Act', category: 'privacy', version: '2023', totalControls: 45, auditFrequencyMonths: 36 },
  { name: 'CERT-In', code: 'CERTIN', description: 'Indian Cyber Security Guidelines', category: 'security', version: '2024', totalControls: 52, auditFrequencyMonths: 12 },
  { name: 'RBI CSCRF', code: 'RBI-CSCRF', description: 'Reserve Bank of India Cyber Security', category: 'finance', version: '2024', totalControls: 58, auditFrequencyMonths: 12 },
];