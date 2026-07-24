import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/Button';
import { CheckCircle2, XCircle, ChevronRight, Settings, Cpu } from 'lucide-react';

export const SetupWizard: React.FC = () => {
  const [step, setStep] = React.useState(1);
  const navigate = useNavigate();

  const handleFinish = () => {
    localStorage.setItem('setup_complete', 'true');
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center p-6 relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-accent/20 rounded-full blur-[120px] pointer-events-none" />
      
      <div className="w-full max-w-2xl z-10">
        <div className="glass-card p-10 border-border/50 shadow-2xl relative overflow-hidden">
          {/* Active step progress indicator */}
          <div className="absolute top-0 left-0 h-1 bg-surface w-full">
            <div 
              className="h-full bg-gradient-to-r from-accent to-accent2 transition-all duration-500 ease-out"
              style={{ width: `${(step / 5) * 100}%` }}
            />
          </div>

          {step === 1 && (
            <div className="text-center animate-fade-in space-y-6 py-8">
              <div className="inline-flex items-center justify-center w-24 h-24 rounded-2xl overflow-hidden mb-4 shadow-[0_0_40px_rgba(108,99,255,0.4)]">
                <img src="/logo.jpg" alt="Vivara" className="w-full h-full object-cover" />
              </div>
              <h1 className="text-4xl font-bold tracking-tight">
                Welcome to <span className="gradient-text">Vivara</span>
              </h1>
              <p className="text-lg text-textMuted max-w-md mx-auto">
                The free, open-source AI video studio running completely on your machine.
              </p>
              <div className="pt-8">
                <Button size="lg" onClick={() => setStep(2)} className="w-48 group">
                  Let's get set up
                  <ChevronRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
                </Button>
              </div>
            </div>
          )}

          {step === 2 && (
            <div className="animate-fade-in space-y-6">
              <div className="text-center mb-8">
                <h2 className="text-2xl font-bold">System Scan</h2>
                <p className="text-textMuted">Checking for required dependencies</p>
              </div>
              
              <div className="space-y-3">
                {[
                  { name: 'FFmpeg', ok: true, desc: 'Video processing engine' },
                  { name: 'NVIDIA GPU', ok: true, desc: 'Hardware acceleration (NVENC)' },
                  { name: 'OmniRoute Router', ok: true, desc: 'Universal AI gateway router' },
                  { name: 'Kokoro TTS', ok: false, desc: 'Offline voice synthesis' },
                  { name: 'Faster-Whisper', ok: true, desc: 'Subtitles & speech recognition' },
                ].map((item, i) => (
                  <div key={i} className="flex items-center justify-between p-4 bg-surface rounded-xl border border-border/50">
                    <div className="flex items-center gap-3">
                      {item.ok ? <CheckCircle2 className="w-6 h-6 text-success" /> : <XCircle className="w-6 h-6 text-error" />}
                      <div>
                        <p className="font-medium text-text">{item.name}</p>
                        <p className="text-xs text-textMuted">{item.desc}</p>
                      </div>
                    </div>
                    {!item.ok && (
                      <Button variant="secondary" size="sm">Install</Button>
                    )}
                  </div>
                ))}
              </div>
              
              <div className="flex justify-between pt-6">
                <Button variant="ghost" onClick={() => setStep(1)}>Back</Button>
                <Button variant="primary" onClick={() => setStep(3)}>Continue</Button>
              </div>
            </div>
          )}

          {step === 3 && (
            <div className="animate-fade-in space-y-6">
              <div className="text-center mb-6">
                <h2 className="text-2xl font-bold">Free Stock Media & Voice Keys</h2>
                <p className="text-xs text-textMuted mt-1">All keys are optional. Openverse open license media works with no key required!</p>
              </div>
              
              <div className="space-y-3 max-h-[340px] overflow-y-auto pr-2 custom-scrollbar">
                <div className="p-4 bg-surface rounded-xl border border-border/50 space-y-2">
                  <label className="block text-xs font-bold text-text">Pexels API Key (Free 200 req/hr)</label>
                  <input type="password" placeholder="Paste free key..." className="w-full bg-background border border-border rounded-lg p-2 text-xs focus:border-accent outline-none" />
                  <a href="https://www.pexels.com/api/" target="_blank" rel="noreferrer" className="text-[11px] text-accent hover:underline block">Get free Pexels key →</a>
                </div>
                
                <div className="p-4 bg-surface rounded-xl border border-border/50 space-y-2">
                  <label className="block text-xs font-bold text-text">Pixabay API Key (Free tier)</label>
                  <input type="password" placeholder="Paste free key..." className="w-full bg-background border border-border rounded-lg p-2 text-xs focus:border-accent outline-none" />
                  <a href="https://pixabay.com/api/docs/" target="_blank" rel="noreferrer" className="text-[11px] text-accent hover:underline block">Get free Pixabay key →</a>
                </div>

                <div className="p-4 bg-surface rounded-xl border border-border/50 space-y-2">
                  <label className="block text-xs font-bold text-text">Unsplash API Key (Free photos, 50 req/hr)</label>
                  <input type="password" placeholder="Paste free key..." className="w-full bg-background border border-border rounded-lg p-2 text-xs focus:border-accent outline-none" />
                  <a href="https://unsplash.com/developers" target="_blank" rel="noreferrer" className="text-[11px] text-accent hover:underline block">Get free Unsplash key →</a>
                </div>

                <div className="p-4 bg-surface rounded-xl border border-border/50 space-y-2">
                  <label className="block text-xs font-bold text-text">ElevenLabs API Key (Free 10,000 chars/mo)</label>
                  <input type="password" placeholder="Paste free key..." className="w-full bg-background border border-border rounded-lg p-2 text-xs focus:border-accent outline-none" />
                  <a href="https://elevenlabs.io/app/speech-synthesis" target="_blank" rel="noreferrer" className="text-[11px] text-accent hover:underline block">Get free ElevenLabs key →</a>
                </div>
              </div>
              
              <div className="flex justify-between pt-4">
                <Button variant="ghost" onClick={() => setStep(2)}>Back</Button>
                <div className="space-x-3">
                  <Button variant="ghost" onClick={() => setStep(4)}>Skip All</Button>
                  <Button variant="primary" onClick={() => setStep(4)}>Save & Continue</Button>
                </div>
              </div>
            </div>
          )}
          
          {step === 4 && (
            <div className="animate-fade-in space-y-6">
              <div className="text-center mb-6">
                <h2 className="text-2xl font-bold">OmniRoute AI Gateway</h2>
                <p className="text-textMuted text-xs">Universal model router for local & cloud AI models</p>
              </div>
              
              <div className="p-5 bg-accent/10 border-2 border-accent rounded-xl">
                <div className="flex items-center gap-3">
                  <Cpu className="w-8 h-8 text-accent" />
                  <div>
                    <h3 className="font-bold text-base">OmniRoute Universal AI Platform</h3>
                    <p className="text-xs text-textMuted mt-0.5">Unified OpenAI-compatible gateway running at http://localhost:20128/v1</p>
                  </div>
                </div>
              </div>
              
              <div className="p-5 bg-surface border border-border/50 rounded-xl space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-1">OmniRoute Base Endpoint URL</label>
                  <input type="text" defaultValue="http://localhost:20128/v1" className="w-full bg-background border border-border rounded-lg p-2.5 text-sm focus:border-accent outline-none" />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">OmniRoute Model Route</label>
                  <input type="text" defaultValue="auto" placeholder="e.g. auto, auto/best-free, auto/best-fast" className="w-full bg-background border border-border rounded-lg p-2.5 text-sm focus:border-accent outline-none" />
                </div>
              </div>
              
              <div className="flex justify-between pt-6">
                <Button variant="ghost" onClick={() => setStep(3)}>Back</Button>
                <Button variant="primary" onClick={() => setStep(5)}>Verify & Continue</Button>
              </div>
            </div>
          )}

          {step === 5 && (
            <div className="text-center animate-fade-in space-y-6 py-8">
              <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-success/20 mb-4">
                <CheckCircle2 className="w-10 h-10 text-success" />
              </div>
              <h2 className="text-3xl font-bold">You're all set!</h2>
              <p className="text-textMuted max-w-sm mx-auto">
                VistaForge is configured and ready. You can change these settings at any time.
              </p>
              
              <div className="pt-8">
                <Button size="lg" onClick={handleFinish} className="w-64 group relative overflow-hidden">
                  <div className="absolute inset-0 bg-white/20 animate-shimmer pointer-events-none" style={{ width: '200%' }} />
                  <span className="relative z-10 flex items-center justify-center pointer-events-none">
                    Start Creating <Settings className="w-5 h-5 ml-2 group-hover:rotate-90 transition-transform" />
                  </span>
                </Button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
