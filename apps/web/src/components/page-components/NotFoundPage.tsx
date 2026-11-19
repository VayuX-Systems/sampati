'use client';

import { useRouter } from 'next/navigation';
import { Home, ArrowLeft, Search } from 'lucide-react';

export function NotFoundPage() {
  const router = useRouter();

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center">
      <div className="mx-auto max-w-md px-4 py-8 text-center">
        <div className="mb-6">
          <div className="inline-flex h-20 w-20 items-center justify-center rounded-full bg-primary-100 mb-4">
            <Search className="h-10 w-10 text-primary-600" />
          </div>
          <h1 className="text-4xl font-bold text-slate-900 mb-2">Page Not Found</h1>
          <p className="text-slate-600">
            The page you're looking for doesn't exist or has been moved.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-3 mb-8">
          <button
            onClick={() => router.back()}
            className="inline-flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
          >
            <ArrowLeft className="h-4 w-4" />
            Go Back
          </button>
          <button
            onClick={() => router.push('/dashboard')}
            className="inline-flex items-center gap-2 rounded-lg bg-primary-600 px-4 py-2 text-sm font-semibold text-white hover:bg-primary-700"
          >
            <Home className="h-4 w-4" />
            Go to Dashboard
          </button>
        </div>

        <div className="text-sm text-slate-500">
          <p>Need help? Contact support or use the navigation above.</p>
        </div>
      </div>
    </div>
  );
}