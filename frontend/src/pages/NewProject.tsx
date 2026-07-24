import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useProjectStore } from '../store/projectStore';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Select } from '../components/ui/Select';
import { useToast } from '../hooks/useToast';
import { VideoType, ProjectCreate } from '../types';
import { 
  Trophy, Star, Lightbulb, Smartphone, Film, BookOpen, Wand2, 
  ArrowRight, Sparkles, CheckCircle2
} from 'lucide-react';

export const NewProject: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { createProject } = useProjectStore();
  const { addToast } = useToast();
  
  const [step, setStep] = useState(1);
  const [isGenerating, setIsGenerating] = useState(false);
  const [script, setScript] = useState('');
  
  const initialType = (searchParams.get('type') as VideoType) || 'ranking';
  const initialTopic = searchParams.get('topic') || '';

  const [formData, setFormData] = useState<Partial<ProjectCreate>>({
    video_type: initialType,
    title: initialTopic,
    topic: initialTopic,
    settings: {
      duration: 'medium',
      aspect_ratio: initialType === 'shorts' ? '9:16' : '16:9',
      voice: 'af_heart',
      subtitle_style: 'clean',
      bg_music: 'ambient'
    }
  });

  useEffect(() => {
    if (initialTopic) {
      setStep(2);
    }
  }, [initialTopic]);

  const videoTypes = [
    { type: 'ranking', name: 'Ranking / Top 10', icon: Trophy, desc: 'Countdowns, top entries & lists', color: 'text-amber-400 border-amber-500/40 bg-amber-500/10' },
    { type: 'review', name: 'Review & Verdict', icon: Star, desc: 'Movies, games, tech breakdown', color: 'text-blue-400 border-blue-500/40 bg-blue-500/10' },
    { type: 'explainer', name: 'Explainer & Lore', icon: Lightbulb, desc: 'How-to, deep explanations', color: 'text-purple-400 border-purple-500/40 bg-purple-500/10' },
    { type: 'shorts', name: 'YouTube Shorts', icon: Smartphone, desc: 'Vertical 9:16, punchy 3s hook', color: 'text-pink-400 border-pink-500/40 bg-pink-500/10' },
    { type: 'documentary', name: 'Documentary Arc', icon: Film, desc: 'Cinematic storytelling', color: 'text-cyan-400 border-cyan-500/40 bg-cyan-500/10' },
    { type: 'educational', name: 'Educational Guide', icon: BookOpen, desc: 'Tutorials & course lessons', color: 'text-emerald-400 border-emerald-500/40 bg-emerald-500/10' },
  ];

  const handleNext = () => setStep(s => Math.min(s + 1, 5));
  const handleBack = () => setStep(s => Math.max(s - 1, 1));

  const updateForm = (field: string, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const updateSetting = (field: string, value: any) => {
    setFormData(prev => ({
      ...prev,
      settings: { ...prev.settings, [field]: value }
    }));
  };

  const generateScriptPreview = async () => {
    if (!formData.topic) {
      addToast({ type: 'error', message: 'Please enter a topic first' });
      return;
    }
    setIsGenerating(true);
    try {
      await new Promise(r => setTimeout(r, 1800));
      const mockScript = `[SCENE 1: High energy hook with cinematic background audio]
Narrator: Have you ever wondered why ${formData.topic || 'this topic'} captivates millions? Let's dive deep!

[SCENE 2: Fast cut transitions & bold title card]
Narrator: Key insight #1 — The foundation of everything comes down to innovation and execution.

[SCENE 3: Dynamic stock footage overlay & subtitle highlights]
Narrator: In conclusion, mastering ${formData.topic || 'this concept'} gives you an unbeatable advantage. Like & subscribe!`;

      setScript(mockScript);
      setStep(4);
    } catch (e: any) {
      addToast({ type: 'error', message: 'Script generation failed' });
    } finally {
      setIsGenerating(false);
    }
  };

  const handleLaunch = async () => {
    try {
      const proj = await createProject({
        title: formData.title || formData.topic || 'New Project',
        video_type: formData.video_type as VideoType,
        topic: formData.topic || '',
        settings: formData.settings || {}
      });
      navigate(`/project/${proj.id}`);
    } catch (e: any) {
      addToast({ type: 'error', message: e.message || 'Creation failed' });
    }
  };

  return (
    <div className="p-8 max-w-5xl mx-auto animate-fade-in space-y-8">
      {/* ── Header & Glowing Progress Bar ────────────────────────────── */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <div>
            <h1 className="text-3xl font-extrabold tracking-tight">New Creation Studio</h1>
            <p className="text-sm text-textMuted">Configure your AI video parameters step by step.</p>
          </div>
          <span className="text-xs font-mono text-accent bg-accent/10 px-3 py-1.5 rounded-full border border-accent/30 font-semibold">
            STEP {step} OF 5
          </span>
        </div>

        <div className="h-2 w-full bg-surface rounded-full overflow-hidden p-0.5 border border-border/50">
          <div 
            className="h-full bg-gradient-to-r from-accent via-accent2 to-accent3 rounded-full transition-all duration-500 ease-out"
            style={{ width: `${(step / 5) * 100}%` }}
          />
        </div>
      </div>

      {/* ── Glass Container ──────────────────────────────────────────── */}
      <div className="glass-card p-8 border-border/60 min-h-[520px] flex flex-col justify-between relative overflow-hidden">
        
        {step === 1 && (
          <div className="animate-fade-in space-y-6 flex-1">
            <div>
              <h2 className="text-xl font-bold">Choose a Workflow Platform</h2>
              <p className="text-sm text-textMuted">Select the structural template for your video.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {videoTypes.map(vt => {
                const isSelected = formData.video_type === vt.type;
                const Icon = vt.icon;
                return (
                  <div 
                    key={vt.type}
                    onClick={() => updateForm('video_type', vt.type)}
                    className={`
                      p-5 rounded-2xl border-2 cursor-pointer transition-all duration-200 flex flex-col justify-between gap-3 group
                      ${isSelected 
                        ? `${vt.color}` 
                        : 'border-border/60 bg-surface/70 hover:border-accent/40 hover:bg-surface/90'
                      }
                    `}
                  >
                    <div className="flex items-center justify-between">
                      <div className={`p-3 rounded-xl ${isSelected ? 'bg-white/10' : 'bg-background/80'} group-hover:scale-110 transition-transform`}>
                        <Icon className="w-6 h-6" />
                      </div>
                      {isSelected && <CheckCircle2 className="w-5 h-5 text-accent" />}
                    </div>
                    <div>
                      <h3 className="font-bold text-base">{vt.name}</h3>
                      <p className="text-xs text-textMuted mt-1">{vt.desc}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="animate-fade-in space-y-6 flex-1 max-w-2xl mx-auto w-full">
            <div>
              <h2 className="text-xl font-bold">What is the video about?</h2>
              <p className="text-sm text-textMuted">Define your topic, angle, or paste specific instructions.</p>
            </div>

            <div className="space-y-5">
              <Input 
                label="Project Title" 
                placeholder="e.g. Top 10 Best Sci-Fi Movies of 2026"
                value={formData.title}
                onChange={e => updateForm('title', e.target.value)}
              />
              
              <Input 
                multiline
                label="Detailed Topic / Research Prompt" 
                placeholder="Describe what you want the script to focus on. Include key facts, tone, or specific items to rank..."
                value={formData.topic}
                onChange={e => updateForm('topic', e.target.value)}
              />
            </div>
          </div>
        )}

        {step === 3 && (
          <div className="animate-fade-in space-y-6 flex-1 max-w-3xl mx-auto w-full">
            <div>
              <h2 className="text-xl font-bold">Style & Rendering Parameters</h2>
              <p className="text-sm text-textMuted">Configure aspect ratio, voice actor, and subtitle overlay styling.</p>
            </div>

            <div className="grid grid-cols-2 gap-5">
              <Select 
                label="Duration" 
                value={formData.settings?.duration}
                onChange={e => updateSetting('duration', e.target.value)}
                options={[
                  {label: 'Short (1-3 min)', value: 'short'},
                  {label: 'Medium (5-8 min)', value: 'medium'},
                  {label: 'Long (10-15 min)', value: 'long'},
                ]}
              />
              <Select 
                label="Aspect Ratio" 
                value={formData.settings?.aspect_ratio}
                onChange={e => updateSetting('aspect_ratio', e.target.value)}
                options={[
                  {label: 'Landscape 16:9 (YouTube)', value: '16:9'},
                  {label: 'Portrait 9:16 (Shorts/TikTok)', value: '9:16'},
                ]}
              />
              <Select 
                label="Voice Actor Engine" 
                value={formData.settings?.voice}
                onChange={e => updateSetting('voice', e.target.value)}
                options={[
                  {label: 'Kokoro: Heart (Female)', value: 'af_heart'},
                  {label: 'Kokoro: Bella (Female)', value: 'af_bella'},
                  {label: 'Kokoro: Michael (Male)', value: 'am_michael'},
                  {label: 'Edge-TTS: Jenny (Online)', value: 'en-US-JennyNeural'},
                ]}
              />
              <Select 
                label="Subtitle Overlay Style" 
                value={formData.settings?.subtitle_style}
                onChange={e => updateSetting('subtitle_style', e.target.value)}
                options={[
                  {label: 'Clean — White/Yellow', value: 'clean'},
                  {label: 'Bold — Cyberpunk Box', value: 'bold'},
                  {label: 'Cinematic — Lower Third', value: 'cinematic'},
                  {label: 'Minimal — Transparent', value: 'minimal'},
                ]}
              />
              <Select 
                label="Background Music (Auto-Ducked)" 
                value={formData.settings?.bg_music || 'ambient'}
                onChange={e => updateSetting('bg_music', e.target.value)}
                options={[
                  {label: 'Ambient — Warm Atmospheric (Auto-Ducked)', value: 'ambient'},
                  {label: 'Cinematic — Deep Synth (Auto-Ducked)', value: 'cinematic'},
                  {label: 'Lo-Fi — Warm Chill Beats (Auto-Ducked)', value: 'lofi'},
                  {label: 'Upbeat — Energetic Pulse (Auto-Ducked)', value: 'upbeat'},
                  {label: 'Dramatic — Low Resonance (Auto-Ducked)', value: 'dramatic'},
                  {label: 'None — Voiceover Only', value: 'none'},
                ]}
              />
            </div>
            
            <div className="pt-6 text-center">
              <Button size="lg" onClick={generateScriptPreview} isLoading={isGenerating}>
                <Wand2 className="w-5 h-5 mr-2" />
                Generate Script Preview
              </Button>
            </div>
          </div>
        )}

        {step === 4 && (
          <div className="animate-fade-in flex-1 flex flex-col h-full space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-xl font-bold">Script Preview & Scene Tags</h2>
                <p className="text-xs text-textMuted">Review generated scenes before rendering.</p>
              </div>
              <Button variant="secondary" size="sm" onClick={generateScriptPreview} isLoading={isGenerating}>
                Regenerate
              </Button>
            </div>

            <div className="flex-1 bg-background/90 rounded-xl border border-border p-4 font-mono text-xs text-emerald-400 leading-relaxed whitespace-pre-wrap overflow-y-auto min-h-[220px]">
              {script || "No script generated yet."}
            </div>
          </div>
        )}

        {step === 5 && (
          <div className="animate-fade-in flex-1 flex flex-col items-center justify-center text-center space-y-6 py-6">
            <div className="w-20 h-20 bg-accent/10 border border-accent/30 rounded-full flex items-center justify-center">
              <Sparkles className="w-10 h-10 text-accent" />
            </div>
            
            <div>
              <h2 className="text-3xl font-extrabold">Ready to Forge!</h2>
              <p className="text-textMuted mt-2 max-w-md mx-auto">
                Project <span className="text-accent font-bold">"{formData.title}"</span> is configured and ready for node-based rendering.
              </p>
            </div>

            <Button size="lg" onClick={handleLaunch} className="w-64 group relative overflow-hidden">
              <span className="relative z-10 flex items-center justify-center font-bold">
                Launch Node Pipeline
                <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
              </span>
            </Button>
          </div>
        )}

        {/* ── Navigation Footer ────────────────────────────────────────── */}
        <div className="flex justify-between items-center mt-8 pt-6 border-t border-border/50">
          <Button variant="ghost" onClick={handleBack} disabled={step === 1}>
            Back
          </Button>
          
          {step < 3 && (
            <Button onClick={handleNext} disabled={!formData.video_type || (step === 2 && !formData.topic)}>
              Next Step
            </Button>
          )}
          {step === 4 && (
            <Button onClick={handleNext}>
              Approve Script & Continue
            </Button>
          )}
        </div>
      </div>
    </div>
  );
};
