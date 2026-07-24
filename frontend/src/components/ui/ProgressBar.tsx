import React from 'react';

interface ProgressBarProps {
  progress: number;
  className?: string;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({ progress, className = '' }) => {
  const clampedProgress = Math.min(100, Math.max(0, progress));

  return (
    <div className={`w-full bg-surface rounded-full h-2.5 border border-border overflow-hidden relative ${className}`}>
      <div
        className="bg-gradient-to-r from-accent to-accent2 h-2.5 rounded-full transition-all duration-300 ease-out relative overflow-hidden"
        style={{ width: `${clampedProgress}%` }}
      >
        <div className="absolute inset-0 bg-white/20 animate-shimmer" style={{ width: '200%' }} />
      </div>
    </div>
  );
};
