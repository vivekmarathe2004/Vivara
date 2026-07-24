import React from 'react';
import { LucideIcon } from 'lucide-react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement | HTMLTextAreaElement> {
  label?: string;
  error?: string;
  icon?: LucideIcon;
  multiline?: boolean;
}

export const Input = React.forwardRef<HTMLInputElement | HTMLTextAreaElement, InputProps>(
  ({ label, error, icon: Icon, multiline, className = '', ...props }, ref) => {
    const Component = multiline ? 'textarea' : 'input';
    
    return (
      <div className="w-full">
        {label && (
          <label className="block text-sm font-medium text-text mb-1.5">
            {label}
          </label>
        )}
        <div className="relative">
          {Icon && !multiline && (
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Icon className="h-5 w-5 text-textMuted" />
            </div>
          )}
          <Component
            // @ts-ignore
            ref={ref}
            className={`
              w-full bg-surface border border-border rounded-lg text-text 
              placeholder:text-textMuted focus:outline-none focus:ring-2 focus:ring-accent/50 focus:border-accent
              transition-colors disabled:opacity-50 disabled:cursor-not-allowed
              ${Icon && !multiline ? 'pl-10' : 'pl-3'}
              ${multiline ? 'py-3 min-h-[100px] resize-y' : 'h-11'}
              ${error ? 'border-error focus:ring-error/50 focus:border-error' : ''}
              ${className}
            `}
            {...props}
          />
        </div>
        {error && (
          <p className="mt-1.5 text-sm text-error animate-fade-in">{error}</p>
        )}
      </div>
    );
  }
);
Input.displayName = 'Input';
