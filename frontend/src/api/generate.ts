import { apiPost } from './client';

export const generateApi = {
  generateScript: (projectId: string, data?: any) => apiPost<{ script: string }>(`/api/generate/script/${projectId}`, data),
  runStage: (projectId: string, stageId: string) => apiPost(`/api/generate/stage/${projectId}/${stageId}`),
  runPipeline: (projectId: string) => apiPost(`/api/generate/pipeline/${projectId}`),
  skipStage: (projectId: string, stageId: string) => apiPost(`/api/generate/stage/${projectId}/${stageId}/skip`),
};
