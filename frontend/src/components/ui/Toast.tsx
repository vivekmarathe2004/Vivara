import React from 'react';
import { useToast } from '../../hooks/useToast';
import { XCircle, CheckCircle, Info, X } from 'lucide-react';

export const ToastContainer: React.FC = () => {
  const { toasts, removeToast } = useToast();

  return (
    <div className="fixed bottom-4 right-4 z-50 flex flex-col gap-2">
      {toasts.map((toast) => (
        <div
          key={toast.id}
          className="flex items-center p-4 glass-card shadow-lg border-l-4 min-w-[300px] animate-fade-in"
          style={{
            borderLeftColor:
              toast.type === 'success'
                ? 'var(--color-success)'
                : toast.type === 'error'
                ? 'var(--color-error)'
                : 'var(--color-accent)',
          }}
        >
          <div className="mr-3">
            {toast.type === 'success' && <CheckCircle className="text-success w-5 h-5" />}
            {toast.type === 'error' && <XCircle className="text-error w-5 h-5" />}
            {toast.type === 'info' && <Info className="text-accent w-5 h-5" />}
          </div>
          <div className="flex-1 text-sm font-medium">{toast.message}</div>
          <button
            onClick={() => removeToast(toast.id)}
            className="ml-3 text-textMuted hover:text-text transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      ))}
    </div>
  );
};
