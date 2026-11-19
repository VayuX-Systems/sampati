'use client';

import { useState, useMemo } from 'react';
import {
  Users,
  Phone,
  Mail,
  Folder,
  Shield,
  Lock,
  Clock,
  Globe,
  Settings,
  Photo,
  Upload,
  Cloud,
  GitHub,
  Slack,
  CheckCircle,
  X,
  Calendar,
  AlertCircle,
  TrendingUp,
  Package,
  CreditCard,
  FolderLock,
  Globe,
  Users2,
  Mail as MailIcon,
  Settings as SettingsIcon,
  Shield as ShieldIcon,
  Lock as LockIcon,
} from 'lucide-react';
import { format, parseISO, isToday, isTomorrow, formatDistance } from 'date-fns';
import { cn } from '@/lib/utils';

// ============ Type Definitions ============

type OrgSettingKey = 'companyName' | 'supportEmail' | 'phone' | 'timezone' | 'locale' | 'dateFormat';

type TwoFactorStatus = 'enabled' | 'disabled';

interface OrgSettingsState {
  companyName: string;
  logoUrl: string | null;
  supportEmail: string;
  phone: string;
  timezone: string;
  locale: string;
  dateFormat: 'MM/DD/YYYY' | 'DD/MM/YYYY' | 'YYYY-MM-DD';
}

interface SecuritySettingsState {
  twoFactor: TwoFactorStatus;
  sessionTimeout: number; // in minutes
  ssoEnabled: boolean;
  ssoUrl: string;
  apiTokens: ApiToken[];
}

interface ApiToken {
  id: string;
  name: string;
  lastUsed: Date | null;
  expiresAt: Date | null;
  revocable: boolean;
}

interface IntegrationSettingsState {
  awsStatus: 'connected' | 'disconnected' | 'error';
  gcpStatus: 'connected' | 'disconnected' | 'error';
  azureStatus: 'connected' | 'disconnected' | 'error';
  githubSync: 'synced' | 'pending' | 'error';
  slackSync: 'synced' | 'pending' | 'error';
  webhookUrl: string;
  apiKeys: ApiKey[];
}

interface ApiKey {
  id: string;
  name: string;
  lastUsed: Date | null;
  expiresAt: Date | null;
  revocable: boolean;
}

interface NotificationSettingsState {
  emailNotifications: EmailNotificationSettings;
  slackNotifications: SlackNotificationSettings;
  smsNotifications: boolean;
  notificationSchedule: 'business-hours' | '24x7';
}

interface EmailNotificationSettings {
  complianceAlerts: boolean;
  deadlineReminders: boolean;
  auditUpdates: boolean;
}

interface SlackNotificationSettings {
  enabled: boolean;
  channel: string;
}

// ============ Sample Data ============

const sampleOrgSettings: OrgSettingsState = {
  companyName: 'Acme Corp',
  logoUrl: null,
  supportEmail: 'support@acme.com',
  phone: '+1 (555) 123-4567',
  timezone: 'America/New_York',
  locale: 'en-US',
  dateFormat: 'MM/DD/YYYY',
};

const sampleSecuritySettings: SecuritySettingsState = {
  twoFactor: 'enabled',
  sessionTimeout: 30,
  ssoEnabled: true,
  ssoUrl: 'https://login.acme.com',
  apiTokens: [
    {
      id: 'token-1',
      name: 'API Token - Production',
      lastUsed: new Date('2026-11-18T14:30:00'),
      expiresAt: new Date('2027-05-18T23:59:59'),
      revocable: true,
    },
    {
      id: 'token-2',
      name: 'API Token - Staging',
      lastUsed: new Date('2026-11-15T09:15:00'),
      expiresAt: new Date('2027-02-15T23:59:59'),
      revocable: true,
    },
  ],
};

const sampleIntegrationSettings: IntegrationSettingsState = {
  awsStatus: 'connected',
  gcpStatus: 'disconnected',
  azureStatus: 'connected',
  githubSync: 'synced',
  slackSync: 'pending',
  webhookUrl: 'https://hooks.acme.com/compliance',
  apiKeys: [
    {
      id: 'key-1',
      name: 'AWS Key',
      lastUsed: new Date('2026-11-19T08:00:00'),
      expiresAt: new Date('2027-11-19T23:59:59'),
      revocable: true,
    },
  ],
};

const sampleNotificationSettings: NotificationSettingsState = {
  emailNotifications: {
    complianceAlerts: true,
    deadlineReminders: true,
    auditUpdates: false,
  },
  slackNotifications: {
    enabled: true,
    channel: '#compliance-alerts',
  },
  smsNotifications: false,
  notificationSchedule: 'business-hours',
};

// ============ Settings Page ============

export default function SettingsPage() {
  const [orgSettings, setOrgSettings] = useState<OrgSettingsState>(sampleOrgSettings);
  const [securitySettings, setSecuritySettings] = useState<SecuritySettingsState>(sampleSecuritySettings);
  const [integrationSettings, setIntegrationSettings] = useState<IntegrationSettingsState>(sampleIntegrationSettings);
  const [notificationSettings, setNotificationSettings] = useState<NotificationSettingsState>(sampleNotificationSettings);

  // Format last used date
  const formatLastUsed = (date: Date | null): string => {
    if (!date) return 'Never';
    if (isToday(date)) {
      return `Today, ${format(date, 'HH:mm')}`;
    }
    if (isTomorrow(date)) {
      return `Tomorrow, ${format(date, 'HH:mm')}`;
    }
    return format(date, 'PPP');
  };

  return (
    <div className="min-h-screen bg-slate-50 p-4 sm:p-6 lg:p-8">
      {/* Header */}
      <div className="mb-8 flex flex-col sm:flex-row justify-between items-start gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Settings</h1>
          <p className="mt-1 text-sm text-slate-600">
            Configure organization preferences, security, integrations, and billing
          </p>
        </div>
        <nav className="flex gap-2">
          <button className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 transition-colors">
            General
          </button>
          <button className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 transition-colors active">
            Security
          </button>
          <button className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 transition-colors">
            Integrations
          </button>
          <button className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 transition-colors">
            Notifications
          </button>
          <button className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 transition-colors">
            Billing
          </button>
          <button className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 transition-colors">
            Privacy
          </button>
        </nav>
      </div>

      {/* Tabs Content */}
      <div className="mt-8 space-y-8">

        {/* ============ General Settings Tab ============ */}
        <div>
          <h2 className="text-xl font-semibold text-slate-900 mb-6">Organization Settings</h2>

          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">

            {/* Company Name */}
            <div>
              <label htmlFor="companyName" className="block text-sm font-medium text-slate-700 mb-2">
                Company Name
              </label>
              <div className="relative">
                <input
                  id="companyName"
                  type="text"
                  value={orgSettings.companyName}
                  onChange={(e) => setOrgSettings((o) => ({ ...o, companyName: e.target.value }))}
                  className="w-full rounded-lg border border-slate-300 bg-white pl-3 py-2.5 text-sm shadow-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                  placeholder="Acme Corp"
                />
              </div>
            </div>

            {/* Logo Upload */}
            <div>
              <label htmlFor="logoUpload" className="block text-sm font-medium text-slate-700 mb-2">
                Logo
              </label>
              <div className="relative">
                <input
                  id="logoUpload"
                  type="file"
                  className="hidden"
                  onChange={(e) => {
                    const file = e.target.files?.[0];
                    if (file && file.type.startsWith('image/')) {
                      const reader = new FileReader();
                      reader.onload = (event) => {
                        setOrgSettings((o) => ({ ...o, logoUrl: event.target?.result as string }));
                      };
                      reader.readAsDataURL(file);
                    }
                  }}
                />
                <button
                  className="flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-600 hover:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500"
                  onClick={() => document.getElementById('logoUpload')?.click()}
                >
                  <Upload className="h-4 w-4" />
                  <span>Upload Logo</span>
                </button>
                {orgSettings.logoUrl && (
                  <div className="mt-2 flex items-center gap-2 text-xs text-slate-500">
                    <img
                      src={orgSettings.logoUrl}
                      alt="Company logo"
                      className="h-6 w-6 rounded"
                    />
                    <span>Logo uploaded</span>
                  </div>
                )}
              </div>
            </div>

            {/* Support Email */}
            <div>
              <label htmlFor="supportEmail" className="block text-sm font-medium text-slate-700 mb-2">
                Support Email
              </label>
              <div className="relative">
                <input
                  id="supportEmail"
                  type="email"
                  value={orgSettings.supportEmail}
                  onChange={(e) => setOrgSettings((o) => ({ ...o, supportEmail: e.target.value }))}
                  className="w-full rounded-lg border border-slate-300 bg-white pl-3 py-2.5 text-sm shadow-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                  placeholder="support@acme.com"
                />
              </div>
            </div>

            {/* Phone */}
            <div>
              <label htmlFor="phone" className="block text-sm font-medium text-slate-700 mb-2">
                Phone
              </label>
              <div className="relative">
                <input
                  id="phone"
                  type="tel"
                  value={orgSettings.phone}
                  onChange={(e) => setOrgSettings((o) => ({ ...o, phone: e.target.value }))}
                  className="w-full rounded-lg border border-slate-300 bg-white pl-3 py-2.5 text-sm shadow-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                  placeholder="+1 (555) 123-4567"
                />
              </div>
            </div>

            {/* Timezone */}
            <div>
              <label htmlFor="timezone" className="block text-sm font-medium text-slate-700 mb-2">
                Timezone
              </label>
              <div className="relative">
                <select
                  id="timezone"
                  value={orgSettings.timezone}
                  onChange={(e) => setOrgSettings((o) => ({ ...o, timezone: e.target.value }))}
                  className="w-full rounded-lg border border-slate-300 bg-white pl-3 py-2.5 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                >
                  <option value="America/New_York">America/New York (EST)</option>
                  <option value="America/Los_Angeles">America/Los Angeles (PST)</option>
                  <option value="UTC">UTC</option>
                  <option value="Europe/London">Europe/London (GMT)</option>
                  <option value="Asia/Kolkata">Asia/Kolkata (IST)</option>
                  <option value="Asia/Tokyo">Asia/Tokyo (JST)</option>
                  <option value="Australia/Sydney">Australia/Sydney (AEST)</option>
                </select>
              </div>
            </div>

            {/* Locale */}
            <div>
              <label htmlFor="locale" className="block text-sm font-medium text-slate-700 mb-2">
                Locale
              </label>
              <div className="relative">
                <select
                  id="locale"
                  value={orgSettings.locale}
                  onChange={(e) => setOrgSettings((o) => ({ ...o, locale: e.target.value }))}
                  className="w-full rounded-lg border border-slate-300 bg-white pl-3 py-2.5 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                >
                  <option value="en-US">English (US)</option>
                  <option value="en-GB">English (UK)</option>
                  <option value="en-IN">English (India)</option>
                  <option value="fr-FR">Français (France)</option>
                  <option value="de-DE">Deutsch (Germany)</option>
                  <option value="es-ES">Español (Spain)</option>
                </select>
              </div>
            </div>

            {/* Date Format */}
            <div>
              <label htmlFor="dateFormat" className="block text-sm font-medium text-slate-700 mb-2">
                Date Format
              </label>
              <div className="relative">
                <select
                  id="dateFormat"
                  value={orgSettings.dateFormat}
                  onChange={(e) => setOrgSettings((o) => ({ ...o, dateFormat: e.target.value as any }))}
                  className="w-full rounded-lg border border-slate-300 bg-white pl-3 py-2.5 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                >
                  <option value="MM/DD/YYYY">MM/DD/YYYY</option>
                  <option value="DD/MM/YYYY">DD/MM/YYYY</option>
                  <option value="YYYY-MM-DD">YYYY-MM-DD</option>
                </select>
              </div>
            </div>

          </div>
        </div>

        {/* ============ Security Settings Tab ============ */}
        <div>
          <h2 className="text-xl font-semibold text-slate-900 mb-6">Security Settings</h2>

          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">

            {/* Two-Factor Authentication */}
            <div>
              <label className="flex items-center gap-3 mb-4">
                <input
                  type="checkbox"
                  checked={securitySettings.twoFactor === 'enabled'}
                  onChange={() => setSecuritySettings((s) => ({ ...s, twoFactor: securitySettings.twoFactor === 'enabled' ? 'disabled' : 'enabled' }))}
                  className="rounded border-primary-500 w-5 h-5 focus:ring-primary-500"
                />
                <span className="text-sm font-medium text-slate-900">Two-Factor Authentication</span>
              </label>
              <p className="text-xs text-slate-500 mt-1">
                Require second verification method for sign-in. Users will need to
                enter a code from their authenticator app or receive an SMS code.
              </p>
            </div>

            {/* Session Timeout */}
            <div>
              <label htmlFor="sessionTimeout" className="block text-sm font-medium text-slate-700 mb-2">
                Session Timeout
              </label>
              <div className="relative">
                <select
                  id="sessionTimeout"
                  value={securitySettings.sessionTimeout}
                  onChange={(e) => setSecuritySettings((s) => ({ ...s, sessionTimeout: parseInt(e.target.value) }))}
                  className="w-full rounded-lg border border-slate-300 bg-white pl-3 py-2.5 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                >
                  <option value="15">15 minutes</option>
                  <option value="30">30 minutes</option>
                  <option value="60">60 minutes</option>
                  <option value="120">2 hours</option>
                  <option value="360">6 hours</option>
                  <option value="720">12 hours</option>
                </select>
              </div>
              <p className="text-xs text-slate-500 mt-1">
                Users will be automatically logged out after this period of inactivity.
              </p>
            </div>

            {/* SSO/SAML */}
            <div>
              <label className="flex items-center gap-3 mb-4">
                <input
                  type="checkbox"
                  checked={securitySettings.ssoEnabled}
                  onChange={() => setSecuritySettings((s) => ({ ...s, ssoEnabled: !securitySettings.ssoEnabled }))}
                  className="rounded border-primary-500 w-5 h-5 focus:ring-primary-500"
                />
                <span className="text-sm font-medium text-slate-900">SSO / SAML</span>
              </label>
              {securitySettings.ssoEnabled && (
                <div className="mt-3 p-4 rounded-lg border-b-primary-500 bg-primary-50 text-sm text-slate-800">
                  <div className="flex items-center gap-2 mb-2">
                    <Globe className="h-4 w-4 text-primary-600" />
                    <span>SSO URL</span>
                  </div>
                  <input
                    type="text"
                    value={securitySettings.ssoUrl}
                    onChange={(e) => setSecuritySettings((s) => ({ ...s, ssoUrl: e.target.value }))}
                    className="w-full rounded-lg border border-slate-300 bg-white pl-3 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                    placeholder="https://login.acme.com"
                  />
                  <p className="mt-2 text-xs text-slate-500">
                    Users will be redirected to this URL for authentication.
                  </p>
                </div>
              )}
            </div>

            {/* API Access Tokens */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-3">
                API Access Tokens
              </label>
              <p className="text-xs text-slate-500 mb-3">
                Manage API tokens for third-party integrations. Rotate tokens regularly
                and revoke unused credentials.
              </p>

              {/* Token List */}
              <div className="rounded-lg border border-slate-200 bg-white p-4 mb-4">
                {securitySettings.apiTokens.map((token) => (
                  <div
                    key={token.id}
                    className="flex items-center justify-between p-3 rounded-lg border border-slate-200 bg-slate-50"
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-sm font-medium text-slate-900">{token.name}</span>
                      <span className="text-xs text-slate-500 ml-3">{token.revocable ? 'Revocable' : 'Managed'}</span>
                    </div>
                    <div className="text-right text-xs text-slate-500">
                      <span>Last used: {formatLastUsed(token.lastUsed)}</span>
                      {token.expiresAt && (
                        <span className="ml-2">
                          • Expires: {format(token.expiresAt, 'MMM d, yyyy')}
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>

              <div className="flex gap-2">
                <button
                  className="flex-1 rounded-lg border border-primary-500 px-3 py-2 text-xs font-medium text-primary-600 hover:bg-primary-50 focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  Generate Token
                </button>
              </div>
            </div>

            {/* Password Policy */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Password Policy
              </label>
              <div className="space-y-3 text-sm text-slate-600">
                <div className="flex items-center justify-between">
                  <span>Minimum length</span>
                  <span className="font-medium text-slate-900">8 characters</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Require uppercase</span>
                  <span className="font-medium text-slate-900">Yes</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Require numbers</span>
                  <span className="font-medium text-slate-900">Yes</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Require special chars</span>
                  <span className="font-medium text-slate-900">Yes</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Password expiry</span>
                  <span className="font-medium text-slate-900">90 days</span>
                </div>
              </div>
            </div>

          </div>
        </div>

        {/* ============ Integration Settings Tab ============ */}
        <div>
          <h2 className="text-xl font-semibold text-slate-900 mb-6">Integration Settings</h2>

          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">

            {/* AWS */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-3">
                AWS Cloud Provider
              </label>
              <div className={cn(
                'flex items-center gap-3 rounded-lg p-3',
                securitySettings.awsStatus === 'connected' && 'bg-green-50 border-green-200 text-green-600',
                securitySettings.awsStatus === 'disconnected' && 'bg-red-50 border-red-200 text-red-600',
                securitySettings.awsStatus === 'error' && 'bg-yellow-50 border-yellow-200 text-yellow-600'
              )}>
                <Cloud className="h-4 w-4" />
                <span>
                  {securitySettings.awsStatus}: {securitySettings.awsStatus === 'connected' ? '12 connectors active' : 'Not connected'}
                </span>
              </div>
              <button
                className="mt-2 w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-600 hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                Connect AWS
              </button>
            </div>

            {/* GCP */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-3">
                GCP Cloud Provider
              </label>
              <div className={cn(
                'flex items-center gap-3 rounded-lg p-3',
                securitySettings.gcpStatus === 'connected' && 'bg-green-50 border-green-200 text-green-600',
                securitySettings.gcpStatus === 'disconnected' && 'bg-red-50 border-red-200 text-red-600',
                securitySettings.gcpStatus === 'error' && 'bg-yellow-50 border-yellow-200 text-yellow-600'
              )}>
                <Cloud className="h-4 w-4" />
                <span>
                  {securitySettings.gcpStatus}: {securitySettings.gcpStatus === 'connected' ? '8 connectors active' : 'Not connected'}
                </span>
              </div>
              <button
                className="mt-2 w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-600 hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                Connect GCP
              </button>
            </div>

            {/* Azure */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-3">
                Azure Cloud Provider
              </label>
              <div className={cn(
                'flex items-center gap-3 rounded-lg p-3',
                securitySettings.azureStatus === 'connected' && 'bg-green-50 border-green-200 text-green-600',
                securitySettings.azureStatus === 'disconnected' && 'bg-red-50 border-red-200 text-red-600',
                securitySettings.azureStatus === 'error' && 'bg-yellow-50 border-yellow-200 text-yellow-600'
              )}>
                <Cloud className="h-4 w-4" />
                <span>
                  {securitySettings.azureStatus}: {securitySettings.azureStatus === 'connected' ? '10 connectors active' : 'Not connected'}
                </span>
              </div>
              <button
                className="mt-2 w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-600 hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                Connect Azure
              </button>
            </div>

            {/* GitHub */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-3">
                GitHub Integration
              </label>
              <div className={cn(
                'flex items-center gap-3 rounded-lg p-3',
                integrationSettings.githubSync === 'synced' && 'bg-green-50 border-green-200 text-green-600',
                integrationSettings.githubSync === 'pending' && 'bg-amber-50 border-amber-200 text-amber-600',
                integrationSettings.githubSync === 'error' && 'bg-red-50 border-red-200 text-red-600'
              )}>
                <GitHub className="h-4 w-4" />
                <span>
                  {integrationSettings.githubSync}: {integrationSettings.githubSync === 'synced' ? 'Synced' : integrationSettings.githubSync === 'pending' ? 'Pending' : 'Error'}
                </span>
              </div>
              <button
                className="mt-2 w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-600 hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                Re-sync GitHub
              </button>
            </div>

            {/* Slack */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-3">
                Slack Integration
              </label>
              <div className={cn(
                'flex items-center gap-3 rounded-lg p-3',
                integrationSettings.slackSync === 'synced' && 'bg-green-50 border-green-200 text-green-600',
                integrationSettings.slackSync === 'pending' && 'bg-amber-50 border-amber-200 text-amber-600',
                integrationSettings.slackSync === 'error' && 'bg-red-50 border-red-200 text-red-600'
              )}>
                <Slack className="h-4 w-4" />
                <span>
                  {integrationSettings.slackSync}: {integrationSettings.slackSync === 'synced' ? 'Connected' : integrationSettings.slackSync === 'pending' ? 'Pending' : 'Error'}
                </span>
              </div>
              <button
                className="mt-2 w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-600 hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                Re-authenticate
              </button>
            </div>

            {/* Webhook */}
            <div>
              <label htmlFor="webhookUrl" className="block text-sm font-medium text-slate-700 mb-2">
                Webhook URL
              </label>
              <div className="relative">
                <input
                  id="webhookUrl"
                  type="text"
                  value={integrationSettings.webhookUrl}
                  onChange={(e) => setIntegrationSettings((i) => ({ ...i, webhookUrl: e.target.value }))}
                  className="w-full rounded-lg border border-slate-300 bg-white pl-3 py-2.5 text-sm shadow-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                  placeholder="https://hooks.acme.com/compliance"
                />
                <button
                  type="button"
                  className="absolute right-3 top-1/2 -translate-y-1/2 rounded-lg bg-primary-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-primary-700"
                >
                  Test Webhook
                </button>
              </div>
            </div>

            {/* API Keys */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-3">
                API Keys
              </label>
              <p className="text-xs text-slate-500 mb-3">
                Securely store and rotate API keys for cloud providers and services.
              </p>

              {/* API Key List */}
              <div className="rounded-lg border border-slate-200 bg-white p-4 mb-4">
                {integrationSettings.apiKeys.map((key) => (
                  <div
                    key={key.id}
                    className="flex items-center justify-between p-3 rounded-lg border border-slate-200 bg-slate-50"
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-sm font-medium text-slate-900">{key.name}</span>
                      <span className="text-xs text-slate-500 ml-3">{key.revocable ? 'Revocable' : 'Managed'}</span>
                    </div>
                    <div className="text-right text-xs text-slate-500">
                      <span>Last used: {formatLastUsed(key.lastUsed)}</span>
                      {key.expiresAt && (
                        <span className="ml-2">
                          • Expires: {format(key.expiresAt, 'MMM d, yyyy')}
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>

              <div className="flex gap-2">
                <button
                  className="flex-1 rounded-lg border border-primary-500 px-3 py-2 text-xs font-medium text-primary-600 hover:bg-primary-50 focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  Add API Key
                </button>
              </div>
            </div>

          </div>
        </div>

        {/* ============ Notification Preferences Tab ============ */}
        <div>
          <h2 className="text-xl font-semibold text-slate-900 mb-6">Notification Preferences</h2>

          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">

            {/* Email Notifications */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-3">
                Email Notifications
              </label>
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <input
                    type="checkbox"
                    checked={notificationSettings.emailNotifications.complianceAlerts}
                    onChange={() =>
                      setNotificationSettings((n) => ({
                        ...n,
                        emailNotifications: {
                          ...n.emailNotifications,
                          complianceAlerts: !n.emailNotifications.complianceAlerts,
                        },
                      }))
                    }
                    className="rounded border-primary-500 w-5 h-5 focus:ring-primary-500"
                  />
                  <span className="text-sm font-medium text-slate-900">
                    Compliance alerts
                  </span>
                </div>
                <div className="flex items-center gap-3">
                  <input
                    type="checkbox"
                    checked={notificationSettings.emailNotifications.deadlineReminders}
                    onChange={() =>
                      setNotificationSettings((n) => ({
                        ...n,
                        emailNotifications: {
                          ...n.emailNotifications,
                          deadlineReminders: !n.emailNotifications.deadlineReminders,
                        },
                      }))
                    }
                    className="rounded border-primary-500 w-5 h-5 focus:ring-primary-500"
                  />
                  <span className="text-sm font-medium text-slate-900">
                    Deadline reminders
                  </span>
                </div>
                <div className="flex items-center gap-3">
                  <input
                    type="checkbox"
                    checked={notificationSettings.emailNotifications.auditUpdates}
                    onChange={() =>
                      setNotificationSettings((n) => ({
                        ...n,
                        emailNotifications: {
                          ...n.emailNotifications,
                          auditUpdates: !n.emailNotifications.auditUpdates,
                        },
                      }))
                    }
                    className="rounded border-primary-500 w-5 h-5 focus:ring-primary-500"
                  />
                  <span className="text-sm font-medium text-slate-900">
                    Audit updates
                  </span>
                </div>
              </div>
            </div>

            {/* Slack Notifications */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-3">
                Slack Notifications
              </label>
              <div className="flex items-center gap-3">
                <input
                  type="checkbox"
                  checked={notificationSettings.slackNotifications.enabled}
                  onChange={() =>
                    setNotificationSettings((n) => ({
                      ...n,
                      slackNotifications: {
                        ...n.slackNotifications,
                        enabled: !n.slackNotifications.enabled,
                      }),
                    })
                  }
                  className="rounded border-primary-500 w-5 h-5 focus:ring-primary-500"
                />
                <span className="text-sm font-medium text-slate-900">Enable Slack notifications</span>
              </div>
              {notificationSettings.slackNotifications.enabled && (
                <div className="mt-3 p-3 rounded-lg border border-slate-300 bg-slate-50 text-sm">
                  <div className="flex items-center gap-2">
                    <Slack className="h-4 w-4" />
                    <span>Channel:</span>
                    <input
                      type="text"
                      value={notificationSettings.slackNotifications.channel}
                      onChange={(e) =>
                        setNotificationSettings((n) => ({
                          ...n,
                          slackNotifications: {
                            ...n.slackNotifications,
                            channel: e.target.value,
                          },
                        }))
                      }
                      className="flex-1 rounded-lg border border-slate-300 bg-white px-2 py-1 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                      placeholder="#compliance-alerts"
                    />
                  </div>
                  <p className="mt-1 text-xs text-slate-500">
                    Notify about compliance deadlines and audit updates
                  </p>
                </div>
              )}
            </div>

            {/* SMS Notifications */}
            <div>
              <label className="flex items-center gap-3 mb-4">
                <input
                  type="checkbox"
                  checked={notificationSettings.smsNotifications}
                  onChange={() =>
                    setNotificationSettings((n) => ({
                      ...n,
                      smsNotifications: !n.smsNotifications,
                    }))
                  }
                  className="rounded border-primary-500 w-5 h-5 focus:ring-primary-500"
                />
                <span className="text-sm font-medium text-slate-900">SMS notifications</span>
              </label>
              <p className="text-xs text-slate-500">
                SMS alerts for critical compliance events and deadline reminders. Standard
                messaging rates may apply.
              </p>
            </div>

            {/* Notification Schedule */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-3">
                Notification Schedule
              </label>
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <input
                    type="radio"
                    id="schedule-business"
                    name="notificationSchedule"
                    value="business-hours"
                    checked={notificationSettings.notificationSchedule === 'business-hours'}
                    onChange={() =>
                      setNotificationSettings((n) => ({
                        ...n,
                        notificationSchedule: 'business-hours',
                      }))
                    }
                    className="rounded border-primary-500 w-5 h-5 focus:ring-primary-500"
                  />
                  <label htmlFor="schedule-business" className="text-sm font-medium text-slate-700">
                    Business hours (9 AM - 5 PM local time)
                  </label>
                </div>
                <div className="flex items-center gap-3">
                  <input
                    type="radio"
                    id="schedule-24x7"
                    name="notificationSchedule"
                    value="24x7"
                    checked={notificationSettings.notificationSchedule === '24x7'}
                    onChange={() =>
                      setNotificationSettings((n) => ({
                        ...n,
                        notificationSchedule: '24x7',
                      }))
                    }
                    className="rounded border-primary-500 w-5 h-5 focus:ring-primary-500"
                  />
                  <label htmlFor="schedule-24x7" className="text-sm font-medium text-slate-700">
                    24 hours a day, 7 days a week
                  </label>
                </div>
              </div>
            </div>

          </div>
        </div>

        {/* ============ Billing & Subscription Tab ============ */}
        <div>
          <h2 className="text-xl font-semibold text-slate-900 mb-6">Billing & Subscription</h2>

          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">

            {/* Current Plan */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-3">
                Current Plan
              </label>
              <div className="rounded-lg border rounded-b-xl border-slate-300 bg-white p-4">
                <div className="flex items-center gap-3 mb-3">
                  <div className="h-8 w-8 rounded-lg bg-primary-100 flex items-center justify-center">
                    <Package className="h-4 w-4 text-primary-600" />
                  </div>
                  <div>
                    <p className="text-lg font-bold text-slate-900">Professional</p>
                    <p className="text-sm text-slate-500">Monthly</p>
                  </div>
                </div>
                <p className="text-xs text-slate-500">
                  50 users, 200 controls, unlimited connectors
                </p>
                <button
                  className="mt-2 w-full rounded-lg border border-primary-600 bg-primary-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  Change Plan
                </button>
              </div>
            </div>

            {/* Usage Statistics */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-3">
                Usage Statistics
              </label>
              <div className="grid grid-cols-2 gap-4">
                <div className="rounded-lg border border-slate-200 bg-white p-4">
                  <p className="text-sm font-medium text-slate-700">Controls</p>
                  <p className="text-2xl font-bold text-slate-900">1,247</p>
                  <p className="text-xs text-slate-500">/ 5,000 max</p>
                </div>
                <div className="rounded-lg border border-slate-200 bg-white p-4">
                  <p className="text-sm font-medium text-slate-700">Users</p>
                  <p className="text-2xl font-bold text-slate-900">34</p>
                  <p className="text-xs text-slate-500">/ 50 max</p>
                </div>
                <div className="rounded-lg border border-slate-200 bg-white p-4">
                  <p className="text-sm font-medium text-slate-700">Connectors</p>
                  <p className="text-2xl font-bold text-slate-900">15</p>
                  <p className="text-xs text-slate-500">/ 25 max</p>
                </div>
              </div>
            </div>

            {/* Billing History */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-3">
                Billing History
              </label>
              <div className="rounded-lg border border-slate-200 bg-white p-4">
                <div className="flex items-between justify-between mb-2">
                  <span className="text-sm font-medium text-slate-700">Nov 2026</span>
                  <span className="text-right text-sm text-slate-500">$4,500</span>
                </div>
                <div className="flex items-between justify-between mb-2">
                  <span className="text-sm font-medium text-slate-700">Oct 2026</span>
                  <span className="text-right text-sm text-slate-500">$4,500</span>
                </div>
                <div className="flex items-between justify-between mb-2">
                  <span className="text-sm font-medium text-slate-700">Sep 2026</span>
                  <span className="text-right text-sm text-slate-500">$4,500</span>
                </div>
                <button
                  className="mt-2 w-full rounded-lg border border-primary-600 bg-primary-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500"
                  style={{ marginTop: '8px' }}>
                  View All Invoices
                </button>
              </div>
            </div>

          </div>
        </div>

        {/* ============ Privacy & Compliance Tab ============ */}
        <div>
          <h2 className="text-xl font-semibold text-slate-900 mb-6">Privacy & Compliance</h2>

          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">

            {/* Data Processing Agreement */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-3">
                Data Processing Agreement
              </label>
              <div className="rounded-lg border border-slate-200 bg-white p-4">
                <div className="flex items-center gap-3 mb-3">
                  <input
                    type="checkbox"
                    className="rounded border-primary-500 w-4 h-4 focus:ring-primary-500"
                  />
                  <span className="text-sm font-medium text-slate-900">
                    Accept DPA terms
                  </span>
                </div>
                <p className="text-xs text-slate-500">
                  By accepting, you agree to the data processing terms for your organization.
                  This data will be processed in accordance with applicable privacy laws.
                </p>
                <button
                  className="mt-2 w-full rounded-lg border border-primary-500 bg-primary-50 px-3 py-1.5 text-xs font-medium text-primary-600 hover:bg-primary-100 focus:outline-none focus:ring-2 focus:ring-primary-500"
                  style={{ marginTop: '8px' }}>
                  View Full DPA
                </button>
              </div>
            </div>

            {/* Cookie Policy */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-3">
                Cookie Policy
              </label>
              <div className="rounded-lg border border-slate-200 bg-white p-4">
                <p className="text-xs text-slate-500">
                  Our cookie policy explains how we use cookies and similar technologies to
                  improve your experience. <a href="#" className="text-primary-600 hover:underline">View policy</a>
                </p>
              </div>
            </div>

            {/* Data Retention */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-3">
                Data Retention Settings
              </label>
              <div className="space-y-3 text-sm text-slate-600">
                <div className="flex items-center justify-between">
                  <span>Retention period for audit logs</span>
                  <span className="font-medium text-slate-900">7 years</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Retention period for evidence files</span>
                  <span className="font-medium text-slate-900">3 years</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Retention period for session data</span>
                  <span className="font-medium text-slate-900">30 days</span>
                </div>
              </div>
            </div>

            {/* GDPR/CCPA Compliance */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-3">
                GDPR / CCPA Compliance
              </label>
              <div className="grid grid-cols-2 gap-3">
                <div className="rounded-lg border border-slate-200 bg-white p-3">
                  <p className="text-xs font-medium text-slate-700">GDPR</p>
                  <p className="text-xs text-slate-500">Data subject rights enabled</p>
                </div>
                <div className="rounded-lg border border-slate-200 bg-white p-3">
                  <p className="text-xs font-medium text-slate-700">CCPA</p>
                  <p className="text-xs text-slate-500">Opt-out mechanism active</p>
                </div>
                <div className="rounded-lg border border-slate-200 bg-white p-3">
                  <p className="text-xs font-medium text-slate-700">Portability</p>
                  <p className="text-xs text-slate-500">Export API available</p>
                </div>
                <div className="rounded-lg border border-slate-200 bg-white p-3">
                  <p className="text-xs font-medium text-slate-700">Deletion</p>
                  <p className="text-xs text-slate-500">Bulk delete supported</p>
                </div>
              </div>
            </div>

          </div>
        </div>

      </div>
    </div>
  );
}