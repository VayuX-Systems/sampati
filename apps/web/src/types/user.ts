export type Role = 'admin' | 'compliance-manager' | 'auditor' | 'viewer';

export type Permission =
  | 'users:read'
  | 'users:write'
  | 'users:delete'
  | 'frameworks:read'
  | 'frameworks:write'
  | 'frameworks:delete'
  | 'controls:read'
  | 'controls:write'
  | 'controls:delete'
  | 'evidence:read'
  | 'evidence:write'
  | 'evidence:delete'
  | 'audits:read'
  | 'audits:write'
  | 'audits:delete'
  | 'risks:read'
  | 'risks:write'
  | 'risks:delete'
  | 'reports:read'
  | 'reports:write'
  | 'reports:delete'
  | 'settings:read'
  | 'settings:write';

export const ROLE_PERMISSIONS: Record<Role, Permission[]> = {
  admin: [
    'users:read',
    'users:write',
    'users:delete',
    'frameworks:read',
    'frameworks:write',
    'frameworks:delete',
    'controls:read',
    'controls:write',
    'controls:delete',
    'evidence:read',
    'evidence:write',
    'evidence:delete',
    'audits:read',
    'audits:write',
    'audits:delete',
    'risks:read',
    'risks:write',
    'risks:delete',
    'reports:read',
    'reports:write',
    'reports:delete',
    'settings:read',
    'settings:write',
  ],
  'compliance-manager': [
    'users:read',
    'frameworks:read',
    'frameworks:write',
    'controls:read',
    'controls:write',
    'evidence:read',
    'evidence:write',
    'audits:read',
    'audits:write',
    'risks:read',
    'risks:write',
    'reports:read',
    'reports:write',
    'settings:read',
  ],
  auditor: [
    'users:read',
    'frameworks:read',
    'controls:read',
    'evidence:read',
    'audits:read',
    'audits:write',
    'risks:read',
    'reports:read',
    'reports:write',
  ],
  viewer: [
    'users:read',
    'frameworks:read',
    'controls:read',
    'evidence:read',
    'audits:read',
    'risks:read',
    'reports:read',
  ],
};

export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  role: Role;
  permissions: Permission[];
  department?: string;
  title?: string;
  phone?: string;
  isActive: boolean;
  lastLoginAt?: string;
  createdAt: string;
  updatedAt: string;
  mfaEnabled: boolean;
  preferredLanguage: string;
  timezone: string;
}

export interface Team {
  id: string;
  name: string;
  description?: string;
  members: User[];
  createdAt: string;
  updatedAt: string;
}

export interface Organization {
  id: string;
  name: string;
  domain: string;
  logo?: string;
  industry: string;
  size: 'startup' | 'small' | 'medium' | 'large' | 'enterprise';
  address?: string;
  phone?: string;
  website?: string;
  complianceContact?: User;
  settings: OrganizationSettings;
  createdAt: string;
  updatedAt: string;
}

export interface OrganizationSettings {
  allowSelfRegistration: boolean;
  requireMfa: boolean;
  sessionTimeoutMinutes: number;
  passwordPolicy: PasswordPolicy;
  evidenceRetentionDays: number;
  auditLogRetentionDays: number;
  defaultFrameworkIds: string[];
  notificationChannels: NotificationChannel[];
  integrations: IntegrationConfig[];
}

export interface PasswordPolicy {
  minLength: number;
  requireUppercase: boolean;
  requireLowercase: boolean;
  requireNumbers: boolean;
  requireSpecialChars: boolean;
  maxAgeDays: number;
  preventReuseCount: number;
}

export interface NotificationChannel {
  id: string;
  type: 'email' | 'slack' | 'sms' | 'webhook';
  name: string;
  config: Record<string, unknown>;
  isActive: boolean;
}

export interface IntegrationConfig {
  id: string;
  type: 'aws' | 'gcp' | 'azure' | 'github' | 'gitlab' | 'jira' | 'servicenow' | 'okta' | 'entra-id' | 'splunk' | 'datadog';
  name: string;
  config: Record<string, unknown>;
  isActive: boolean;
  lastSyncAt?: string;
}
