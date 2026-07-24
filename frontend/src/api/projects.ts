import { Project, ProjectCreate, PipelineStage } from '../types';
import { apiGet, apiPost, apiPut, apiDelete } from './client';

export const projectsApi = {
  list: () => apiGet<Project[]>('/api/projects'),
  get: (id: string) => apiGet<Project>(`/api/projects/${id}`),
  create: (data: ProjectCreate) => apiPost<Project>('/api/projects', data),
  update: (id: string, data: { title?: string; script?: string; settings?: any }) => 
    apiPut<Project>(`/api/projects/${id}`, data),
  delete: (id: string) => apiDelete<{ message: string }>(`/api/projects/${id}`),
  getStages: (id: string) => apiGet<PipelineStage[]>(`/api/projects/${id}/stages`),
};
