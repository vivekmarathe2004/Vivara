import { create } from 'zustand';
import { apiGet, apiPut } from '../api/client';

export interface AppSettings {
  llm_provider?: string;
  llm_base_url?: string;
  llm_api_key?: string;
  llm_model?: string;
  tts_provider?: string;
  tts_voice?: string;
  edge_tts_voice?: string;
  gtts_lang?: string;
  elevenlabs_api_key?: string;
  elevenlabs_voice_id?: string;
  openai_tts_voice?: string;
  openai_tts_model?: string;
  pexels_api_key?: string;
  pixabay_api_key?: string;
  unsplash_api_key?: string;
  gpu_enabled?: boolean;
  ffmpeg_path?: string;
  whisper_model?: string;
  storage_dir?: string;
  [key: string]: any;
}

interface SettingsStore {
  settings: AppSettings | null;
  isLoading: boolean;
  error: string | null;
  fetchSettings: () => Promise<void>;
  updateSettings: (settings: Partial<AppSettings>) => Promise<void>;
}

export const useSettingsStore = create<SettingsStore>((set, get) => ({
  settings: null,
  isLoading: false,
  error: null,

  fetchSettings: async () => {
    set({ isLoading: true, error: null });
    try {
      const settings = await apiGet<AppSettings>('/api/settings');
      set({ settings, isLoading: false });
    } catch (error: any) {
      set({ error: error.message || 'Failed to load settings', isLoading: false });
    }
  },

  updateSettings: async (newSettings: Partial<AppSettings>) => {
    set({ isLoading: true, error: null });
    try {
      const currentSettings = get().settings || {};
      const updated = { ...currentSettings, ...newSettings };
      const response = await apiPut<AppSettings>('/api/settings', updated);
      set({ settings: response, isLoading: false });
    } catch (error: any) {
      set({ error: error.message || 'Failed to save settings', isLoading: false });
      throw error;
    }
  }
}));
