'use client';

import './globals.css';
import { Inter } from 'next/font/google';
import { SessionProvider } from 'next-auth/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ThemeProvider } from 'next-themes';
import { Toaster } from 'sonner';
import { ReactNode, useState, useMemo, useCallback, type FC } from 'react';
import {
  Menu,
  X,
  Home,
  Shield,
  CheckCircle,
  Users,
  FileText,
  BarChart3,
  Settings as SettingsIcon,
  User,
  LogOut,
  Bell,
  Moon,
  Sun,
  ChevronDown
} from 'lucide-react';
import { cn } from '@/lib/utils';

const inter = Inter({ subsets: ['latin'] });

// Type definitions
interface NavItem {
  name: string;
  href: string;
  icon: FC<{ className?: string }>;
  roles: string[];
  protected?: boolean;
}

interface User {
  name: string;
  email: string;
  avatar: string;
  role: string;
}

interface RouteConfig {
  path: string;
  title: string;
  public?: boolean;
}

// Navigation items
const NAV_ITEMS: NavItem[] = [
  { name: 'Dashboard', href: '/dashboard', icon: Home, roles: ['Admin', 'Compliance Manager', 'Auditor', 'Viewer'] },
  { name: 'Frameworks', href: '/frameworks', icon: Shield, roles: ['Admin', 'Compliance Manager', 'Auditor'] },
  { name: 'Controls', href: '/controls', icon: CheckCircle, roles: ['Admin', 'Compliance Manager', 'Auditor'] },
  { name: 'Users', href: '/users', icon: Users, roles: ['Admin', 'Compliance Manager'] },
  { name: 'Risk Assessment', href: '/risk-assessment', icon: BarChart3, roles: ['Admin', 'Compliance Manager', 'Auditor'] },
  { name: 'Audits', href: '/audits', icon: FileText, roles: ['Admin', 'Compliance Manager', 'Auditor'] },
  { name: 'Settings', href: '/settings', icon: SettingsIcon, roles: ['Admin', 'Compliance Manager'] }
];

// Route configuration
const ROUTES: RouteConfig[] = [
  { path: '/login', title: 'Sign In', public: true },
  { path: '/register', title: 'Sign Up', public: true },
  { path: '/dashboard', title: 'Dashboard', public: false },
  { path: '/frameworks', title: 'Frameworks', public: false },
  { path: '/controls', title: 'Controls', public: false },
  { path: '/users', title: 'Users', public: false },
  { path: '/risk-assessment', title: 'Risk Assessment', public: false },
  { path: '/audits', title: 'Audits', public: false },
  { path: '/settings', title: 'Settings', public: false },
];

// Simulated current user (would normally come from session/context)
const CURRENT_USER: User = {
  name: 'Priya Sharma',
  email: 'priya.sharma@company.in',
  avatar: 'https://i.pravatar.cc/150?img=1',
  role: 'Admin'
};

export const metadata = {
  title: 'Sampati by VayuX',
  description: 'Open-source compliance automation platform built for India\'s regulators',
};

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000,
            retry: 1,
          },
        },
      })
  );

  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className} className="antialiased">
        <SessionProvider>
          <QueryClientProvider client={queryClient}>
            <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
              <AppShell>
                {children}
              </AppShell>
              <Toaster position="top-right" />
            </ThemeProvider>
          </QueryClientProvider>
        </SessionProvider>
      </body>
    </html>
  );
}

interface AppShellProps {
  children: ReactNode;
}

const AppShell: FC<AppShellProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  // Filter nav items based on user role
  const accessibleNavItems = useMemo(() => {
    return NAV_ITEMS.filter(item => item.roles.includes(CURRENT_USER.role));
  }, []);

  const handleLogout = useCallback(() => {
    // In a real app, this would call the signOut function from next-auth
    console.log('Signing out...');
  }, []);

  const toggleTheme = useCallback(() => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    // In a real app, this would use the theme provider's setTheme
    document.documentElement.classList.toggle('dark');
  }, [theme]);

  return (
    <div className="flex h-screen bg-slate-50">
      {/* Mobile sidebar backdrop */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/50 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside className={cn(
        "fixed inset-y-0 z-50 flex-col bg-white border-r border-slate-200 transition-transform duration-200",
        sidebarOpen ? "translate-x-0" : "-translate-x-full"
      )}>
        {/* Sidebar header */}
        <div className="flex items-center justify-between px-4 pt-4 pb-2 lg:pt-6 lg:pb-4">
          <div className="flex items-center gap-2">
            <Shield className="h-8 w-8 text-primary-600" />
            <span className="text-xl font-bold text-slate-900">Sampati</span>
          </div>
          <button
            className="rounded-lg p-2 text-slate-500 hover:bg-slate-100 lg:hidden"
            onClick={() => setSidebarOpen(false)}
            aria-label="Close sidebar"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* User role badge */}
        <div className="px-4 pb-2 lg:pb-4">
          <span className="inline-flex items-center rounded-full bg-primary-100 px-2.5 py-0.5 text-xs font-medium text-primary-800">
            {CURRENT_USER.role}
          </span>
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto px-2 pb-4">
          <ul className="space-y-1">
            {accessibleNavItems.map((item) => {
              const Icon = item.icon;
              const isActive = window.location.pathname === item.href;

              return (
                <li key={item.name}>
                  <a
                    href={item.href}
                    className={cn(
                      "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                      isActive
                        ? "bg-primary-50 text-primary-600"
                        : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                    )}
                    onClick={() => setSidebarOpen(false)}
                  >
                    <Icon className="h-5 w-5" />
                    {item.name}
                  </a>
                </li>
              );
            })}
          </ul>
        </nav>
      </aside>

      {/* Main content area */}
      <div className="flex flex-col flex-1 overflow-hidden">
        {/* Top navigation bar */}
        <header className="flex items-center justify-between bg-white border-b border-slate-200 px-4 py-3 lg:px-6">
          {/* Hamburger menu for mobile */}
          <button
            className="rounded-lg p-2 text-slate-500 hover:bg-slate-100 lg:hidden"
            onClick={() => setSidebarOpen(true)}
            aria-label="Open sidebar"
          >
            <Menu className="h-5 w-5" />
          </button>

          {/* Placeholder for page-specific header content */}
          <div className="hidden lg:block">
            {/* Could add breadcrumb or page title here */}
          </div>

          {/* User menu */}
          <div className="relative">
            <div>
              <button
                className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-slate-600 hover:bg-slate-100 focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <img
                  className="h-8 w-8 rounded-full object-cover"
                  src={CURRENT_USER.avatar}
                  alt={CURRENT_USER.name}
                />
                <div className="hidden text-left lg:block">
                  <div className="font-medium text-slate-900">{CURRENT_USER.name}</div>
                  <div className="text-xs text-slate-500">{CURRENT_USER.role}</div>
                </div>
                <ChevronDown className="h-4 w-4 hidden lg:block" />
              </button>
            </div>

            {/* Dropdown menu */}
            <div className="absolute right-0 z-50 mt-2 w-48 origin-top-right rounded-lg border border-slate-200 bg-white shadow-lg">
              <div className="py-1">
                <a
                  href="/settings"
                  className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm text-slate-700 hover:bg-slate-100"
                >
                  <SettingsIcon className="h-4 w-4" />
                  <span>Settings</span>
                </a>
                <button
                  className="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm text-slate-700 hover:bg-slate-100"
                  onClick={() => {/* Add notification logic here */}}
                >
                  <Bell className="h-4 w-4" />
                  <span>Notifications</span>
                </button>
                <div className="my-1 border-t border-slate-200"></div>
                <button
                  className="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm text-slate-700 hover:bg-slate-100"
                  onClick={handleLogout}
                >
                  <LogOut className="h-4 w-4" />
                  <span>Sign out</span>
                </button>
              </div>
            </div>
          </div>
        </header>

        {/* Main content */}
        <main className="flex-1 overflow-y-auto bg-slate-50">
          {children}
        </main>
      </div>
    </div>
  );
};

export { ROUTES, NAV_ITEMS, CURRENT_USER };