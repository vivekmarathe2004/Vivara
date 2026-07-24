import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useProject } from '../hooks/useProject';
import { useProjectStore } from '../store/projectStore';
import { generateApi } from '../api/generate';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { StageCard } from '../components/ui/StageCard';
import { Badge } from '../components/ui/Badge';
import { Modal } from '../components/ui/Modal';
import { useToast } from '../hooks/useToast';
import { 
  ArrowLeft, Play, Settings, Layers, Sparkles, Download, 
  FileText, Edit3, Trash2, Copy, Edit2
} from 'lucide-react';

export const ProjectDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { project, isLoading } = useProject(id);
  const { updateProject, duplicateProject, deleteProject } = useProjectStore();
  const { addToast } = useToast();
  
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isRenameModalOpen, setIsRenameModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [editedScript, setEditedScript] = useState('');
  const [newTitle, setNewTitle] = useState('');
  const [isUpdating, setIsUpdating] = useState(false);

  if (isLoading || !project) {
    return (
      <div className="p-12 flex justify-center items-center h-screen bg-background">
        <div className="w-10 h-10 rounded-full border-2 border-accent border-t-transparent animate-spin" />
      </div>
    );
  }

  const handleRunStage = async (stageName: string) => {
    try {
      await generateApi.runStage(project.id, stageName);
      addToast({ type: 'info', message: `Triggered ${stageName} stage` });
    } catch (e: any) {
      addToast({ type: 'error', message: e.message || 'Stage execution failed' });
    }
  };

  const handleSkipStage = async (stageName: string) => {
    try {
      await generateApi.skipStage(project.id, stageName);
      addToast({ type: 'info', message: `Skipped ${stageName} stage` });
    } catch (e: any) {
      addToast({ type: 'error', message: e.message || 'Failed to skip stage' });
    }
  };

  const handleRunPipeline = async () => {
    try {
      await generateApi.runPipeline(project.id);
      addToast({ type: 'info', message: 'Pipeline execution started' });
    } catch (e: any) {
      addToast({ type: 'error', message: e.message || 'Pipeline execution failed' });
    }
  };
  
  const handleEditScript = () => {
    setEditedScript(project.script || '');
    setIsEditModalOpen(true);
  };
  
  const saveScript = async () => {
    setIsUpdating(true);
    try {
      await updateProject(project.id, { script: editedScript });
      setIsEditModalOpen(false);
      addToast({ type: 'success', message: 'Script saved successfully' });
    } catch (err: any) {
      addToast({ type: 'error', message: err.message || 'Failed to save script' });
    } finally {
      setIsUpdating(false);
    }
  };

  const handleRename = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim()) return;
    setIsUpdating(true);
    try {
      await updateProject(project.id, { title: newTitle.trim() });
      addToast({ type: 'success', message: 'Project renamed successfully' });
      setIsRenameModalOpen(false);
    } catch (err: any) {
      addToast({ type: 'error', message: err.message || 'Failed to rename project' });
    } finally {
      setIsUpdating(false);
    }
  };

  const handleDuplicate = async () => {
    try {
      const copy = await duplicateProject(project);
      addToast({ type: 'success', message: `Duplicated "${project.title}"` });
      navigate(`/project/${copy.id}`);
    } catch (err: any) {
      addToast({ type: 'error', message: err.message || 'Failed to duplicate project' });
    }
  };

  const handleDelete = async () => {
    setIsUpdating(true);
    try {
      await deleteProject(project.id);
      addToast({ type: 'success', message: 'Project deleted successfully' });
      navigate('/');
    } catch (err: any) {
      addToast({ type: 'error', message: err.message || 'Failed to delete project' });
    } finally {
      setIsUpdating(false);
    }
  };

  const activeStageIndex = project.stages.findIndex(s => s.status === 'running' || s.status === 'error' || s.status === 'pending');
  const activeStage = activeStageIndex >= 0 ? project.stages[activeStageIndex] : null;

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      {/* ── Left Content Panel (65%) ────────────────────────────────── */}
      <div className="flex-[65] flex flex-col border-r border-border/50 bg-background/50">
        
        {/* Header */}
        <header className="px-6 py-4 border-b border-border/50 flex items-center justify-between bg-surface/60 backdrop-blur-xl z-20">
          <div className="flex items-center gap-3">
            <Button variant="ghost" size="sm" onClick={() => navigate('/')} className="px-2 cursor-pointer">
              <ArrowLeft className="w-5 h-5" />
            </Button>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="font-extrabold text-lg tracking-tight truncate max-w-md">{project.title}</h1>
                <button
                  type="button"
                  onClick={() => { setNewTitle(project.title); setIsRenameModalOpen(true); }}
                  className="p-1 text-textMuted hover:text-accent transition-colors"
                  title="Rename Title"
                >
                  <Edit2 className="w-3.5 h-3.5" />
                </button>
              </div>
              <div className="flex items-center gap-2 mt-0.5">
                <Badge status={project.status} />
                <span className="text-[10px] font-bold text-accent font-mono uppercase tracking-wider px-2 py-0.5 bg-accent/10 border border-accent/30 rounded">
                  {project.video_type}
                </span>
              </div>
            </div>
          </div>

          {/* Quick Action Toolbar */}
          <div className="flex items-center gap-2">
            <Button variant="secondary" size="sm" onClick={handleDuplicate} title="Duplicate Project">
              <Copy className="w-4 h-4 mr-1.5 text-accent3" />
              Duplicate
            </Button>

            <Button variant="secondary" size="sm" onClick={() => navigate('/settings')}>
              <Settings className="w-4 h-4 mr-1.5" />
              Settings
            </Button>

            <Button variant="danger" size="sm" onClick={() => setIsDeleteModalOpen(true)} title="Delete Project">
              <Trash2 className="w-4 h-4" />
            </Button>
          </div>
        </header>

        {/* Dynamic Visual Stage Output View */}
        <div className="flex-1 overflow-y-auto p-8 relative">
          
          {/* Complete Render View */}
          {(!activeStage || project.status === 'done') && (
            <div className="h-full flex flex-col items-center justify-center animate-fade-in text-center space-y-6 max-w-3xl mx-auto">
              <div className="w-full aspect-video bg-black rounded-xl overflow-hidden border border-border relative group">
                {project.output_path ? (
                  <video src={`http://localhost:8000/output/${project.id}.mp4`} controls className="w-full h-full object-contain" />
                ) : (
                  <div className="absolute inset-0 flex flex-col items-center justify-center p-6 bg-surface">
                    <Play className="w-16 h-16 text-accent mb-4" />
                    <h3 className="font-bold text-lg">Final Video Composited</h3>
                    <p className="text-xs text-textMuted mt-1">Render complete. Ready for preview and download.</p>
                  </div>
                )}
              </div>
              
              <div>
                <h2 className="text-2xl font-extrabold tracking-tight">Generation Complete! 🎉</h2>
                <p className="text-sm text-textMuted mt-1">All pipeline nodes executed successfully.</p>
              </div>

              <div className="flex items-center gap-4">
                <a 
                  href={`http://localhost:8000/output/${project.id}.mp4`} 
                  download 
                  target="_blank" 
                  rel="noreferrer"
                >
                  <Button size="lg" className="w-48">
                    <Download className="w-4 h-4 mr-2" />
                    Download MP4
                  </Button>
                </a>
              </div>
            </div>
          )}

          {/* Script Stage Active View */}
          {activeStage?.stage === 'script' && (
            <div className="animate-fade-in max-w-3xl mx-auto space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <FileText className="w-5 h-5 text-accent" />
                  <h2 className="text-xl font-bold">Script Generation Node</h2>
                </div>
                <Button variant="secondary" size="sm" onClick={handleEditScript}>
                  <Edit3 className="w-4 h-4 mr-2" />
                  Edit Script
                </Button>
              </div>

              <div className="glass-card p-6 border-border/60 font-mono text-xs text-emerald-400 leading-relaxed whitespace-pre-wrap min-h-[400px]">
                {project.script || "Generating script with scene tags..."}
              </div>
            </div>
          )}
          
          {/* Other Stages Processing View */}
          {activeStage && activeStage.stage !== 'script' && (
            <div className="h-full flex flex-col items-center justify-center text-center animate-fade-in space-y-6">
              <div className="relative">
                <div className="w-20 h-20 rounded-full border-4 border-accent/20 border-t-accent animate-spin" />
                <Sparkles className="w-8 h-8 text-accent absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2" />
              </div>
              <div>
                <h2 className="text-2xl font-bold capitalize">Executing Node: {activeStage.stage}</h2>
                <p className="text-sm text-textMuted mt-1 max-w-sm mx-auto">
                  The modular DAG engine is processing this stage. Live streaming logs on the right panel.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* ── Right Pipeline Node Control Panel (35%) ─────────────────── */}
      <div className="flex-[35] flex flex-col bg-surface/40 border-l border-border/50">
        <div className="p-6 border-b border-border/50 flex justify-between items-center bg-surface/60 backdrop-blur-xl">
          <div className="flex items-center gap-2">
            <Layers className="w-5 h-5 text-accent" />
            <h2 className="font-bold text-lg">Node Graph Pipeline</h2>
          </div>
          <Button 
            size="sm" 
            onClick={handleRunPipeline} 
            disabled={project.status === 'running' || project.status === 'done'}
            className="cursor-pointer"
          >
            <Play className="w-4 h-4 mr-1.5" /> Run All
          </Button>
        </div>
        
        <div className="flex-1 overflow-y-auto p-6 space-y-4 custom-scrollbar">
          {project.stages.map((stage) => (
            <StageCard
              key={stage.id}
              stage={stage}
              isActive={stage.id === activeStage?.id}
              onRun={() => handleRunStage(stage.stage)}
              onSkip={() => handleSkipStage(stage.stage)}
              onEdit={stage.stage === 'script' ? handleEditScript : undefined}
            />
          ))}
        </div>
      </div>
      
      {/* ── Script Edit Modal ────────────────────────────────────────── */}
      <Modal isOpen={isEditModalOpen} onClose={() => setIsEditModalOpen(false)} title="Edit Project Script" maxWidth="4xl">
        <div className="space-y-4">
          <textarea
            className="w-full h-[60vh] bg-background/90 border border-border rounded-xl p-4 font-mono text-xs text-emerald-400 leading-relaxed resize-none focus:border-accent outline-none"
            value={editedScript}
            onChange={e => setEditedScript(e.target.value)}
          />
          <div className="flex justify-end gap-3">
            <Button variant="ghost" onClick={() => setIsEditModalOpen(false)}>Cancel</Button>
            <Button onClick={saveScript} isLoading={isUpdating}>Save & Update Script</Button>
          </div>
        </div>
      </Modal>

      {/* ── Rename Title Modal ───────────────────────────────────────── */}
      <Modal isOpen={isRenameModalOpen} onClose={() => setIsRenameModalOpen(false)} title="Rename Project Title">
        <form onSubmit={handleRename} className="space-y-4">
          <Input
            label="Project Title"
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
            placeholder="Enter new project title"
            autoFocus
          />
          <div className="flex justify-end gap-2 pt-2">
            <Button variant="ghost" type="button" onClick={() => setIsRenameModalOpen(false)}>Cancel</Button>
            <Button type="submit" isLoading={isUpdating}>Save Name</Button>
          </div>
        </form>
      </Modal>

      {/* ── Delete Confirmation Modal ────────────────────────────────── */}
      <Modal isOpen={isDeleteModalOpen} onClose={() => setIsDeleteModalOpen(false)} title="Delete Project">
        <div className="space-y-4">
          <p className="text-sm text-textMuted">
            Are you sure you want to delete <strong className="text-text">"{project.title}"</strong>? This will permanently delete the project script and rendered video files.
          </p>
          <div className="flex justify-end gap-2 pt-2">
            <Button variant="ghost" type="button" onClick={() => setIsDeleteModalOpen(false)}>Cancel</Button>
            <Button variant="danger" onClick={handleDelete} isLoading={isUpdating}>Delete Permanently</Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};
