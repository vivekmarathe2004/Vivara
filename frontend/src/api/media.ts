import { apiPost } from './client';

export const mediaApi = {
  testPexels: (key: string) => apiPost<{ success: boolean }>('/api/media/test/pexels', { key }),
  testPixabay: (key: string) => apiPost<{ success: boolean }>('/api/media/test/pixabay', { key }),
};
