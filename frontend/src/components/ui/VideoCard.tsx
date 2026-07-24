import React, { useState } from 'react';
import { Project } from '../../types';
import { Badge } from './Badge';
import { Play, MoreVertical, Edit2, Copy, Trash2, Download } from 'lucide-react';
import { useProjectStore } from '../../store/projectStore';
import { useToast } from '../../hooks/useToast';
import { Modal } from './Modal';
import { Button } from './Button';
import { Input } from './Input';

interface VideoCardProps {
  project: Project;
  onClick: (project: Project) => void;
}

export const VideoCard: React.FC<VideoCardProps> = ({ project, onClick }) => {
  const { updateProject, duplicateProject, deleteProject } = useProjectStore();
  const { addToast } = useToast();

  const [menuOpen, setMenuOpen] = useState(false);
  const [isRenameOpen, setIsRenameOpen] = useState(false);
  const [isDeleteOpen, setIsDeleteOpen] = useState(false);
  const [newTitle, setNewTitle] = useState(project.title);
  const [isUpdating, setIsUpdating] = useState(false);

  const date = new Date(project.created_at).toLocaleDateString();

  const handleRename = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim()) return;
    setIsUpdating(true);
    try {
      await updateProject(project.id, { title: newTitle.trim() });
      addToast({ type: 'success', message: 'Project renamed successfully' });
      setIsRenameOpen(false);
    } catch (err: any) {
      addToast({ type: 'error', message: err.message || 'Failed to rename project' });
    } finally {
      setIsUpdating(false);
    }
  };

  const handleDuplicate = async (e: React.MouseEvent) => {
    e.stopPropagation();
    setMenuOpen(false);
    try {
      await duplicateProject(project);
      addToast({ type: 'success', message: `Duplicated "${project.title}"` });
    } catch (err: any) {
      addToast({ type: 'error', message: err.message || 'Failed to duplicate project' });
    }
  };

  const handleDelete = async (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsUpdating(true);
    try {
      await deleteProject(project.id);
      addToast({ type: 'success', message: 'Project deleted' });
      setIsDeleteOpen(false);
    } catch (err: any) {
      addToast({ type: 'error', message: err.message || 'Failed to delete project' });
    } finally {
      setIsUpdating(false);
    }
  };

  return (
    <>
      <div 
        className="group relative flex flex-col glass-card overflow-hidden cursor-pointer transition-all hover:-translate-y-1"
        onClick={() => onClick(project)}
      >
        {/* Thumbnail area */}
        <div className="aspect-video w-full relative bg-surface border-b border-border/50 flex items-center justify-center overflow-hidden">
          {project.thumbnail_path ? (
            <img 
              src={project.thumbnail_path} 
              alt={project.title} 
              className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
            />
          ) : (
            <div className="w-full h-full bg-gradient-to-br from-surface to-border flex items-center justify-center relative">
              <div className="absolute inset-0 opacity-20 pointer-events-none" 
                   style={{ backgroundImage: 'radial-gradient(circle at 2px 2px, var(--color-text-muted) 1px, transparent 0)', backgroundSize: '24px 24px' }}>
              </div>
              <Play className="w-10 h-10 text-textMuted/40 pointer-events-none" />
            </div>
          )}
          
          {/* Quick Actions Dropdown Button */}
          <div className="absolute top-2 right-2 z-20">
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                setMenuOpen(!menuOpen);
              }}
              className="p-1.5 rounded-lg bg-black/60 hover:bg-black/90 text-white backdrop-blur-md transition-all border border-white/10"
              title="Project Options"
            >
              <MoreVertical className="w-4 h-4" />
            </button>

            {menuOpen && (
              <div 
                className="absolute right-0 mt-1 w-44 bg-surface border border-border rounded-xl shadow-xl z-30 py-1.5 animate-fade-in text-xs"
                onClick={(e) => e.stopPropagation()}
              >
                <button
                  onClick={() => { setMenuOpen(false); setIsRenameOpen(true); }}
                  className="w-full text-left px-3.5 py-2 hover:bg-border/60 flex items-center gap-2.5 text-text"
                >
                  <Edit2 className="w-3.5 h-3.5 text-accent" />
                  Rename Title
                </button>

                <button
                  onClick={handleDuplicate}
                  className="w-full text-left px-3.5 py-2 hover:bg-border/60 flex items-center gap-2.5 text-text"
                >
                  <Copy className="w-3.5 h-3.5 text-accent3" />
                  Duplicate
                </button>

                {project.output_path && (
                  <a
                    href={`http://localhost:8000/output/${project.id}.mp4`}
                    download
                    target="_blank"
                    rel="noreferrer"
                    onClick={(e) => e.stopPropagation()}
                    className="w-full text-left px-3.5 py-2 hover:bg-border/60 flex items-center gap-2.5 text-text"
                  >
                    <Download className="w-3.5 h-3.5 text-success" />
                    Download MP4
                  </a>
                )}

                <div className="my-1 border-t border-border/50" />

                <button
                  onClick={() => { setMenuOpen(false); setIsDeleteOpen(true); }}
                  className="w-full text-left px-3.5 py-2 hover:bg-error/15 text-error flex items-center gap-2.5"
                >
                  <Trash2 className="w-3.5 h-3.5 text-error" />
                  Delete Project
                </button>
              </div>
            )}
          </div>
        </div>
        
        <div className="p-4 flex flex-col gap-3 flex-1">
          <h4 className="font-semibold text-text line-clamp-1 pr-4" title={project.title}>
            {project.title}
          </h4>
          
          <div className="flex items-center justify-between mt-auto">
            <span className="text-[10px] font-bold text-textMuted uppercase tracking-wider bg-surface px-2 py-1 rounded border border-border/50">
              {project.video_type}
            </span>
            <Badge status={project.status} />
          </div>
          
          <div className="text-[11px] text-textMuted font-mono">
            Created {date}
          </div>
        </div>
      </div>

      {/* Rename Modal */}
      <Modal isOpen={isRenameOpen} onClose={() => setIsRenameOpen(false)} title="Rename Project">
        <form onSubmit={handleRename} className="space-y-4">
          <Input
            label="Project Title"
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
            placeholder="Enter new project title"
            autoFocus
          />
          <div className="flex justify-end gap-2 pt-2">
            <Button variant="ghost" type="button" onClick={() => setIsRenameOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" isLoading={isUpdating}>
              Save Name
            </Button>
          </div>
        </form>
      </Modal>

      {/* Delete Confirmation Modal */}
      <Modal isOpen={isDeleteOpen} onClose={() => setIsDeleteOpen(false)} title="Delete Project">
        <div className="space-y-4">
          <p className="text-sm text-textMuted">
            Are you sure you want to delete <strong className="text-text">"{project.title}"</strong>? This will permanently delete the project script and rendered video files.
          </p>
          <div className="flex justify-end gap-2 pt-2">
            <Button variant="ghost" type="button" onClick={() => setIsDeleteOpen(false)}>
              Cancel
            </Button>
            <Button variant="danger" onClick={handleDelete} isLoading={isUpdating}>
              Delete Permanently
            </Button>
          </div>
        </div>
      </Modal>
    </>
  );
};
