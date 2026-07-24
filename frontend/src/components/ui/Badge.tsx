import React from 'react';

interface BadgeProps {
  status: 'pending' | 'running' | 'done' | 'error' | 'skipped';
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({ status, className = '' }) => {
  const statusStyles = {
    pending: 'bg-surface text-textMuted border border-border',
    running: 'bg-accent/10 text-accent border border-accent/20 animate-pulse-glow',
    done: 'bg-success/10 text-success border border-success/20',
    error: 'bg-error/10 text-error border border-error/20',
    skipped: 'bg-surface text-textMuted border border-border line-through opacity-70',
  };

  const labels = {
    pending: 'Pending',
    running: 'Running',
    done: 'Done',
    error: 'Error',
    skipped: 'Skipped',
  };

  return (
    <span className={`badge ${statusStyles[status]} ${className}`}>
      {labels[status]}
    </span>
  );
};
