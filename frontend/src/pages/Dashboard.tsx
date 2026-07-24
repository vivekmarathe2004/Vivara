import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { VideoCard } from '../components/ui/VideoCard';
import { EmptyState } from '../components/ui/EmptyState';
import { useProjectStore } from '../store/projectStore';
import { 
  Trophy, Star, Lightbulb, Smartphone, Film, BookOpen, Scissors, 
  FolderOpen, Sparkles, Cpu, Zap, ArrowRight, Layers, FileText,
  Play, Gamepad2, Mic
} from 'lucide-react';

export const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { projects, fetchProjects, isLoading } = useProjectStore();

  useEffect(() => {
    fetchProjects();
  }, []);

  const workflows = [
    { type: 'ranking', name: 'Top 10 & Rankings', desc: 'Countdown listicles, top 5, comparison countdowns', icon: Trophy, badge: 'Viral Concept', color: 'text-amber-400 border-amber-500/30 hover:border-amber-400' },
    { type: 'review', name: 'Movie & Game Reviews', desc: 'Detailed breakdown, pros/cons, score rating', icon: Star, badge: 'High Engagement', color: 'text-blue-400 border-blue-500/30 hover:border-blue-400' },
    { type: 'explainer', name: 'Explainer & Lore', desc: 'Deep dive, problem breakdown, key takeaways', icon: Lightbulb, badge: 'Educational', color: 'text-purple-400 border-purple-500/30 hover:border-purple-400' },
    { type: 'shorts', name: 'YouTube Shorts & Reels', desc: 'Vertical 9:16, punchy 3s hook under 60s', icon: Smartphone, badge: 'Fast Track', color: 'text-pink-400 border-pink-500/30 hover:border-pink-400' },
    { type: 'documentary', name: 'Cinematic Documentary', desc: 'Historical arcs, mystery, atmospheric storytelling', icon: Film, badge: 'Long Form', color: 'text-cyan-400 border-cyan-500/30 hover:border-cyan-400' },
    { type: 'educational', name: 'Educational & Courses', desc: 'Step-by-step guides, summaries, tutorials', icon: BookOpen, badge: 'Evergreen', color: 'text-emerald-400 border-emerald-500/30 hover:border-emerald-400' },
    { type: 'news', name: 'Tech & Gaming News', desc: 'Daily headlines, fast summaries, trending updates', icon: Gamepad2, badge: 'Trending', color: 'text-orange-400 border-orange-500/30 hover:border-orange-400' },
    { type: 'podcast', name: 'Podcast Highlights', desc: 'Speaker zoom, audio spikes, dynamic captions', icon: Mic, badge: 'Clip Intel', color: 'text-fuchsia-400 border-fuchsia-500/30 hover:border-fuchsia-400' },
  ];

  const creatorTemplates = [
    { title: 'Top 10 Sci-Fi Movies 2026', type: 'ranking' },
    { title: 'Cyberpunk 2077 DLC Review', type: 'review' },
    { title: 'How Quantum Computers Work', type: 'explainer' },
    { title: 'The History of Ancient Rome', type: 'documentary' },
  ];

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-10 animate-fade-in">
      
      {/* ── Studio Header ────────────────────────────────────────────── */}
      <header className="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-accent/10 border border-accent/20 text-accent text-xs font-semibold mb-2">
            <Sparkles className="w-3.5 h-3.5" />
            <span>AI Creator Studio 2.0</span>
          </div>
          <h1 className="text-3xl font-bold tracking-tight">
            Welcome to <span className="gradient-text">Vivara</span> Studio
          </h1>
          <p className="text-textMuted text-sm mt-1">Transform ideas & clips into videos with modular AI pipelines.</p>
        </div>

        <div className="flex items-center gap-3">
          <button 
            onClick={() => navigate('/clip')}
            className="px-4 py-2 rounded-lg bg-surface border border-accent3/30 text-accent3 hover:bg-accent3/10 font-medium text-sm flex items-center gap-2 transition-colors cursor-pointer"
          >
            <Scissors className="w-4 h-4" />
            Clip Mode
          </button>
          <button 
            onClick={() => navigate('/new')}
            className="gradient-btn flex items-center gap-2 text-sm px-4 py-2 cursor-pointer"
          >
            <Zap className="w-4 h-4" />
            New Creation
          </button>
        </div>
      </header>

      {/* ── Stats & Status Cards ────────────────────────────────────── */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
        <div className="glass-card p-5">
          <div className="flex items-center justify-between">
            <p className="text-xs font-semibold text-textMuted uppercase tracking-wider">Total Creations</p>
            <div className="p-2 rounded-lg bg-accent/10 text-accent"><Film className="w-4 h-4" /></div>
          </div>
          <p className="text-3xl font-bold mt-2">{projects.length}</p>
        </div>

        <div className="glass-card p-5">
          <div className="flex items-center justify-between">
            <p className="text-xs font-semibold text-textMuted uppercase tracking-wider">Hours Saved</p>
            <div className="p-2 rounded-lg bg-accent2/10 text-accent2"><Zap className="w-4 h-4" /></div>
          </div>
          <p className="text-3xl font-bold mt-2">~{projects.length * 4.5}h</p>
        </div>

        <div className="glass-card p-5">
          <div className="flex items-center justify-between">
            <p className="text-xs font-semibold text-textMuted uppercase tracking-wider">AI Engine Router</p>
            <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400"><Cpu className="w-4 h-4" /></div>
          </div>
          <div className="flex items-center gap-2 mt-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
            <p className="font-bold text-sm">OmniRoute Gateway</p>
          </div>
        </div>

        <div 
          onClick={() => navigate('/clip')}
          className="glass-card p-5 border-cyan-500/30 cursor-pointer hover:border-cyan-400 group transition-all"
        >
          <div className="flex items-center justify-between">
            <p className="text-xs font-semibold text-cyan-400 uppercase tracking-wider">Clip Intelligence</p>
            <div className="p-2 rounded-lg bg-cyan-500/10 text-cyan-400"><Scissors className="w-4 h-4" /></div>
          </div>
          <p className="font-bold text-sm mt-2 flex items-center justify-between">
            <span>Repurpose Long Video</span>
            <ArrowRight className="w-4 h-4 text-cyan-400 group-hover:translate-x-1 transition-transform" />
          </p>
        </div>
      </div>

      {/* ── Visual Execution Pipeline Preview ────────────── */}
      <section className="glass-card p-6 border-border/60">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Layers className="w-5 h-5 text-accent" />
            <h2 className="text-lg font-bold">Modular DAG Execution Graph</h2>
          </div>
          <span className="text-xs font-mono text-textMuted bg-surface px-3 py-1 rounded-full border border-border">
            Node Pipeline Ready
          </span>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-5 gap-3 pt-1">
          {[
            { step: '01', name: 'Research & Prompt', icon: FileText, color: 'text-amber-400 border-amber-500/30' },
            { step: '02', name: 'AI Voice Synth', icon: Cpu, color: 'text-purple-400 border-purple-500/30' },
            { step: '03', name: 'Auto Subtitles', icon: Sparkles, color: 'text-pink-400 border-pink-500/30' },
            { step: '04', name: 'Stock Media Match', icon: Film, color: 'text-cyan-400 border-cyan-500/30' },
            { step: '05', name: 'GPU FFmpeg Render', icon: Zap, color: 'text-emerald-400 border-emerald-500/30' },
          ].map((node, i) => (
            <div key={i} className={`p-3.5 rounded-lg bg-surface border ${node.color} flex flex-col justify-between`}>
              <div className="flex items-center justify-between text-xs font-mono opacity-70">
                <span>NODE_{node.step}</span>
                <node.icon className="w-4 h-4" />
              </div>
              <p className="font-bold text-sm mt-3">{node.name}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── Workflow Studio Cards ────────────────────────────────────── */}
      <section className="space-y-4">
        <div>
          <h2 className="text-xl font-bold tracking-tight">Workflow Platforms</h2>
          <p className="text-xs text-textMuted mt-0.5">Pick a tailored creator workflow with pre-configured prompts.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {workflows.map((wf) => (
            <div 
              key={wf.type}
              onClick={() => navigate(`/new?type=${wf.type}`)}
              className={`p-5 rounded-xl bg-surface border cursor-pointer transition-all ${wf.color} group relative`}
            >
              <div className="flex items-center justify-between mb-3">
                <div className="p-2.5 rounded-lg bg-background border border-border">
                  <wf.icon className="w-5 h-5" />
                </div>
                <span className="text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded bg-background border border-border">
                  {wf.badge}
                </span>
              </div>
              <h3 className="font-bold text-base mb-1">{wf.name}</h3>
              <p className="text-xs text-textMuted leading-relaxed">{wf.desc}</p>
              
              <div className="mt-4 pt-3 border-t border-border/50 flex items-center justify-between text-xs font-medium">
                <span>Start Workflow</span>
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ── 1-Click Creator Templates ────────────────────────────────── */}
      <section className="glass-card p-5 space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-amber-400" />
            <h2 className="text-base font-bold">1-Click Creator Templates</h2>
          </div>
          <span className="text-xs text-textMuted">Preconfigured prompts & styles</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
          {creatorTemplates.map((tmpl, idx) => (
            <button
              key={idx}
              onClick={() => navigate(`/new?type=${tmpl.type}&topic=${encodeURIComponent(tmpl.title)}`)}
              className="p-3 rounded-lg bg-surface border border-border hover:border-accent/50 text-left transition-colors text-xs font-medium flex items-center justify-between group cursor-pointer"
            >
              <span className="truncate pr-2">{tmpl.title}</span>
              <Play className="w-3.5 h-3.5 text-accent opacity-0 group-hover:opacity-100 transition-opacity shrink-0" />
            </button>
          ))}
        </div>
      </section>

      {/* ── Recent Projects Grid ────────────────────────────────────── */}
      <section className="space-y-4">
        <h2 className="text-xl font-bold tracking-tight">Recent Projects</h2>
        
        {isLoading ? (
          <div className="flex justify-center p-12">
            <div className="w-8 h-8 rounded-full border-2 border-accent border-t-transparent animate-spin" />
          </div>
        ) : projects.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {projects.slice(0, 8).map(project => (
              <VideoCard 
                key={project.id} 
                project={project} 
                onClick={(p) => navigate(`/project/${p.id}`)} 
              />
            ))}
          </div>
        ) : (
          <EmptyState
            icon={FolderOpen}
            title="No video creations yet"
            description="Pick a workflow platform above to launch your first AI video creation."
          />
        )}
      </section>
    </div>
  );
};
