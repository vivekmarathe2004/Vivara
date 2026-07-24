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

export const DEFAULT_SETTINGS: AppSettings = {
  llm_provider: 'omniroute',
  llm_base_url: 'http://localhost:7777/v1',
  llm_model: 'llama3.2',
  tts_provider: 'kokoro',
  tts_voice: 'af_heart',
  edge_tts_voice: 'en-US-JennyNeural',
  gtts_lang: 'en',
  gpu_enabled: true,
  whisper_model: 'base',
  ffmpeg_path: 'ffmpeg',
  storage_dir: '../storage',
};

interface SettingsStore {
  settings: AppSettings;
  isLoading: boolean;
  error: string | null;
  fetchSettings: () => Promise<void>;
  updateSettings: (settings: Partial<AppSettings>) => Promise<void>;
}

export const useSettingsStore = create<SettingsStore>((set, get) => ({
  settings: DEFAULT_SETTINGS,
  isLoading: false,
  error: null,

  fetchSettings: async () => {
    set({ isLoading: true, error: null });
    try {
      const fetched = await apiGet<AppSettings>('/api/settings');
      set({ settings: { ...DEFAULT_SETTINGS, ...fetched }, isLoading: false });
    } catch (error: any) {
      console.warn('Backend settings fetch warning, using defaults:', error.message);
      set({ settings: get().settings || DEFAULT_SETTINGS, error: error.message || 'Failed to load settings', isLoading: false });
    }
  },

  updateSettings: async (newSettings: Partial<AppSettings>) => {
    set({ isLoading: true, error: null });
    try {
      const currentSettings = get().settings || DEFAULT_SETTINGS;
      const updated = { ...currentSettings, ...newSettings };
      const response = await apiPut<AppSettings>('/api/settings', updated);
      set({ settings: { ...DEFAULT_SETTINGS, ...response }, isLoading: false });
    } catch (error: any) {
      set({ error: error.message || 'Failed to save settings', isLoading: false });
      throw error;
    }
  }
}));
