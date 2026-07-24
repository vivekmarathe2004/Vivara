import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, PlusSquare, Scissors, Settings, Cpu } from 'lucide-react';

export const Sidebar: React.FC = () => {
  const navItems = [
    { to: '/', icon: Home, label: 'Dashboard Studio' },
    { to: '/new', icon: PlusSquare, label: 'New Creation' },
    { to: '/clip', icon: Scissors, label: 'Clip Intelligence' },
    { to: '/settings', icon: Settings, label: 'Engine Settings' },
  ];

  return (
    <aside className="w-64 h-screen fixed left-0 top-0 border-r border-border/60 bg-[#07070c]/90 backdrop-blur-2xl z-40 flex flex-col justify-between">
      <div>
        {/* Brand Header */}
        <div className="p-6 flex items-center gap-3 border-b border-border/40">
          <div className="relative group">
            <img src="/logo.jpg" alt="Vivara" className="w-10 h-10 rounded-xl object-cover border border-border" />
            <span className="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 bg-emerald-400 border-2 border-background rounded-full" />
          </div>
          <div>
            <h1 className="text-xl font-extrabold tracking-tight leading-none">
              Vi<span className="gradient-text">vara</span>
            </h1>
            <span className="text-[10px] font-mono font-semibold text-textMuted uppercase tracking-wider">AI Creator Studio</span>
          </div>
        </div>

        {/* Nav list */}
        <nav className="px-4 py-6 space-y-2">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) => `
                flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group relative font-medium text-sm
                ${isActive 
                  ? 'bg-accent/15 text-accent font-semibold border border-accent/30' 
                  : 'text-textMuted hover:text-text hover:bg-surface/80 border border-transparent'
                }
              `}
            >
              <item.icon className="w-4 h-4 transition-transform group-hover:scale-110" />
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>
      </div>

      {/* Footer System Status */}
      <div className="p-4 m-4 rounded-2xl bg-surface/80 border border-border/60 backdrop-blur-md">
        <div className="flex items-center justify-between mb-2">
          <span className="text-[11px] font-bold text-accent font-mono">Vivara 2.0</span>
          <span className="text-[10px] bg-emerald-500/15 text-emerald-400 px-2 py-0.5 rounded-full font-mono font-semibold">Active</span>
        </div>
        <div className="flex items-center gap-2 text-xs text-textMuted">
          <Cpu className="w-3.5 h-3.5 text-accent animate-pulse" />
          <span className="truncate">OmniRoute AI Gateway</span>
        </div>
      </div>
    </aside>
  );
};
