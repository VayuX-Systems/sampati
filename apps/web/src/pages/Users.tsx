'use client';

import { useState, useMemo } from 'react';
import { Users, Search, Filter, Mail, User, Plus, X, Check, AlertCircle } from 'lucide-react';
import { format, isToday, isYesterday } from 'date-fns';
import { cn } from '@/lib/utils';

// Type definitions
type Role = 'Admin' | 'Compliance Manager' | 'Auditor' | 'Viewer';
type Status = 'Active' | 'Invited' | 'Offline';

interface User {
  id: string;
  name: string;
  email: string;
  avatar: string;
  role: Role;
  status: Status;
  lastLogin: Date | null;
  frameworks: string[];
  invitedAt?: Date;
}

// Sample data with 15 users
const sampleUsers: User[] = [
  {
    id: '1',
    name: 'Priya Sharma',
    email: 'priya.sharma@company.in',
    avatar: 'https://i.pravatar.cc/150?img=1',
    role: 'Admin',
    status: 'Active',
    lastLogin: new Date('2026-11-18T10:30:00'),
    frameworks: ['SOC 2', 'ISO 27001', 'DPDP', 'CERT-In'],
  },
  {
    id: '2',
    name: 'Rajesh Kumar',
    email: 'rajesh.kumar@company.in',
    avatar: 'https://i.pravatar.cc/150?img=2',
    role: 'Compliance Manager',
    status: 'Active',
    lastLogin: new Date('2026-11-19T08:15:00'),
    frameworks: ['DPDP', 'ISO 27001', 'RBI CSCRF'],
  },
  {
    id: '3',
    name: 'Ananya Patel',
    email: 'ananya.patel@company.in',
    avatar: 'https://i.pravatar.cc/150?img=3',
    role: 'Compliance Manager',
    status: 'Active',
    lastLogin: new Date('2026-11-17T16:45:00'),
    frameworks: ['SOC 2', 'CERT-In', 'SEBI CSCRF'],
  },
  {
    id: '4',
    name: 'Vikram Singh',
    email: 'vikram.singh@company.in',
    avatar: 'https://i.pravatar.cc/150?img=4',
    role: 'Auditor',
    status: 'Active',
    lastLogin: new Date('2026-11-19T09:00:00'),
    frameworks: ['DPDP', 'CERT-In'],
  },
  {
    id: '5',
    name: 'Meera Iyer',
    email: 'meera.iyer@company.in',
    avatar: 'https://i.pravatar.cc/150?img=5',
    role: 'Viewer',
    status: 'Active',
    lastLogin: new Date('2026-11-19T07:30:00'),
    frameworks: ['ISO 27001'],
  },
  {
    id: '6',
    name: 'Arjun Menon',
    email: 'arjun.menon@company.in',
    avatar: 'https://i.pravatar.cc/150?img=6',
    role: 'Admin',
    status: 'Offline',
    lastLogin: new Date('2026-11-16T14:20:00'),
    frameworks: ['SOC 2', 'ISO 27001', 'DPDP', 'CERT-In', 'RBI CSCRF', 'SEBI CSCRF', 'IRDAI'],
  },
  {
    id: '7',
    name: 'Sneha Reddy',
    email: 'sneha.reddy@company.in',
    avatar: 'https://i.pravatar.cc/150?img=7',
    role: 'Auditor',
    status: 'Active',
    lastLogin: new Date('2026-11-19T11:00:00'),
    frameworks: ['SOC 2', 'ISO 27001'],
  },
  {
    id: '8',
    name: 'Karthik Rao',
    email: 'karthik.rao@company.in',
    avatar: 'https://i.pravatar.cc/150?img=8',
    role: 'Compliance Manager',
    status: 'Active',
    lastLogin: new Date('2026-11-19T06:45:00'),
    frameworks: ['DPDP', 'CERT-In', 'RBI CSCRF', 'IRDAI'],
  },
  {
    id: '9',
    name: 'Pooja Nair',
    email: 'pooja.nair@company.in',
    avatar: 'https://i.pravatar.cc/150?img=9',
    role: 'Viewer',
    status: 'Active',
    lastLogin: new Date('2026-11-18T18:30:00'),
    frameworks: ['ISO 27001', 'SOC 2'],
  },
  {
    id: '10',
    name: 'Rohan Desai',
    email: 'rohan.desai@company.in',
    avatar: 'https://i.pravatar.cc/150?img=10',
    role: 'Admin',
    status: 'Invited',
    lastLogin: null,
    frameworks: ['DPDP'],
    invitedAt: new Date('2026-11-18T09:00:00'),
  },
  {
    id: '11',
    name: 'Shreya Joshi',
    email: 'shreya.joshi@company.in',
    avatar: 'https://i.pravatar.cc/150?img=11',
    role: 'Compliance Manager',
    status: 'Offline',
    lastLogin: new Date('2026-11-15T12:00:00'),
    frameworks: ['ISO 27001', 'SOC 2'],
  },
  {
    id: '12',
    name: 'Amit Trivedi',
    email: 'amit.trivedi@company.in',
    avatar: 'https://i.pravatar.cc/150?img=12',
    role: 'Auditor',
    status: 'Active',
    lastLogin: new Date('2026-11-19T05:15:00'),
    frameworks: ['DPDP', 'CERT-In', 'SEBI CSCRF'],
  },
  {
    id: '13',
    name: 'Neha Verma',
    email: 'neha.verma@company.in',
    avatar: 'https://i.pravatar.cc/150?img=13',
    role: 'Compliance Manager',
    status: 'Active',
    lastLogin: new Date('2026-11-19T09:30:00'),
    frameworks: ['ISO 27001', 'SOC 2', 'PCI DSS'],
  },
  {
    id: '14',
    name: 'Deepak Patel',
    email: 'deepak.patel@company.in',
    avatar: 'https://i.pravatar.cc/150?img=14',
    role: 'Viewer',
    status: 'Offline',
    lastLogin: new Date('2026-11-14T10:00:00'),
    frameworks: ['SOC 2'],
  },
  {
    id: '15',
    name: 'Fatima Khan',
    email: 'fatima.khan@company.in',
    avatar: 'https://i.pravatar.cc/150?img=15',
    role: 'Admin',
    status: 'Active',
    lastLogin: new Date('2026-11-19T12:00:00'),
    frameworks: ['DPDP', 'RBI CSCRF', 'IRDAI', 'CERT-In', 'ISO 27001'],
  },
];

// Available frameworks
const AVAILABLE_FRAMEWORKS = [
  'SOC 2',
  'ISO 27001',
  'DPDP',
  'CERT-In',
  'RBI CSCRF',
  'SEBI CSCRF',
  'IRDAI',
  'PCI DSS',
  'HIPAA',
  'GDPR',
];

// Role descriptions
const ROLE_DESCRIPTIONS: Record<Role, string> = {
  Admin: 'Full access, user management, settings',
  'Compliance Manager': 'Framework management, control assignment, evidence review',
  Auditor: 'Read-only access, audit reports, framework assessment',
  Viewer: 'Read-only dashboards, no editing capabilities',
};

// Role colors
const ROLE_COLORS: Record<Role, { bg: string; text: string; border: string; badge: string }> = {
  Admin: {
    bg: 'bg-primary-50',
    text: 'text-primary-700',
    border: 'border-primary-200',
    badge: 'bg-primary-100 text-primary-800',
  },
  'Compliance Manager': {
    bg: 'bg-emerald-50',
    text: 'text-emerald-700',
    border: 'border-emerald-200',
    badge: 'bg-emerald-100 text-emerald-800',
  },
  Auditor: {
    bg: 'bg-indigo-50',
    text: 'text-indigo-700',
    border: 'border-indigo-200',
    badge: 'bg-indigo-100 text-indigo-800',
  },
  Viewer: {
    bg: 'bg-slate-50',
    text: 'text-slate-700',
    border: 'border-slate-200',
    badge: 'bg-slate-100 text-slate-800',
  },
};

// Status colors
const STATUS_COLORS: Record<Status, { text: string; bg: string; dot: string }> = {
  Active: {
    text: 'text-emerald-600',
    bg: 'bg-emerald-50',
    dot: 'bg-emerald-500',
  },
  Invited: {
    text: 'text-amber-600',
    bg: 'bg-amber-50',
    dot: 'bg-amber-500',
  },
  Offline: {
    text: 'text-slate-600',
    bg: 'bg-slate-50',
    dot: 'bg-slate-400',
  },
};

export default function UsersPage() {
  const [users] = useState<User[]>(sampleUsers);
  const [searchTerm, setSearchTerm] = useState('');
  const [roleFilter, setRoleFilter] = useState<Role | 'All'>('All');
  const [statusFilter, setStatusFilter] = useState<Status | 'All'>('All');
  const [showInviteForm, setShowInviteForm] = useState(false);
  const [inviteEmail, setInviteEmail] = useState('');
  const [inviteRole, setInviteRole] = useState<Role>('Viewer');

  // Filter logic
  const filteredUsers = useMemo(() => {
    return users.filter((user) => {
      const matchesSearch =
        user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        user.email.toLowerCase().includes(searchTerm.toLowerCase());

      const matchesRole = roleFilter === 'All' || user.role === roleFilter;
      const matchesStatus = statusFilter === 'All' || user.status === statusFilter;

      return matchesSearch && matchesRole && matchesStatus;
    });
  }, [users, searchTerm, roleFilter, statusFilter]);

  // Role options
  const roleOptions: Role[] = ['Admin', 'Compliance Manager', 'Auditor', 'Viewer'];

  // Status options
  const statusOptions: Status[] = ['Active', 'Invited', 'Offline'];

  // Format last login date
  const formatLastLogin = (date: Date | null): string => {
    if (!date) return 'Never';

    if (isToday(date)) {
      return `Today, ${format(date, 'HH:mm')}`;
    }

    if (isYesterday(date)) {
      return `Yesterday, ${format(date, 'HH:mm')}`;
    }

    return format(date, 'PPP p');
  };

  // Handle invite submission
  const handleInviteSubmit = () => {
    if (!inviteEmail) return;
    // In a real app, this would call an API
    console.log('Inviting user:', { email: inviteEmail, role: inviteRole });
    setShowInviteForm(false);
    setInviteEmail('');
    setInviteRole('Viewer');
  };

  // Handle role change for a user
  const handleRoleChange = (userId: string, newRole: Role) => {
    console.log('Updating role for user:', userId, 'to:', newRole);
    // In a real app, this would call an API
  };

  // Handle framework assignment toggle
  const handleFrameworkToggle = (userId: string, framework: string) => {
    console.log('Toggling framework for user:', userId, 'framework:', framework);
    // In a real app, this would call an API
  };

  return (
    <div className="min-h-screen bg-slate-50 p-4 sm:p-6 lg:p-8">
      {/* Header */}
      <div className="mb-8 flex flex-col justify-between gap-4 sm:items-center sm:flex-row">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Users & Roles</h1>
          <p className="mt-1 text-sm text-slate-600">
            Manage team members, assign roles, and control access to compliance frameworks
          </p>
        </div>
        <button
          onClick={() => setShowInviteForm(true)}
          className="inline-flex items-center gap-2 rounded-lg bg-primary-600 px-4 py-2 text-sm font-semibold text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
        >
          <Plus className="h-4 w-4" />
          Invite New User
        </button>
      </div>

      {/* Filters and Search */}
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
          <input
            type="text"
            placeholder="Search by name or email..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full rounded-lg border border-slate-300 bg-white pl-10 pr-4 py-2 text-sm shadow-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
          />
        </div>

        <div className="flex gap-3">
          <div className="relative">
            <Filter className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
            <select
              value={roleFilter}
              onChange={(e) => setRoleFilter(e.target.value as Role | 'All')}
              className="relative w-40 rounded-lg border border-slate-300 bg-white pl-10 pr-4 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
            >
              <option value="All">All Roles</option>
              {roleOptions.map((role) => (
                <option key={role} value={role}>
                  {role}
                </option>
              ))}
            </select>
          </div>

          <div className="relative">
            <Filter className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value as Status | 'All')}
              className="relative w-32 rounded-lg border border-slate-300 bg-white pl-10 pr-4 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
            >
              <option value="All">All Status</option>
              {statusOptions.map((status) => (
                <option key={status} value={status}>
                  {status}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* User Count */}
      <div className="mb-6 text-sm text-slate-600">
        Showing {filteredUsers.length} of {users.length} users
      </div>

      {/* Users Table - Mobile Cards */}
      <div className="space-y-4 sm:space-y-0">
        {filteredUsers.map((user) => (
          <div
            key={user.id}
            className="rounded-lg border border-slate-200 bg-white shadow-sm sm:border-l-4 sm:border-l-primary-600"
          >
            {/* Mobile Card View */}
            <div className="p-4 sm:hidden">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <img
                    src={user.avatar}
                    alt={user.name}
                    className="h-10 w-10 rounded-full object-cover"
                  />
                  <div>
                    <h3 className="text-sm font-semibold text-slate-900">{user.name}</h3>
                    <p className="text-xs text-slate-500">{user.email}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span
                    className={cn(
                      'inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium',
                      ROLE_COLORS[user.role].badge
                    )}
                  >
                    {user.role}
                  </span>
                </div>
              </div>

              <div className="mt-4 space-y-3">
                {/* Status */}
                <div className="flex items-center gap-2">
                  <span
                    className={cn('h-2 w-2 rounded-full', STATUS_COLORS[user.status].dot)}
                  />
                  <span className={cn('text-sm', STATUS_COLORS[user.status].text)}>
                    {user.status}
                  </span>
                </div>

                {/* Last Login */}
                <div className="flex items-center gap-2 text-sm text-slate-600">
                  <User className="h-4 w-4" />
                  <span>{formatLastLogin(user.lastLogin)}</span>
                </div>

                {/* Frameworks */}
                <div>
                  <p className="text-xs font-medium text-slate-700 mb-2">Frameworks</p>
                  <div className="flex flex-wrap gap-1">
                    {user.frameworks.length > 0 ? (
                      user.frameworks.map((framework) => (
                        <span
                          key={framework}
                          className="inline-flex items-center rounded-full bg-slate-100 px-2 py-0.5 text-xs text-slate-600"
                        >
                          {framework}
                        </span>
                      ))
                    ) : (
                      <span className="text-xs text-slate-500">None assigned</span>
                    )}
                  </div>
                </div>

                {/* Role Selector */}
                <div>
                  <p className="text-xs font-medium text-slate-700 mb-2">Role</p>
                  <select
                    value={user.role}
                    onChange={(e) => handleRoleChange(user.id, e.target.value as Role)}
                    className="w-full rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-sm"
                  >
                    {roleOptions.map((role) => (
                      <option key={role} value={role}>
                        {role}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Framework Assignments */}
                <div>
                  <p className="text-xs font-medium text-slate-700 mb-2">Assign Frameworks</p>
                  <div className="flex max-h-40 flex-wrap gap-2 overflow-y-auto border border-slate-200 rounded-lg p-2">
                    {AVAILABLE_FRAMEWORKS.map((framework) => (
                      <label key={framework} className="flex items-center gap-1.5 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={user.frameworks.includes(framework)}
                          onChange={() => handleFrameworkToggle(user.id, framework)}
                          className="h-3 w-3 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                        />
                        <span className="text-xs text-slate-600">{framework}</span>
                      </label>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Desktop Table Cell */}
            <div className="hidden sm:table-cell">
              <div className="border-t border-slate-200 p-4 last:border-b-0 sm:border-l-0">
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-6">
                  {/* User Info */}
                  <div className="lg:col-span-2">
                    <div className="flex items-center gap-3">
                      <img
                        src={user.avatar}
                        alt={user.name}
                        className="h-10 w-10 rounded-full object-cover"
                      />
                      <div>
                        <h3 className="text-sm font-semibold text-slate-900">{user.name}</h3>
                        <p className="text-xs text-slate-500 flex items-center gap-1">
                          <Mail className="h-3 w-3" />
                          {user.email}
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Role */}
                  <div>
                    <select
                      value={user.role}
                      onChange={(e) => handleRoleChange(user.id, e.target.value as Role)}
                      className={cn(
                        'w-full rounded-lg border px-2 py-1.5 text-sm font-medium',
                        ROLE_COLORS[user.role].badge,
                        'focus:outline-none focus:ring-2 focus:ring-primary-500'
                      )}
                    >
                      {roleOptions.map((role) => (
                        <option key={role} value={role} className={ROLE_COLORS[role].badge}>
                          {role}
                        </option>
                      ))}
                    </select>
                  </div>

                  {/* Status */}
                  <div>
                    <span
                      className={cn(
                        'inline-flex items-center gap-1.5 rounded-full px-2 py-0.5 text-xs font-medium',
                        STATUS_COLORS[user.status].badge
                      )}
                    >
                      <span
                        className={cn(
                          'h-2 w-2 rounded-full',
                          STATUS_COLORS[user.status].dot
                        )}
                      />
                      {user.status}
                    </span>
                  </div>

                  {/* Last Login */}
                  <div>
                    <span className="text-sm text-slate-600">{formatLastLogin(user.lastLogin)}</span>
                  </div>

                  {/* Frameworks */}
                  <div>
                    <div className="flex flex-wrap gap-1">
                      {user.frameworks.length > 0 ? (
                        user.frameworks.slice(0, 3).map((framework) => (
                          <span
                            key={framework}
                            className="inline-flex items-center rounded-full bg-slate-100 px-2 py-0.5 text-xs text-slate-600"
                          >
                            {framework}
                          </span>
                        ))
                      ) : (
                        <span className="text-xs text-slate-500">None</span>
                      )}
                      {user.frameworks.length > 3 && (
                        <span className="text-xs text-slate-500">
                          +{user.frameworks.length - 3} more
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => {}}
                      className="rounded-lg p-1.5 text-slate-400 hover:text-primary-600 hover:bg-primary-50"
                      title="View details"
                    >
                      <User className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Desktop Table View */}
      <div className="hidden rounded-lg border border-slate-200 bg-white shadow-sm lg:block">
        <table className="w-full">
          <thead>
            <tr className="border-b border-slate-200 bg-slate-50">
              <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">
                User
              </th>
              <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">
                Role
              </th>
              <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">
                Last Login
              </th>
              <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">
                Frameworks
              </th>
              <th className="px-6 py-3 text-right text-xs font-semibold uppercase tracking-wider text-slate-600">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200">
            {filteredUsers.map((user) => (
              <tr key={user.id} className="hover:bg-slate-50 transition-colors">
                <td className="px-6 py-4">
                  <div className="flex items-center gap-3">
                    <img
                      src={user.avatar}
                      alt={user.name}
                      className="h-10 w-10 rounded-full object-cover"
                    />
                    <div>
                      <div className="font-medium text-slate-900">{user.name}</div>
                      <div className="text-xs text-slate-500">{user.email}</div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <select
                    value={user.role}
                    onChange={(e) => handleRoleChange(user.id, e.target.value as Role)}
                    className={cn(
                      'w-32 rounded-lg border px-2 py-1.5 text-sm font-medium',
                      ROLE_COLORS[user.role].badge,
                      'focus:outline-none focus:ring-2 focus:ring-primary-500'
                    )}
                  >
                    {roleOptions.map((role) => (
                      <option key={role} value={role}>
                        {role}
                      </option>
                    ))}
                  </select>
                </td>
                <td className="px-6 py-4">
                  <span
                    className={cn(
                      'inline-flex items-center gap-1.5 rounded-full px-2 py-0.5 text-xs font-medium',
                      STATUS_COLORS[user.status].badge
                    )}
                  >
                    <span
                      className={cn(
                        'h-2 w-2 rounded-full',
                        STATUS_COLORS[user.status].dot
                      )}
                    />
                    {user.status}
                  </span>
                </td>
                <td className="px-6 py-4">
                  <span className="text-sm text-slate-600">{formatLastLogin(user.lastLogin)}</span>
                </td>
                <td className="px-6 py-4">
                  <div className="flex flex-wrap gap-1">
                    {user.frameworks.length > 0 ? (
                      user.frameworks.slice(0, 3).map((framework) => (
                        <span
                          key={framework}
                          className="inline-flex items-center rounded-full bg-slate-100 px-2 py-0.5 text-xs text-slate-600"
                        >
                          {framework}
                        </span>
                      ))
                    ) : (
                      <span className="text-xs text-slate-500">None</span>
                    )}
                    {user.frameworks.length > 3 && (
                      <span className="text-xs text-slate-500">
                        +{user.frameworks.length - 3} more
                      </span>
                    )}
                  </div>
                </td>
                <td className="px-6 py-4 text-right">
                  <button
                    onClick={() => {}}
                    className="rounded-lg p-1.5 text-slate-400 hover:text-primary-600 hover:bg-primary-50"
                    title="View details"
                  >
                    <User className="h-4 w-4" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* No results */}
      {filteredUsers.length === 0 && (
        <div className="rounded-lg border border-slate-200 bg-white p-12 text-center">
          <AlertCircle className="mx-auto h-12 w-12 text-slate-300" />
          <h3 className="mt-4 text-lg font-medium text-slate-900">No users found</h3>
          <p className="mt-2 text-sm text-slate-600">
            Try adjusting your search or filter criteria.
          </p>
        </div>
      )}

      {/* Invite Modal */}
      {showInviteForm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div className="w-full max-w-md rounded-lg border border-slate-200 bg-white p-6 shadow-xl">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-slate-900">Invite New User</h2>
              <button
                onClick={() => setShowInviteForm(false)}
                className="rounded-full p-1 text-slate-400 hover:text-slate-600"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            <div className="mt-6 space-y-4">
              <div>
                <label
                  htmlFor="email"
                  className="block text-sm font-medium text-slate-700"
                >
                  Email Address
                </label>
                <div className="mt-1">
                  <input
                    type="email"
                    id="email"
                    value={inviteEmail}
                    onChange={(e) => setInviteEmail(e.target.value)}
                    placeholder="user@example.com"
                    className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                  />
                </div>
              </div>

              <div>
                <label
                  htmlFor="role"
                  className="block text-sm font-medium text-slate-700"
                >
                  Role
                </label>
                <div className="mt-1">
                  <select
                    id="role"
                    value={inviteRole}
                    onChange={(e) => setInviteRole(e.target.value as Role)}
                    className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                  >
                    {roleOptions.map((role) => (
                      <option key={role} value={role}>
                        {role}
                      </option>
                    ))}
                  </select>
                </div>
                <p className="mt-1 text-xs text-slate-500">
                  {ROLE_DESCRIPTIONS[inviteRole]}
                </p>
              </div>
            </div>

            <div className="mt-6 flex justify-end gap-3">
              <button
                type="button"
                onClick={() => setShowInviteForm(false)}
                className="rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleInviteSubmit}
                disabled={!inviteEmail}
                className={cn(
                  'inline-flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-semibold transition-colors',
                  inviteEmail
                    ? 'bg-primary-600 text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2'
                    : 'bg-slate-100 text-slate-400 cursor-not-allowed'
                )}
              >
                <Check className="h-4 w-4" />
                Send Invitation
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Role Legend */}
      <div className="mt-8 rounded-lg border border-slate-200 bg-white p-4">
        <h3 className="text-sm font-medium text-slate-700 mb-3">Role Permissions</h3>
        <div className="grid gap-3 sm:grid-cols-2">
          {roleOptions.map((role) => (
            <div key={role} className="flex items-start gap-3">
              <span
                className={cn(
                  'inline-flex h-2 w-2 rounded-full',
                  ROLE_COLORS[role].dot
                )}
              />
              <div>
                <p className="text-sm font-medium text-slate-900">{role}</p>
                <p className="text-xs text-slate-500">{ROLE_DESCRIPTIONS[role]}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}