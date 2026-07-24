import { create } from 'zustand';
import { Project, ProjectCreate } from '../types';
import { projectsApi } from '../api/projects';

interface ProjectStore {
  projects: Project[];
  currentProject: Project | null;
  isLoading: boolean;
  error: string | null;
  fetchProjects: () => Promise<void>;
  fetchProject: (id: string) => Promise<void>;
  setCurrentProject: (p: Project | null) => void;
  createProject: (data: ProjectCreate) => Promise<Project>;
  updateProject: (id: string, data: { title?: string; script?: string; settings?: any }) => Promise<Project>;
  duplicateProject: (project: Project) => Promise<Project>;
  deleteProject: (id: string) => Promise<void>;
}

export const useProjectStore = create<ProjectStore>((set, get) => ({
  projects: [],
  currentProject: null,
  isLoading: false,
  error: null,

  fetchProjects: async () => {
    set({ isLoading: true, error: null });
    try {
      const projects = await projectsApi.list();
      set({ projects, isLoading: false });
    } catch (error: any) {
      set({ error: error.message || 'Failed to load projects', isLoading: false });
    }
  },

  fetchProject: async (id: string) => {
    set({ isLoading: true, error: null });
    try {
      const project = await projectsApi.get(id);
      set({ currentProject: project, isLoading: false });
    } catch (error: any) {
      set({ error: error.message || 'Failed to fetch project', isLoading: false });
    }
  },

  setCurrentProject: (p: Project | null) => set({ currentProject: p }),

  createProject: async (data: ProjectCreate) => {
    set({ isLoading: true, error: null });
    try {
      const project = await projectsApi.create(data);
      set((state) => ({ 
        projects: [project, ...state.projects],
        currentProject: project,
        isLoading: false
      }));
      return project;
    } catch (error: any) {
      set({ error: error.message || 'Failed to create project', isLoading: false });
      throw error;
    }
  },

  updateProject: async (id: string, data: { title?: string; script?: string; settings?: any }) => {
    try {
      const updated = await projectsApi.update(id, data);
      set((state) => ({
        projects: state.projects.map(p => p.id === id ? updated : p),
        currentProject: state.currentProject?.id === id ? updated : state.currentProject
      }));
      return updated;
    } catch (error: any) {
      set({ error: error.message || 'Failed to update project' });
      throw error;
    }
  },

  duplicateProject: async (project: Project) => {
    const settings = project.settings || {};

    const copyData: ProjectCreate = {
      title: `${project.title} (Copy)`,
      video_type: project.video_type as any,
      topic: project.topic,
      settings: settings
    };

    return get().createProject(copyData);
  },

  deleteProject: async (id: string) => {
    try {
      await projectsApi.delete(id);
      set((state) => ({
        projects: state.projects.filter(p => p.id !== id),
        currentProject: state.currentProject?.id === id ? null : state.currentProject
      }));
    } catch (error: any) {
      set({ error: error.message || 'Failed to delete project' });
      throw error;
    }
  },
}));
