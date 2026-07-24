import { useEffect } from 'react';
import { useProjectStore } from '../store/projectStore';
import { useSSE } from './useSSE';

export function useProject(projectId: string | undefined) {
  const { currentProject, fetchProject, isLoading, error } = useProjectStore();

  useEffect(() => {
    if (projectId) {
      fetchProject(projectId);
    }
  }, [projectId]);

  useSSE(projectId ? `/api/jobs/${projectId}/stream` : null, (data) => {
    if (data && projectId) {
      fetchProject(projectId);
    }
  });

  return { project: currentProject, isLoading, error };
}
