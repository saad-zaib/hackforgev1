import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Target, Cpu, Zap, TrendingUp, Activity, Play, Shield, Server, Terminal, ChevronRight, Sparkles, AlertCircle } from 'lucide-react';
import api from '../services/api';

const ModernDashboard = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState({
    blueprints: 0,
    machines: 0,
    campaigns: 0,
    running: 0
  });
  const [dockerStatus, setDockerStatus] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
    // Poll docker status every 5 seconds
    const interval = setInterval(fetchDockerStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      // Fetch stats and docker status in parallel
      const [statsData, dockerData] = await Promise.all([
        api.getStats(),
        api.getDockerStatus()
      ]);

      setStats({
        blueprints: statsData.total_blueprints || 0,
        machines: statsData.total_machines || 0,
        campaigns: statsData.total_campaigns || 0,
        running: dockerData.running || 0
      });

      setDockerStatus(dockerData);
      setIsLoading(false);
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
      setError(err.message);
      setIsLoading(false);
    }
  };

  const fetchDockerStatus = async () => {
    try {
      const dockerData = await api.getDockerStatus();
      setDockerStatus(dockerData);
      setStats(prev => ({ ...prev, running: dockerData.running || 0 }));
    } catch (err) {
      console.error('Error fetching docker status:', err);
    }
  };

  const StatCard = ({ icon: Icon, label, value, gradient, delay, isLive }) => (
    <div 
      className="relative group overflow-hidden rounded-2xl p-6 transition-all duration-500 hover:scale-105"
      style={{
        background: 'linear-gradient(135deg, rgba(20, 20, 20, 0.95) 0%, rgba(30, 30, 30, 0.95) 100%)',
        border: '1px solid rgba(255, 115, 0, 0.2)',
        animation: `slideUp 0.6s ease-out ${delay}s both`
      }}
    >
      <div className="absolute inset-0 bg-gradient-to-br from-orange-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
      
      <div className="relative z-10">
        <div className="flex items-center justify-between mb-4">
          <div 
            className="p-3 rounded-xl transition-all duration-300 group-hover:scale-110"
            style={{
              background: gradient,
              boxShadow: '0 8px 16px -4px rgba(255, 115, 0, 0.3)'
            }}
          >
            <Icon className="w-6 h-6 text-white" />
          </div>
          {isLive && <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />}
        </div>
        
        <div className="space-y-1">
          <p className="text-gray-400 text-sm font-medium tracking-wide">{label}</p>
          <p className="text-4xl font-bold text-white">{value}</p>
        </div>
      </div>

      <div className="absolute bottom-0 left-0 w-full h-1 bg-gradient-to-r from-orange-500 to-orange-600 transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500" />
    </div>
  );

  const QuickActionButton = ({ icon: Icon, label, color, onClick }) => (
    <button
      onClick={onClick}
      className="group relative overflow-hidden rounded-xl p-5 transition-all duration-300 hover:scale-105 active:scale-95"
      style={{
        background: `linear-gradient(135deg, ${color}15 0%, ${color}05 100%)`,
        border: `1px solid ${color}40`
      }}
    >
      <div className="absolute inset-0 bg-gradient-to-r opacity-0 group-hover:opacity-100 transition-opacity duration-300"
        style={{ background: `linear-gradient(135deg, ${color}20, transparent)` }}
      />
      
      <div className="relative z-10 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div 
            className="p-2.5 rounded-lg"
            style={{ backgroundColor: `${color}25` }}
          >
            <Icon className="w-5 h-5" style={{ color }} />
          </div>
          <span className="text-white font-semibold">{label}</span>
        </div>
        <ChevronRight 
          className="w-5 h-5 text-gray-400 group-hover:text-orange-500 transform group-hover:translate-x-1 transition-all" 
        />
      </div>
    </button>
  );

  if (isLoading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-center">
          <div className="relative w-20 h-20 mx-auto mb-4">
            <div className="absolute inset-0 rounded-full border-4 border-orange-500/20" />
            <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-orange-500 animate-spin" />
          </div>
          <p className="text-orange-500 font-semibold">Loading HackForge...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center p-6">
        <div className="max-w-md w-full bg-red-950/20 border border-red-500/50 rounded-2xl p-8 text-center">
          <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-white mb-2">Connection Error</h2>
          <p className="text-gray-400 mb-6">{error}</p>
          <button
            onClick={fetchDashboardData}
            className="px-6 py-3 bg-orange-500 hover:bg-orange-600 text-white rounded-lg transition-colors"
          >
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-white">
      <style>{`
        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Hero Section */}
        <div className="mb-8">
          <h2 className="text-4xl font-bold mb-2 bg-gradient-to-r from-white via-orange-500 to-orange-600 bg-clip-text text-transparent">
            Welcome back, Hacker 👾
          </h2>
          <p className="text-gray-400">Ready to level up your cybersecurity skills?</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard 
            icon={Shield} 
            label="Blueprints" 
            value={stats.blueprints}
            gradient="linear-gradient(135deg, #ff7300 0%, #ff9500 100%)"
            delay={0}
          />
          <StatCard 
            icon={Server} 
            label="Machines" 
            value={stats.machines}
            gradient="linear-gradient(135deg, #ff7300 0%, #ff9500 100%)"
            delay={0.1}
          />
          <StatCard 
            icon={Zap} 
            label="Campaigns" 
            value={stats.campaigns}
            gradient="linear-gradient(135deg, #ff7300 0%, #ff9500 100%)"
            delay={0.2}
          />
          <StatCard 
            icon={Activity} 
            label="Running" 
            value={stats.running}
            gradient="linear-gradient(135deg, #10b981 0%, #059669 100%)"
            delay={0.3}
            isLive={true}
          />
        </div>

        {/* Quick Actions */}
        <div className="mb-8">
          <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-orange-500" />
            Quick Actions
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <QuickActionButton 
              icon={Play} 
              label="Create Campaign" 
              color="#ff7300"
              onClick={() => navigate('/campaigns')}
            />
            <QuickActionButton 
              icon={Cpu} 
              label="View Machines" 
              color="#ff7300"
              onClick={() => navigate('/machines')}
            />
            <QuickActionButton 
              icon={Terminal} 
              label="Docker Control" 
              color="#0ea5e9"
              onClick={() => navigate('/docker')}
            />
          </div>
        </div>

        {/* Docker Status & System Info */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Docker Status */}
          <div className="rounded-2xl p-6 border border-gray-900 bg-gradient-to-br from-gray-900/50 to-black/50 backdrop-blur">
            <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
              <Terminal className="w-5 h-5 text-blue-500" />
              Docker Status
            </h3>
            {dockerStatus && (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-gray-400">Total Containers</span>
                  <span className="text-white font-semibold">{dockerStatus.total}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-400">Running</span>
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                    <span className="text-green-500 font-semibold">{dockerStatus.running}</span>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-400">Stopped</span>
                  <span className="text-gray-500 font-semibold">{dockerStatus.total - dockerStatus.running}</span>
                </div>
              </div>
            )}
          </div>

          {/* System Status */}
          <div className="rounded-2xl p-6 border border-gray-900 bg-gradient-to-br from-gray-900/50 to-black/50 backdrop-blur">
            <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
              <Activity className="w-5 h-5 text-green-500" />
              System Health
            </h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-gray-400">API Server</span>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                  <span className="text-green-500 text-sm font-semibold">Online</span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Database</span>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                  <span className="text-green-500 text-sm font-semibold">Connected</span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Docker Engine</span>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                  <span className="text-green-500 text-sm font-semibold">Running</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default ModernDashboard;
