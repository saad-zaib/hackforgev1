import React, { useState, useEffect } from 'react';
import { Terminal, Play, Square, RefreshCw, Trash2, Activity, Loader, CheckCircle, AlertCircle, Server, FileText, Filter } from 'lucide-react';
import api from '../services/api';

const DockerControl = () => {
  const [userId] = useState('user_default');
  const [containers, setContainers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState({});
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [stats, setStats] = useState({ total: 0, running: 0 });
  const [containerLogs, setContainerLogs] = useState(null);
  
  // NEW: Campaign filtering
  const [myCampaigns, setMyCampaigns] = useState([]);
  const [selectedCampaign, setSelectedCampaign] = useState('all');
  const [filteredContainers, setFilteredContainers] = useState([]);

  useEffect(() => {
    fetchMyCampaigns();
    fetchDockerStatus();
    const interval = setInterval(fetchDockerStatus, 3000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    filterContainers();
  }, [containers, selectedCampaign]);

  const fetchMyCampaigns = async () => {
    try {
      const campaigns = await api.getUserCampaigns(userId);
      setMyCampaigns(campaigns);
    } catch (err) {
      console.error('Error fetching campaigns:', err);
    }
  };

  const fetchDockerStatus = async () => {
    try {
      const data = await api.getDockerStatus();
      setContainers(data.containers || []);
      setStats({
        total: data.total || 0,
        running: data.running || 0
      });
      setIsLoading(false);
      setError(null);
    } catch (err) {
      console.error('Error fetching docker status:', err);
      setError(err.message);
      setIsLoading(false);
    }
  };

  const filterContainers = async () => {
    if (selectedCampaign === 'all') {
      setFilteredContainers(containers);
    } else {
      try {
        const data = await api.getCampaignContainers(selectedCampaign);
        setFilteredContainers(data.containers || []);
      } catch (err) {
        console.error('Error filtering containers:', err);
        setFilteredContainers([]);
      }
    }
  };

  const handleBulkAction = async (actionFunc, actionName) => {
    try {
      setActionLoading(prev => ({ ...prev, [actionName]: true }));
      setError(null);
      setSuccess(null);

      const result = await actionFunc();
      setSuccess(result.message || `${actionName} completed successfully`);
      
      setTimeout(() => {
        fetchDockerStatus();
        setActionLoading(prev => ({ ...prev, [actionName]: false }));
        setSuccess(null);
      }, 2000);
    } catch (err) {
      setError(err.message);
      setActionLoading(prev => ({ ...prev, [actionName]: false }));
    }
  };

  const handleContainerAction = async (containerId, actionFunc, actionName) => {
    const key = `${actionName}-${containerId}`;
    try {
      setActionLoading(prev => ({ ...prev, [key]: true }));
      setError(null);
      setSuccess(null);

      const result = await actionFunc(containerId);
      setSuccess(`${actionName} completed successfully`);
      
      setTimeout(() => {
        fetchDockerStatus();
        setActionLoading(prev => ({ ...prev, [key]: false }));
        setSuccess(null);
      }, 1500);
    } catch (err) {
      setError(`Failed to ${actionName.toLowerCase()}: ${err.message}`);
      setActionLoading(prev => ({ ...prev, [key]: false }));
    }
  };

  const handleViewLogs = async (containerId, containerName) => {
    try {
      setError(null);
      const logs = await api.getContainerLogs(containerId);
      setContainerLogs({ 
        containerId, 
        containerName,
        logs: logs.logs || 'No logs available' 
      });
    } catch (err) {
      setError(`Failed to fetch logs: ${err.message}`);
    }
  };

  const BulkActionButton = ({ icon: Icon, label, onClick, color }) => (
    <button
      onClick={onClick}
      disabled={actionLoading[label]}
      className="flex-1 p-4 rounded-xl border transition-all duration-300 hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed group"
      style={{
        backgroundColor: `${color}10`,
        borderColor: `${color}40`,
      }}
    >
      <div className="flex flex-col items-center gap-2">
        {actionLoading[label] ? (
          <Loader className="w-6 h-6 animate-spin" style={{ color }} />
        ) : (
          <Icon className="w-6 h-6 group-hover:scale-110 transition-transform" style={{ color }} />
        )}
        <span className="text-sm font-semibold text-white">{label}</span>
      </div>
    </button>
  );

  const ContainerCard = ({ container }) => {
    const isRunning = container.State === 'running';
    const containerId = container.Id || container.ID || '';
    const containerName = container.Names?.[0]?.replace('/', '') || container.Name || 'Unknown';
    
    const startKey = `Start-${containerId}`;
    const stopKey = `Stop-${containerId}`;
    const restartKey = `Restart-${containerId}`;
    const removeKey = `Remove-${containerId}`;
    
    return (
      <div className="p-5 rounded-xl bg-black/30 border border-gray-800 hover:border-orange-500/50 transition-all duration-300">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3 flex-1">
            <div className={`w-3 h-3 rounded-full ${isRunning ? 'bg-green-500 animate-pulse' : 'bg-gray-600'}`} />
            <div className="flex-1">
              <h4 className="text-white font-semibold text-lg">{containerName}</h4>
              <p className="text-xs text-gray-500 font-mono">
                {containerId.substring(0, 12)}
              </p>
            </div>
          </div>
          <div className={`px-3 py-1 rounded-lg text-xs font-semibold ${
            isRunning 
              ? 'bg-green-950/30 text-green-400 border border-green-500/30' 
              : 'bg-gray-900 text-gray-500 border border-gray-700'
          }`}>
            {container.State || 'unknown'}
          </div>
        </div>

        {/* Container Info */}
        <div className="mb-4 p-3 rounded-lg bg-gray-900/50">
          <p className="text-xs text-gray-400">
            <span className="text-gray-500 font-semibold">Image:</span>
          </p>
          <p className="text-xs text-white font-mono truncate mt-1">
            {container.Image || 'N/A'}
          </p>
        </div>

        {/* Action Buttons */}
        <div className="space-y-2">
          <div className="grid grid-cols-2 gap-2">
            {/* Start Button */}
            <button
              onClick={() => handleContainerAction(containerId, api.startContainer, 'Start')}
              disabled={isRunning || actionLoading[startKey]}
              className="p-3 rounded-lg bg-green-500/20 hover:bg-green-500/30 disabled:opacity-50 disabled:cursor-not-allowed border border-green-500/40 transition-all group"
            >
              <div className="flex items-center justify-center gap-2">
                {actionLoading[startKey] ? (
                  <Loader className="w-4 h-4 text-green-500 animate-spin" />
                ) : (
                  <Play className="w-4 h-4 text-green-500 group-hover:scale-110 transition-transform" />
                )}
                <span className="text-sm font-semibold text-green-500">Start</span>
              </div>
            </button>
            
            {/* Stop Button */}
            <button
              onClick={() => handleContainerAction(containerId, api.stopContainer, 'Stop')}
              disabled={!isRunning || actionLoading[stopKey]}
              className="p-3 rounded-lg bg-orange-500/20 hover:bg-orange-500/30 disabled:opacity-50 disabled:cursor-not-allowed border border-orange-500/40 transition-all group"
            >
              <div className="flex items-center justify-center gap-2">
                {actionLoading[stopKey] ? (
                  <Loader className="w-4 h-4 text-orange-500 animate-spin" />
                ) : (
                  <Square className="w-4 h-4 text-orange-500 group-hover:scale-110 transition-transform" />
                )}
                <span className="text-sm font-semibold text-orange-500">Stop</span>
              </div>
            </button>
          </div>

          <div className="grid grid-cols-2 gap-2">
            {/* Restart Button */}
            <button
              onClick={() => handleContainerAction(containerId, api.restartContainer, 'Restart')}
              disabled={!isRunning || actionLoading[restartKey]}
              className="p-3 rounded-lg bg-blue-500/20 hover:bg-blue-500/30 disabled:opacity-50 disabled:cursor-not-allowed border border-blue-500/40 transition-all group"
            >
              <div className="flex items-center justify-center gap-2">
                {actionLoading[restartKey] ? (
                  <Loader className="w-4 h-4 text-blue-500 animate-spin" />
                ) : (
                  <RefreshCw className="w-4 h-4 text-blue-500 group-hover:scale-110 transition-transform" />
                )}
                <span className="text-sm font-semibold text-blue-500">Restart</span>
              </div>
            </button>
            
            {/* Logs Button */}
            <button
              onClick={() => handleViewLogs(containerId, containerName)}
              className="p-3 rounded-lg bg-purple-500/20 hover:bg-purple-500/30 border border-purple-500/40 transition-all group"
            >
              <div className="flex items-center justify-center gap-2">
                <FileText className="w-4 h-4 text-purple-500 group-hover:scale-110 transition-transform" />
                <span className="text-sm font-semibold text-purple-500">Logs</span>
              </div>
            </button>
          </div>

          {/* Remove Button - Separate and More Dangerous */}
          <button
            onClick={() => {
              if (window.confirm(`⚠️ Remove container "${containerName}"? This cannot be undone!`)) {
                handleContainerAction(containerId, api.removeContainer, 'Remove');
              }
            }}
            disabled={actionLoading[removeKey]}
            className="w-full p-3 rounded-lg bg-red-500/20 hover:bg-red-500/30 disabled:opacity-50 border border-red-500/40 transition-all group"
          >
            <div className="flex items-center justify-center gap-2">
              {actionLoading[removeKey] ? (
                <Loader className="w-4 h-4 text-red-500 animate-spin" />
              ) : (
                <Trash2 className="w-4 h-4 text-red-500 group-hover:scale-110 transition-transform" />
              )}
              <span className="text-sm font-semibold text-red-500">Remove Container</span>
            </div>
          </button>
        </div>
      </div>
    );
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-center">
          <Loader className="w-12 h-12 text-orange-500 animate-spin mx-auto mb-4" />
          <p className="text-gray-400">Loading Docker status...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-white via-blue-500 to-blue-600 bg-clip-text text-transparent">
            Docker Control Panel
          </h1>
          <p className="text-gray-400">Manage your container infrastructure</p>
        </div>

        {/* Campaign Filter - NEW */}
        <div className="mb-6 rounded-2xl border border-gray-900 bg-gradient-to-br from-gray-900/50 to-black/50 backdrop-blur p-6">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <Filter className="w-5 h-5 text-blue-500" />
              <span className="text-sm font-semibold text-gray-400">Filter by Campaign:</span>
            </div>
            <select
              value={selectedCampaign}
              onChange={(e) => setSelectedCampaign(e.target.value)}
              className="flex-1 max-w-md px-4 py-2 bg-black/50 border border-gray-800 rounded-lg text-white focus:outline-none focus:border-orange-500 transition-colors"
            >
              <option value="all">All Containers</option>
              {myCampaigns.map((campaign) => (
                <option key={campaign.campaign_id} value={campaign.campaign_id}>
                  {campaign.campaign_name || 'Unnamed Campaign'} ({campaign.machine_count} machines)
                </option>
              ))}
            </select>
            <div className="text-sm text-gray-400">
              Showing: <span className="text-white font-semibold">{filteredContainers.length}</span> containers
            </div>
          </div>
        </div>

        {/* Status Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="rounded-2xl border border-gray-900 bg-gradient-to-br from-gray-900/50 to-black/50 backdrop-blur p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-white">Status Overview</h3>
              <Activity className="w-5 h-5 text-blue-500" />
            </div>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Total Containers</span>
                <span className="text-2xl font-bold text-white">{stats.total}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Running</span>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                  <span className="text-2xl font-bold text-green-500">{stats.running}</span>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Stopped</span>
                <span className="text-2xl font-bold text-gray-500">{stats.total - stats.running}</span>
              </div>
            </div>
          </div>

          {/* Bulk Action Controls */}
          <div className="rounded-2xl border border-gray-900 bg-gradient-to-br from-gray-900/50 to-black/50 backdrop-blur p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-white">Bulk Actions</h3>
              <Terminal className="w-5 h-5 text-blue-500" />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <BulkActionButton
                icon={Play}
                label="Start All"
                color="#10b981"
                onClick={() => handleBulkAction(() => api.startContainers(), 'Start All')}
              />
              <BulkActionButton
                icon={Square}
                label="Stop All"
                color="#f97316"
                onClick={() => handleBulkAction(() => api.stopContainers(), 'Stop All')}
              />
              <BulkActionButton
                icon={RefreshCw}
                label="Restart All"
                color="#3b82f6"
                onClick={() => handleBulkAction(() => api.restartContainers(), 'Restart All')}
              />
              <BulkActionButton
                icon={Trash2}
                label="Destroy All"
                color="#ef4444"
                onClick={() => {
                  if (window.confirm('⚠️ This will permanently delete all containers. Are you sure?')) {
                    handleBulkAction(() => api.destroyContainers(), 'Destroy All');
                  }
                }}
              />
            </div>
          </div>
        </div>

        {/* Messages */}
        {error && (
          <div className="mb-6 p-4 rounded-xl bg-red-950/20 border border-red-500/50 flex items-center gap-3 animate-pulse">
            <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0" />
            <p className="text-red-400 flex-1">{error}</p>
            <button 
              onClick={() => setError(null)} 
              className="text-red-400 hover:text-red-300 text-xl font-bold"
            >
              ×
            </button>
          </div>
        )}

        {success && (
          <div className="mb-6 p-4 rounded-xl bg-green-950/20 border border-green-500/50 flex items-center gap-3 animate-pulse">
            <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
            <p className="text-green-400">{success}</p>
          </div>
        )}

        {/* Container Logs Modal */}
        {containerLogs && (
          <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-6">
            <div className="bg-gray-900 rounded-2xl border border-gray-800 max-w-4xl w-full max-h-[80vh] overflow-hidden">
              <div className="p-6 border-b border-gray-800 flex items-center justify-between">
                <div>
                  <h3 className="text-xl font-bold text-white">Container Logs</h3>
                  <p className="text-sm text-gray-400">{containerLogs.containerName}</p>
                </div>
                <button 
                  onClick={() => setContainerLogs(null)}
                  className="text-gray-400 hover:text-white text-2xl font-bold"
                >
                  ×
                </button>
              </div>
              <div className="p-6 overflow-auto max-h-[calc(80vh-100px)]">
                <pre className="text-xs text-green-400 font-mono bg-black/50 p-4 rounded-lg overflow-x-auto whitespace-pre-wrap">
                  {containerLogs.logs}
                </pre>
              </div>
            </div>
          </div>
        )}

        {/* Containers List */}
        <div className="rounded-2xl border border-gray-900 bg-gradient-to-br from-gray-900/50 to-black/50 backdrop-blur p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <Server className="w-5 h-5 text-blue-500" />
              Containers ({filteredContainers.length})
            </h3>
            <button
              onClick={fetchDockerStatus}
              disabled={Object.keys(actionLoading).length > 0}
              className="p-2 rounded-lg bg-blue-500/20 hover:bg-blue-500/30 text-blue-400 transition-colors disabled:opacity-50"
            >
              <RefreshCw className={`w-4 h-4 ${Object.keys(actionLoading).length > 0 ? 'animate-spin' : ''}`} />
            </button>
          </div>

          {filteredContainers.length === 0 ? (
            <div className="text-center py-12">
              <Server className="w-16 h-16 text-gray-700 mx-auto mb-4" />
              <h4 className="text-xl font-bold text-gray-600 mb-2">No Containers Found</h4>
              <p className="text-gray-500 mb-6">
                {selectedCampaign === 'all' 
                  ? 'Create a campaign to generate containers'
                  : 'This campaign has no running containers'}
              </p>
              <button
                onClick={() => window.location.href = '/campaigns'}
                className="px-6 py-3 bg-orange-500 hover:bg-orange-600 text-white rounded-lg transition-colors"
              >
                Go to Campaigns
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {filteredContainers.map((container, index) => (
                <ContainerCard key={container.Id || index} container={container} />
              ))}
            </div>
          )}
        </div>

        {/* Info Panel */}
        <div className="mt-6 p-4 rounded-xl bg-blue-950/20 border border-blue-500/30">
          <h4 className="text-sm font-semibold text-blue-400 mb-2 flex items-center gap-2">
            <Activity className="w-4 h-4" />
            Docker Management Guide
          </h4>
          <ul className="space-y-1 text-sm text-gray-400">
            <li>• <span className="text-green-400">Start</span>: Launch individual container</li>
            <li>• <span className="text-orange-400">Stop</span>: Stop individual container (preserves data)</li>
            <li>• <span className="text-blue-400">Restart</span>: Restart individual container</li>
            <li>• <span className="text-purple-400">Logs</span>: View container logs and output</li>
            <li>• <span className="text-red-400">Remove</span>: Permanently delete container</li>
            <li>• Use bulk actions to control all containers simultaneously</li>
            <li>• Filter by campaign to manage specific training sessions</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default DockerControl;
