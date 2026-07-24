import React, { useEffect, useState } from 'react';
import { useSettingsStore } from '../store/settingsStore';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Select } from '../components/ui/Select';
import { useToast } from '../hooks/useToast';
import { Save, Cpu, Key, Volume2, Monitor, ExternalLink, CheckCircle2 } from 'lucide-react';

type Tab = 'llm' | 'tts' | 'media' | 'system';

const tabs: { id: Tab; label: string; icon: React.ElementType }[] = [
  { id: 'llm',    label: 'AI / LLM',    icon: Cpu     },
  { id: 'tts',    label: 'Voice / TTS', icon: Volume2 },
  { id: 'media',  label: 'Stock Media', icon: Key     },
  { id: 'system', label: 'System',      icon: Monitor },
];

export const Settings: React.FC = () => {
  const { settings, fetchSettings, updateSettings, isLoading } = useSettingsStore();
  const { addToast } = useToast();
  const [formData, setFormData] = useState<any>({});
  const [activeTab, setActiveTab] = useState<Tab>('llm');

  useEffect(() => { fetchSettings(); }, []);

  useEffect(() => {
    if (settings) setFormData(settings);
  }, [settings]);

  const handleChange = (field: string, value: any) => {
    setFormData((prev: any) => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    try {
      await updateSettings(formData);
      addToast({ type: 'success', message: 'Settings saved successfully' });
    } catch (error: any) {
      addToast({ type: 'error', message: error.message || 'Failed to save settings' });
    }
  };

  if (!settings) {
    return (
      <div className="p-8 flex justify-center items-center min-h-[400px]">
        <div className="w-8 h-8 rounded-full border-2 border-accent border-t-transparent animate-spin" />
      </div>
    );
  }

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-8 animate-fade-in">
      {/* ── Header ────────────────────────────────────────────── */}
      <div className="flex items-center justify-between border-b border-border/50 pb-6">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight">Engine Settings</h1>
          <p className="text-sm text-textMuted mt-1">Configure AI routers, voice engines, and stock media keys.</p>
        </div>
        <Button onClick={handleSave} isLoading={isLoading} className="cursor-pointer font-bold">
          <Save className="w-4 h-4 mr-2" />
          Save Changes
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-8">

        {/* ── Left Tab Sidebar ───────────────────────────────────── */}
        <div className="md:col-span-1 space-y-2">
          <div className="glass-card p-2 space-y-1">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  type="button"
                  onClick={() => setActiveTab(tab.id)}
                  className={`
                    w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-semibold
                    transition-all duration-150 text-left cursor-pointer
                    ${isActive
                      ? 'bg-accent/15 text-accent border border-accent/30'
                      : 'text-textMuted hover:text-text hover:bg-surface/80 border border-transparent'
                    }
                  `}
                >
                  <Icon className="w-4.5 h-4.5 shrink-0" />
                  {tab.label}
                </button>
              );
            })}
          </div>
        </div>

        {/* ── Right Content Area ─────────────────────────────────── */}
        <div className="md:col-span-3">

          {/* AI / LLM Configuration */}
          {activeTab === 'llm' && (
            <section className="glass-card p-6 space-y-6 animate-fade-in">
              <div className="flex items-center gap-2 border-b border-border/50 pb-4">
                <Cpu className="w-5 h-5 text-accent" />
                <h2 className="text-lg font-bold">AI / LLM Gateway Router</h2>
              </div>
              <div className="space-y-5">
                <Select
                  label="Provider Engine"
                  value={formData.llm_provider || 'omniroute'}
                  onChange={(e) => handleChange('llm_provider', e.target.value)}
                  options={[
                    { label: 'OmniRoute AI Gateway (Recommended)', value: 'omniroute' },
                    { label: 'Auto (smart provider routing)',     value: 'auto' },
                    { label: 'Ollama (Local)',                     value: 'ollama' },
                    { label: 'OpenAI Compatible',                  value: 'openai_compat' },
                    { label: 'LM Studio',                          value: 'lm_studio' },
                    { label: 'vLLM',                               value: 'vllm' },
                    { label: 'OpenRouter',                         value: 'openrouter' },
                    { label: 'Custom Endpoint',                    value: 'custom' },
                  ]}
                />
                <Input
                  label="Base Endpoint URL"
                  value={formData.llm_base_url || 'http://localhost:7777/v1'}
                  onChange={(e) => handleChange('llm_base_url', e.target.value)}
                  placeholder="e.g. http://localhost:7777/v1 or http://localhost:11434"
                />
                <Input
                  label="API Key (Optional)"
                  type="password"
                  value={formData.llm_api_key || ''}
                  onChange={(e) => handleChange('llm_api_key', e.target.value)}
                  placeholder="Leave blank for local providers"
                />
                <Input
                  label="Model Identifier / Alias"
                  value={formData.llm_model || 'llama3.2'}
                  onChange={(e) => handleChange('llm_model', e.target.value)}
                  placeholder="e.g. auto, llama3.2, claude-3-5-sonnet"
                />
              </div>
            </section>
          )}

          {/* Voice / TTS Engines */}
          {activeTab === 'tts' && (
            <section className="glass-card p-6 space-y-6 animate-fade-in">
              <div className="flex items-center gap-2 border-b border-border/50 pb-4">
                <Volume2 className="w-5 h-5 text-accent" />
                <h2 className="text-lg font-bold">Voice & Speech Synthesis</h2>
              </div>
              <div className="space-y-5">
                <Select
                  label="Primary TTS Engine"
                  value={formData.tts_provider || 'kokoro'}
                  onChange={(e) => handleChange('tts_provider', e.target.value)}
                  options={[
                    { label: 'Kokoro-82M (100% Free, Offline — Recommended)', value: 'kokoro' },
                    { label: 'Edge-TTS (100% Free, Microsoft Neural Voices)',   value: 'edge_tts' },
                    { label: 'Google Translate TTS (100% Free, 100+ Languages, No Key)', value: 'gtts' },
                    { label: 'ElevenLabs (Free API Key: 10,000 Chars/Mo)',     value: 'elevenlabs' },
                    { label: 'OpenAI Speech API (Alloy, Echo, Fable, Onyx, Nova, Shimmer)', value: 'openai_tts' },
                  ]}
                />

                {formData.tts_provider === 'elevenlabs' && (
                  <div className="p-4 rounded-xl bg-surface border border-border space-y-3">
                    <Input
                      label="ElevenLabs API Key"
                      type="password"
                      value={formData.elevenlabs_api_key || ''}
                      onChange={(e) => handleChange('elevenlabs_api_key', e.target.value)}
                      placeholder="Paste your free ElevenLabs API key"
                    />
                    <a
                      href="https://elevenlabs.io/app/speech-synthesis"
                      target="_blank"
                      rel="noreferrer"
                      className="text-xs text-textMuted hover:text-accent font-medium inline-flex items-center gap-1 transition-colors"
                    >
                      <span>Get a free ElevenLabs API key (10,000 chars/mo free)</span>
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  </div>
                )}

                {formData.tts_provider === 'gtts' && (
                  <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/25 flex items-start gap-3">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                    <div className="text-xs text-emerald-300 font-medium leading-relaxed">
                      <strong>Google Translate TTS Active</strong> — 100% Free online voice synthesis supporting over 100 languages with zero API key required!
                    </div>
                  </div>
                )}

                <Select
                  label="Default Voice Preset"
                  value={formData.tts_voice || 'af_heart'}
                  onChange={(e) => handleChange('tts_voice', e.target.value)}
                  options={[
                    { label: 'Kokoro: Heart (Female, Natural)',    value: 'af_heart' },
                    { label: 'Kokoro: Bella (Female, Energetic)',  value: 'af_bella' },
                    { label: 'Kokoro: Michael (Male, Pro)',        value: 'am_michael' },
                    { label: 'Google: English (en)',               value: 'en' },
                    { label: 'Google: Spanish (es)',               value: 'es' },
                    { label: 'Google: French (fr)',                value: 'fr' },
                    { label: 'ElevenLabs: Rachel (Female, Warm)',  value: '21m00Tcm4TlvDq8ikWAM' },
                    { label: 'OpenAI: Alloy (Neutral, Versatile)', value: 'alloy' },
                    { label: 'OpenAI: Echo (Male, Warm)',          value: 'echo' },
                    { label: 'OpenAI: Nova (Female, Energetic)',   value: 'nova' },
                    { label: 'Edge-TTS: Jenny (Female, US)',       value: 'en-US-JennyNeural' },
                  ]}
                />
              </div>
            </section>
          )}

          {/* Stock Media Providers */}
          {activeTab === 'media' && (
            <section className="glass-card p-6 space-y-6 animate-fade-in">
              <div className="flex items-center gap-2 border-b border-border/50 pb-4">
                <Key className="w-5 h-5 text-accent" />
                <h2 className="text-lg font-bold">Stock Media Providers</h2>
              </div>
              
              {/* Clean Notice Badge */}
              <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/25 flex items-start gap-3">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                <div className="text-xs text-emerald-300 font-medium leading-relaxed">
                  <strong>Openverse / Wikimedia Active</strong> — Millions of 100% free open license photos & stock media are ready out of the box with zero API keys required!
                </div>
              </div>

              {/* Clean Form List */}
              <div className="space-y-5 pt-1">
                
                <div className="p-4 rounded-xl bg-surface border border-border space-y-2">
                  <Input
                    label="Pexels API Key (Free Tier: 200 Requests/Hr)"
                    type="password"
                    value={formData.pexels_api_key || ''}
                    onChange={(e) => handleChange('pexels_api_key', e.target.value)}
                    placeholder="Paste your free Pexels key here"
                  />
                  <a
                    href="https://www.pexels.com/api/"
                    target="_blank"
                    rel="noreferrer"
                    className="text-xs text-textMuted hover:text-accent font-medium inline-flex items-center gap-1 transition-colors"
                  >
                    <span>Get a free Pexels API key</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                </div>

                <div className="p-4 rounded-xl bg-surface border border-border space-y-2">
                  <Input
                    label="Pixabay API Key (Free Tier: 5,000 Requests/Hr)"
                    type="password"
                    value={formData.pixabay_api_key || ''}
                    onChange={(e) => handleChange('pixabay_api_key', e.target.value)}
                    placeholder="Paste your free Pixabay key here"
                  />
                  <a
                    href="https://pixabay.com/api/docs/"
                    target="_blank"
                    rel="noreferrer"
                    className="text-xs text-textMuted hover:text-accent font-medium inline-flex items-center gap-1 transition-colors"
                  >
                    <span>Get a free Pixabay API key</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                </div>

                <div className="p-4 rounded-xl bg-surface border border-border space-y-2">
                  <Input
                    label="Unsplash API Key (Free Tier: 50 Requests/Hr)"
                    type="password"
                    value={formData.unsplash_api_key || ''}
                    onChange={(e) => handleChange('unsplash_api_key', e.target.value)}
                    placeholder="Paste your free Unsplash key here"
                  />
                  <a
                    href="https://unsplash.com/developers"
                    target="_blank"
                    rel="noreferrer"
                    className="text-xs text-textMuted hover:text-accent font-medium inline-flex items-center gap-1 transition-colors"
                  >
                    <span>Get a free Unsplash API key</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                </div>

              </div>
            </section>
          )}

          {/* System Configuration */}
          {activeTab === 'system' && (
            <section className="glass-card p-6 space-y-6 animate-fade-in">
              <div className="flex items-center gap-2 border-b border-border/50 pb-4">
                <Monitor className="w-5 h-5 text-accent" />
                <h2 className="text-lg font-bold">System & Performance Configuration</h2>
              </div>
              <div className="space-y-5">
                {/* GPU toggle */}
                <div className="flex items-center justify-between p-4 bg-surface rounded-xl border border-border">
                  <div>
                    <h4 className="font-semibold text-sm">GPU Acceleration (NVENC / AMF)</h4>
                    <p className="text-xs text-textMuted mt-0.5">Use hardware video encoder when available</p>
                  </div>
                  <button
                    type="button"
                    onClick={() => handleChange('gpu_enabled', !formData.gpu_enabled)}
                    className={`w-12 h-6 rounded-full transition-colors relative focus:outline-none cursor-pointer ${
                      formData.gpu_enabled ? 'bg-success' : 'bg-border'
                    }`}
                  >
                    <div
                      className={`w-4 h-4 rounded-full bg-white absolute top-1 transition-all ${
                        formData.gpu_enabled ? 'left-7' : 'left-1'
                      }`}
                    />
                  </button>
                </div>

                <Select
                  label="Whisper Model Size"
                  value={formData.whisper_model || 'base'}
                  onChange={(e) => handleChange('whisper_model', e.target.value)}
                  options={[
                    { label: 'Tiny  (fastest, least accurate)',  value: 'tiny'   },
                    { label: 'Base  (balanced — recommended)',    value: 'base'   },
                    { label: 'Small (better accuracy)',           value: 'small'  },
                    { label: 'Medium (high accuracy, slower)',    value: 'medium' },
                  ]}
                />

                <Input
                  label="FFmpeg Path (Optional Override)"
                  value={formData.ffmpeg_path || ''}
                  onChange={(e) => handleChange('ffmpeg_path', e.target.value)}
                  placeholder="Auto-detected if blank (e.g. ffmpeg)"
                />

                <Input
                  label="Storage Directory"
                  value={formData.storage_dir || '../storage'}
                  onChange={(e) => handleChange('storage_dir', e.target.value)}
                  placeholder="../storage"
                />
              </div>
            </section>
          )}

        </div>
      </div>
    </div>
  );
};
