import { SystemCheck } from '../types';
import { apiGet, apiPost } from './client';

export const setupApi = {
  getSystemCheck: () => apiGet<SystemCheck>('/api/setup/check'),
  completeSetup: () => apiPost('/api/setup/complete'),
};
