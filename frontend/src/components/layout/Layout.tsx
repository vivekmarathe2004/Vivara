import React from 'react';
import { Sidebar } from './Sidebar';
import { ToastContainer } from '../ui/Toast';

export const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar />
      <main className="flex-1 ml-64 min-h-screen pb-12 relative z-0">
        <div className="absolute top-0 left-0 right-0 h-64 bg-gradient-to-b from-accent/5 to-transparent pointer-events-none -z-10" />
        {children}
      </main>
      <ToastContainer />
    </div>
  );
};
