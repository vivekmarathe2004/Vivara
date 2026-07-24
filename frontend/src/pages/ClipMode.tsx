import React, { useState } from 'react';
import { 
  Upload, Link as LinkIcon, Download, Search, Scissors, Play, 
  Radio, Zap, Volume2, Eye, FileVideo
} from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Select } from '../components/ui/Select';
import { Badge } from '../components/ui/Badge';
import { ProgressBar } from '../components/ui/ProgressBar';
import { useToast } from '../hooks/useToast';

export const ClipMode: React.FC = () => {
  const [step, setStep] = useState(1);
  const [url, setUrl] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [progress, setProgress] = useState(0);
  const { addToast } = useToast();

  const handleAnalyze = () => {
    setIsAnalyzing(true);
    let pct = 0;
    const interval = setInterval(() => {
      pct += 20;
      setProgress(pct);
      if (pct >= 100) {
        clearInterval(interval);
        setIsAnalyzing(false);
        setStep(3);
        addToast({ type: 'success', message: 'Clip Intelligence extracted 3 viral Shorts!' });
      }
    }, 400);
  };

  const clips = [
    { id: 1, title: 'Unbelievable Tech Secret', start: '00:45', end: '01:23', duration: '38s', score: 98, hook: '"You won\'t believe what happened when we pushed this model to its maximum limits..."', audioSpike: 'Laughter + Applause Detected' },
    { id: 2, title: 'The Ultimate Conclusion', start: '04:12', end: '04:55', duration: '43s', score: 94, hook: '"In the end, the secret comes down to execution and discipline..."', audioSpike: 'Silence Removed (1.4s)' },
    { id: 3, title: 'Mind-Blowing Feature Revealed', start: '08:30', end: '09:10', duration: '40s', score: 91, hook: '"This single feature changes the entire game forever..."', audioSpike: 'Scene Cut + Face Zoom' },
  ];

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-8 animate-fade-in relative">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 relative z-10">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-xs font-semibold mb-3">
            <Radio className="w-3.5 h-3.5" />
            <span>Clip Intelligence Engine v2.0</span>
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight flex items-center gap-3">
            <Scissors className="text-cyan-400" /> Repurpose Studio
          </h1>
          <p className="text-sm text-textMuted mt-1">
            Turn long podcasts & videos into multi-Short viral clips with auto-captions and face tracking.
          </p>
        </div>

        {/* Intelligence feature badges */}
        <div className="flex flex-wrap gap-2 text-[11px] font-mono font-semibold">
          <span className="px-2.5 py-1 rounded-lg bg-surface border border-cyan-500/30 text-cyan-400 flex items-center gap-1.5">
            <Volume2 className="w-3 h-3" /> Silence Removal
          </span>
          <span className="px-2.5 py-1 rounded-lg bg-surface border border-purple-500/30 text-purple-400 flex items-center gap-1.5">
            <Eye className="w-3 h-3" /> Scene Cut Detect
          </span>
          <span className="px-2.5 py-1 rounded-lg bg-surface border border-pink-500/30 text-pink-400 flex items-center gap-1.5">
            <Zap className="w-3 h-3" /> Viral Hook Finder
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 relative z-10">
        
        {/* Left Column: Workflow Stepper */}
        <div className="lg:col-span-1 space-y-4">
          
          {/* Step 1: Import */}
          <div className={`p-5 rounded-2xl border-2 transition-all ${step === 1 ? 'border-cyan-400 bg-cyan-500/10' : 'border-border/60 bg-surface/60 opacity-75'}`}>
            <h3 className="font-bold flex items-center gap-2 mb-3">
              <span className="w-6 h-6 rounded-full bg-cyan-500/20 text-cyan-400 border border-cyan-500/40 flex items-center justify-center text-xs font-mono">1</span> 
              Import Source Video
            </h3>

            {step === 1 ? (
              <div className="space-y-4">
                <div className="p-6 border-2 border-dashed border-border/80 rounded-xl text-center hover:border-cyan-400 hover:bg-cyan-500/5 transition-all cursor-pointer group">
                  <Upload className="w-8 h-8 mx-auto text-cyan-400 mb-2 group-hover:scale-110 transition-transform" />
                  <p className="text-xs font-bold">Drop MP4 / MOV file here</p>
                  <p className="text-[11px] text-textMuted mt-1">Or click to browse local storage</p>
                </div>

                <div className="flex items-center gap-2">
                  <div className="flex-1 h-px bg-border/60"></div>
                  <span className="text-[10px] text-textMuted uppercase font-mono">OR URL</span>
                  <div className="flex-1 h-px bg-border/60"></div>
                </div>

                <Input 
                  placeholder="Paste YouTube video link..." 
                  icon={LinkIcon} 
                  value={url}
                  onChange={e => setUrl(e.target.value)}
                />

                <Button className="w-full bg-cyan-500 hover:bg-cyan-400 text-black font-bold" onClick={() => setStep(2)}>
                  Import Media Source
                </Button>
              </div>
            ) : (
              <Button variant="ghost" size="sm" className="w-full text-xs" onClick={() => setStep(1)}>Change Media Source</Button>
            )}
          </div>

          {/* Step 2: Analyze */}
          <div className={`p-5 rounded-2xl border-2 transition-all ${step === 2 ? 'border-cyan-400 bg-cyan-500/10' : 'border-border/60 bg-surface/60 opacity-75'}`}>
            <h3 className="font-bold flex items-center gap-2 mb-3">
              <span className="w-6 h-6 rounded-full bg-cyan-500/20 text-cyan-400 border border-cyan-500/40 flex items-center justify-center text-xs font-mono">2</span> 
              Clip Intelligence Scan
            </h3>

            {step === 2 && (
              <div className="space-y-4">
                <p className="text-xs text-textMuted leading-relaxed">
                  Faster-Whisper and LLM will analyze audio spikes, laughter, and scene cuts to extract top moments.
                </p>
                {isAnalyzing && <ProgressBar progress={progress} />}
                <Button 
                  className="w-full bg-cyan-500 hover:bg-cyan-400 text-black font-bold" 
                  onClick={handleAnalyze}
                  isLoading={isAnalyzing}
                >
                  <Search className="w-4 h-4 mr-2" /> Scan & Find Viral Highlights
                </Button>
              </div>
            )}
          </div>

          {/* Step 3: Export */}
          <div className={`p-5 rounded-2xl border-2 transition-all ${step === 3 ? 'border-cyan-400 bg-cyan-500/10' : 'border-border/60 bg-surface/60 opacity-75'}`}>
            <h3 className="font-bold flex items-center gap-2 mb-3">
              <span className="w-6 h-6 rounded-full bg-cyan-500/20 text-cyan-400 border border-cyan-500/40 flex items-center justify-center text-xs font-mono">3</span> 
              Captioning & Render
            </h3>

            {step === 3 && (
              <div className="space-y-4">
                <Select 
                  label="Caption Preset"
                  options={[
                    {label: 'Hormozi — Animated Yellow/White Box', value: 'hormozi'},
                    {label: 'Minimalist — Clean Subtitles', value: 'minimal'},
                    {label: 'Cinematic — Lower Third', value: 'cinematic'},
                  ]}
                />
                <Select 
                  label="Auto-Crop & Speaker Tracking"
                  options={[
                    {label: 'Smart Face Zoom (Active Speaker)', value: 'aggressive'},
                    {label: 'Subtle Center Crop (9:16)', value: 'subtle'},
                    {label: 'No Zoom (Center Box)', value: 'off'},
                  ]}
                />
                <Button className="w-full bg-cyan-500 hover:bg-cyan-400 text-black font-bold">
                  <Download className="w-4 h-4 mr-2" /> Export All 3 Shorts (.mp4)
                </Button>
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Interactive Workspace Preview */}
        <div className="lg:col-span-2">
          <div className="glass-card border-border/60 h-full min-h-[580px] flex flex-col overflow-hidden">
            <div className="p-4 border-b border-border/50 bg-surface/60 backdrop-blur-xl flex justify-between items-center">
              <div className="flex items-center gap-2">
                <FileVideo className="w-4 h-4 text-cyan-400" />
                <h2 className="font-bold text-sm">Clip Intelligence Workspace</h2>
              </div>
              {step === 3 && <Badge status="done" />}
            </div>
            
            <div className="flex-1 p-6 flex flex-col bg-background/50">
              {step === 1 && (
                <div className="flex-1 flex flex-col items-center justify-center text-center text-textMuted py-12 space-y-4">
                  <Upload className="w-16 h-16 opacity-20 text-cyan-400 animate-pulse" />
                  <div>
                    <h3 className="font-bold text-lg text-text">No Video Imported</h3>
                    <p className="text-xs text-textMuted mt-1">Import a video file or YouTube URL on the left panel.</p>
                  </div>
                </div>
              )}
              
              {step === 2 && (
                <div className="flex-1 flex flex-col items-center justify-center text-center space-y-6">
                  <div className="w-full max-w-lg aspect-video bg-black rounded-2xl border border-cyan-500/40 flex items-center justify-center relative overflow-hidden shadow-[0_0_30px_rgba(6,182,212,0.2)]">
                     <Play className="w-14 h-14 text-cyan-400 animate-pulse" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold">Source Video Ready</h3>
                    <p className="text-xs text-textMuted mt-1">Click 'Scan & Find Viral Highlights' to begin multi-modal AI analysis.</p>
                  </div>
                </div>
              )}
              
              {step === 3 && (
                <div className="space-y-4 overflow-y-auto pr-2 custom-scrollbar">
                  {clips.map((c) => (
                    <div key={c.id} className="p-4 rounded-2xl bg-surface/80 border border-border/60 hover:border-cyan-400/60 transition-all flex gap-4">
                      
                      {/* Vertical Short Thumbnail Preview */}
                      <div className="w-28 aspect-[9/16] bg-black rounded-xl border border-cyan-500/30 overflow-hidden relative shrink-0 flex items-center justify-center">
                         <Play className="w-8 h-8 text-cyan-400 opacity-80" />
                         <span className="absolute bottom-1 right-1 text-[9px] font-mono bg-black/80 text-white px-1.5 py-0.5 rounded">
                           9:16
                         </span>
                      </div>

                      <div className="flex-1 flex flex-col justify-between">
                        <div>
                          <div className="flex items-center justify-between mb-1">
                            <h4 className="font-bold text-base text-text">{c.title}</h4>
                            <span className="text-xs font-mono font-bold bg-cyan-500/20 text-cyan-400 border border-cyan-500/40 px-2.5 py-0.5 rounded-full">
                              Score: {c.score}/100
                            </span>
                          </div>

                          <div className="flex items-center gap-3 text-xs text-textMuted mb-2">
                            <span>Time: {c.start} - {c.end} ({c.duration})</span>
                            <span className="text-[10px] text-pink-400 bg-pink-500/10 px-2 py-0.5 rounded font-mono">
                              ⚡ {c.audioSpike}
                            </span>
                          </div>

                          <p className="text-xs italic text-emerald-400 bg-background/80 p-2.5 rounded-xl border border-border/50 font-mono leading-relaxed line-clamp-2">
                            {c.hook}
                          </p>
                        </div>

                        <div className="flex gap-2 mt-3">
                          <Button size="sm" variant="secondary" className="text-xs">
                            <Play className="w-3 h-3 mr-1 text-cyan-400" /> Preview Clip
                          </Button>
                          <Button size="sm" variant="ghost" className="text-xs">
                            <Scissors className="w-3 h-3 mr-1" /> Trim Cut
                          </Button>
                        </div>
                      </div>

                    </div>
                  ))}
                </div>
              )}

            </div>
          </div>
        </div>
        
      </div>
    </div>
  );
};
