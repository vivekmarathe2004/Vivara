import React from 'react';
import { PipelineStage, StageType } from '../../types';
import { Badge } from './Badge';
import { ProgressBar } from './ProgressBar';
import { Button } from './Button';
import { FileText, Mic, MessageSquare, Image, Film, Play, SkipForward, Edit2 } from 'lucide-react';

interface StageCardProps {
  stage: PipelineStage;
  onRun: (id: string) => void;
  onSkip: (id: string) => void;
  onEdit?: (id: string) => void;
  isActive?: boolean;
}

export const StageCard: React.FC<StageCardProps> = ({ stage, onRun, onSkip, onEdit, isActive = false }) => {
  const icons: Record<StageType, React.ReactNode> = {
    script: <FileText className="w-5 h-5" />,
    voice: <Mic className="w-5 h-5" />,
    subtitles: <MessageSquare className="w-5 h-5" />,
    media: <Image className="w-5 h-5" />,
    render: <Film className="w-5 h-5" />,
  };

  const titles: Record<StageType, string> = {
    script: 'Script Generation',
    voice: 'Voice Synthesis',
    subtitles: 'Subtitle Generation',
    media: 'Media Assembly',
    render: 'Final Render',
  };

  const isRunning = stage.status === 'running';
  const isDone = stage.status === 'done';

  return (
    <div className={`
      relative p-4 rounded-xl border transition-all duration-300
      ${isActive ? 'bg-surface/80 border-accent/50 shadow-[0_0_15px_rgba(108,99,255,0.1)]' : 'glass-card border-border/50'}
      ${isRunning ? 'border-accent animate-[pulse-glow_2s_ease-in-out_infinite]' : ''}
    `}>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-3">
          <div className={`
            p-2 rounded-lg 
            ${isDone ? 'bg-success/20 text-success' : isRunning ? 'bg-accent/20 text-accent' : 'bg-surface text-textMuted'}
          `}>
            {icons[stage.stage]}
          </div>
          <div>
            <h4 className="font-medium text-text">{titles[stage.stage]}</h4>
          </div>
        </div>
        <Badge status={stage.status} />
      </div>

      {isRunning && (
        <div className="mb-4 mt-2">
          <div className="flex justify-between text-xs text-textMuted mb-1">
            <span>Progress</span>
            <span>{Math.round(stage.progress)}%</span>
          </div>
          <ProgressBar progress={stage.progress} />
        </div>
      )}

      {stage.error_msg && (
        <div className="mt-2 mb-3 p-2 bg-error/10 border border-error/20 rounded-md text-sm text-error">
          {stage.error_msg}
        </div>
      )}

      <div className="flex items-center gap-2 mt-4">
        <Button 
          variant={isDone ? 'ghost' : 'primary'} 
          size="sm" 
          onClick={() => onRun(stage.id)}
          disabled={isRunning}
          className="flex-1"
        >
          <Play className="w-4 h-4 mr-2" />
          {isDone ? 'Re-run' : 'Run'}
        </Button>
        
        {stage.stage === 'script' && isDone && onEdit && (
          <Button variant="secondary" size="sm" onClick={() => onEdit(stage.id)}>
            <Edit2 className="w-4 h-4" />
          </Button>
        )}
        
        {!isDone && !isRunning && (
          <Button variant="ghost" size="sm" onClick={() => onSkip(stage.id)}>
            <SkipForward className="w-4 h-4" />
          </Button>
        )}
      </div>
    </div>
  );
};
