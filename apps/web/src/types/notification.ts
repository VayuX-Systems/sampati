export type NotificationType =
  | 'compliance-alert'
  | 'deadline-reminder'
  | 'audit-scheduled'
  | 'finding-identified'
  | 'control-failed'
  | 'evidence-expiring'
  | 'user-invited'
  | 'system-update'
  | 'risk-alert';

export type NotificationChannel = 'email' | 'slack' | 'sms' | 'in-app';

export interface Notification {
  id: string;
  type: NotificationType;
  title: string;
  message: string;
  channel: NotificationChannel;
  recipientId: string;
  recipientName: string;
  recipientEmail: string;
  isRead: boolean;
  createdAt: string;
  readAt?: string;
  link?: string;
  metadata?: Record<string, unknown>;
}

export interface NotificationPreferences {
  userId: string;
  channels: Partial<Record<NotificationType, NotificationChannel[]>>;
  muteAll: boolean;
  lastMutedAt?: string;
  updatedAt: string;
}

export interface InAppNotification {
  id: string;
  title: string;
  message: string;
  link?: string;
  type: NotificationType;
  createdAt: string;
  isRead: boolean;
}