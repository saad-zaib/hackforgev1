// src/App.js
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { Target, Home, Zap, Server, Terminal, User, Trophy } from 'lucide-react';

// Import components
import Dashboard from './components/Dashboard';
import Campaigns from './components/Campaigns';
import CampaignDetail from './components/CampaignDetail'; // NEW
import Machines from './components/Machines';
import DockerControl from './components/DockerControl';
import Leaderboard from './components/Leaderboard';
import Profile from './components/Profile';
import ContainerDebug from './components/ContainerDebug';
import ConfigManager from './components/ConfigManager';

// Navigation Component
const Navigation = () => {
  const location = useLocation();
  const [currentUserId] = useState('user_default');

  const isActive = (path) => location.pathname === path;

  const navItems = [
    { path: '/', icon: Home, label: 'Dashboard' },
    { path: '/campaigns', icon: Zap, label: 'Campaigns' },
    { path: '/machines', icon: Server, label: 'Machines' },
    { path: '/docker', icon: Terminal, label: 'Docker' },
    { path: '/leaderboard', icon: Trophy, label: 'Leaderboard' },
    { path: '/configs', icon: User, label: 'Config' },
  ];


  return (
    <header className="border-b border-gray-900 bg-black/50 backdrop-blur-xl sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-3">
            <div className="relative">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-orange-500 to-orange-600 flex items-center justify-center"
                style={{ animation: 'glow 2s ease-in-out infinite' }}>
                <Target className="w-6 h-6 text-white" />
              </div>
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
                HackForge
              </h1>
              <p className="text-xs text-gray-500">Cybersecurity Training</p>
            </div>
          </Link>

          {/* Navigation */}
          <nav className="flex items-center gap-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const active = isActive(item.path);
              
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all duration-300 ${
                    active
                      ? 'bg-orange-500/20 text-orange-500 border border-orange-500/50'
                      : 'text-gray-400 hover:text-white hover:bg-gray-900/50'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span className="text-sm font-medium">{item.label}</span>
                </Link>
              );
            })}
          </nav>
        </div>
      </div>

      <style>{`
        @keyframes glow {
          0%, 100% { box-shadow: 0 0 20px rgba(255, 115, 0, 0.3); }
          50% { box-shadow: 0 0 40px rgba(255, 115, 0, 0.6); }
        }
      `}</style>
    </header>
  );
};

// Main App Component
function App() {
  return (
    <Router>
      <div className="min-h-screen bg-black">
        <Navigation />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/campaigns" element={<Campaigns />} />
          <Route path="/campaigns/:campaignId" element={<CampaignDetail />} /> {/* NEW */}
          <Route path="/machines" element={<Machines />} />
          <Route path="/docker" element={<DockerControl />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/debug" element={<ContainerDebug />} />
	  <Route path="/configs" element={<ConfigManager />} />
      </Routes>
      </div>
    </Router>
  );
}

export default App;
