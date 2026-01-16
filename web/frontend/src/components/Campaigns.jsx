import React, { useState, useEffect } from 'react';
import { Zap, Plus, Target, AlertCircle, CheckCircle, Loader, ChevronRight, Shield, List, Eye } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const Campaigns = () => {
  const navigate = useNavigate();
  const [userId] = useState('user_default');
  const [isCreating, setIsCreating] = useState(false);
  const [difficulty, setDifficulty] = useState(2);
  const [machineCount, setMachineCount] = useState(5);
  const [campaignName, setCampaignName] = useState(''); // NEW
  const [createdCampaign, setCreatedCampaign] = useState(null);
  const [error, setError] = useState(null);
  
  // NEW: Campaign list
  const [myCampaigns, setMyCampaigns] = useState([]);
  const [loadingCampaigns, setLoadingCampaigns] = useState(true);

  useEffect(() => {
    fetchMyCampaigns();
  }, []);

  const fetchMyCampaigns = async () => {
    try {
      setLoadingCampaigns(true);
      const campaigns = await api.getUserCampaigns(userId);
      setMyCampaigns(campaigns);
      setLoadingCampaigns(false);
    } catch (err) {
      console.error('Error fetching campaigns:', err);
      setLoadingCampaigns(false);
    }
  };

  const handleCreateCampaign = async () => {
    if (!campaignName.trim()) {
      setError('Please enter a campaign name');
      return;
    }

    try {
      setIsCreating(true);
      setError(null);
      
      const campaign = await api.createCampaign(userId, campaignName, difficulty, machineCount);
      setCreatedCampaign(campaign);
      setIsCreating(false);
      
      // Refresh campaigns list
      fetchMyCampaigns();
      
      // Reset form
      setCampaignName('');
    } catch (err) {
      setError(err.message);
      setIsCreating(false);
    }
  };

  const getDifficultyColor = (level) => {
    const colors = {
      1: '#10b981',
      2: '#3b82f6',
      3: '#f59e0b',
      4: '#f97316',
      5: '#ef4444'
    };
    return colors[level] || '#ff7300';
  };

  const getDifficultyLabel = (level) => {
    const labels = {
      1: 'Beginner',
      2: 'Easy',
      3: 'Medium',
      4: 'Hard',
      5: 'Expert'
    };
    return labels[level] || 'Unknown';
  };

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-white via-orange-500 to-orange-600 bg-clip-text text-transparent">
            Campaign Manager
          </h1>
          <p className="text-gray-400">Create and manage your cybersecurity training campaigns</p>
        </div>

        {/* My Campaigns Section */}
        <div className="mb-8">
          <div className="rounded-2xl border border-gray-900 bg-gradient-to-br from-gray-900/50 to-black/50 backdrop-blur p-6">
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
              <div className="p-2 rounded-lg bg-blue-500/20">
                <List className="w-6 h-6 text-blue-500" />
              </div>
              My Campaigns
            </h2>

            {loadingCampaigns ? (
              <div className="text-center py-8">
                <Loader className="w-8 h-8 text-orange-500 animate-spin mx-auto mb-3" />
                <p className="text-gray-400 text-sm">Loading campaigns...</p>
              </div>
            ) : myCampaigns.length === 0 ? (
              <div className="text-center py-8">
                <Target className="w-16 h-16 text-gray-700 mx-auto mb-4 opacity-50" />
                <p className="text-gray-500">No campaigns yet. Create your first one below!</p>
              </div>
            ) : (
              <div className="space-y-3">
                {myCampaigns.map((campaign) => (
                  <div
                    key={campaign.campaign_id}
                    className="p-4 rounded-xl bg-black/30 border border-gray-800 hover:border-orange-500/50 transition-all duration-300 group cursor-pointer"
                    onClick={() => navigate(`/campaigns/${campaign.campaign_id}`)}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <h3 className="text-lg font-bold text-white group-hover:text-orange-500 transition-colors">
                            {campaign.campaign_name || 'Unnamed Campaign'}
                          </h3>
                          <div
                            className="px-2 py-1 rounded-lg text-xs font-semibold"
                            style={{
                              backgroundColor: `${getDifficultyColor(campaign.difficulty)}20`,
                              color: getDifficultyColor(campaign.difficulty)
                            }}
                          >
                            Level {campaign.difficulty}
                          </div>
                        </div>
                        
                        <div className="flex items-center gap-4 text-sm text-gray-400">
                          <span>{campaign.machine_count} machines</span>
                          <span>•</span>
                          <span>
                            {campaign.machines_solved || 0}/{campaign.machine_count} solved
                          </span>
                          <span>•</span>
                          <span>
                            {Math.round(campaign.progress_percentage || 0)}% complete
                          </span>
                        </div>

                        {/* Progress Bar */}
                        <div className="mt-3 h-2 bg-gray-900 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-gradient-to-r from-orange-500 to-orange-600 transition-all duration-500"
                            style={{ width: `${campaign.progress_percentage || 0}%` }}
                          />
                        </div>
                      </div>

                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          navigate(`/campaigns/${campaign.campaign_id}`);
                        }}
                        className="ml-4 p-3 rounded-lg bg-orange-500/20 hover:bg-orange-500/30 border border-orange-500/40 transition-all group/btn"
                      >
                        <Eye className="w-5 h-5 text-orange-500 group-hover/btn:scale-110 transition-transform" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Create New Campaign Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Creation Form */}
          <div className="rounded-2xl border border-gray-900 bg-gradient-to-br from-gray-900/50 to-black/50 backdrop-blur p-8">
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
              <div className="p-2 rounded-lg bg-orange-500/20">
                <Plus className="w-6 h-6 text-orange-500" />
              </div>
              Create New Campaign
            </h2>

            {/* Campaign Name Input - NEW */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-400 mb-3">
                Campaign Name *
              </label>
              <input
                type="text"
                value={campaignName}
                onChange={(e) => setCampaignName(e.target.value)}
                placeholder="e.g., Web Security Training, SQL Injection Course"
                className="w-full px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white focus:outline-none focus:border-orange-500 transition-colors placeholder-gray-600"
              />
            </div>

            {/* Difficulty Selector */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-400 mb-3">
                Difficulty Level
              </label>
              <div className="grid grid-cols-5 gap-2">
                {[1, 2, 3, 4, 5].map((level) => (
                  <button
                    key={level}
                    onClick={() => setDifficulty(level)}
                    className={`p-3 rounded-xl border transition-all duration-300 ${
                      difficulty === level
                        ? 'border-orange-500 bg-orange-500/20 scale-105'
                        : 'border-gray-800 hover:border-gray-700'
                    }`}
                    style={{
                      borderColor: difficulty === level ? getDifficultyColor(level) : undefined,
                      backgroundColor: difficulty === level ? `${getDifficultyColor(level)}20` : undefined
                    }}
                  >
                    <div className="text-center">
                      <Shield 
                        className="w-6 h-6 mx-auto mb-1"
                        style={{ color: difficulty === level ? getDifficultyColor(level) : '#6b7280' }}
                      />
                      <div className="text-xs font-semibold" style={{ color: difficulty === level ? getDifficultyColor(level) : '#9ca3af' }}>
                        {level}
                      </div>
                    </div>
                  </button>
                ))}
              </div>
              <p className="mt-2 text-sm text-center" style={{ color: getDifficultyColor(difficulty) }}>
                {getDifficultyLabel(difficulty)}
              </p>
            </div>

            {/* Machine Count */}
            <div className="mb-8">
              <label className="block text-sm font-medium text-gray-400 mb-3">
                Number of Machines
              </label>
              <div className="relative">
                <input
                  type="number"
                  min="1"
                  max="10"
                  value={machineCount}
                  onChange={(e) => setMachineCount(parseInt(e.target.value) || 1)}
                  className="w-full px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white focus:outline-none focus:border-orange-500 transition-colors"
                />
                <div className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500 text-sm">
                  machines
                </div>
              </div>
            </div>

            {/* Error Display */}
            {error && (
              <div className="mb-6 p-4 rounded-xl bg-red-950/20 border border-red-500/50 flex items-center gap-3">
                <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0" />
                <p className="text-red-400 text-sm">{error}</p>
              </div>
            )}

            {/* Create Button */}
            <button
              onClick={handleCreateCampaign}
              disabled={isCreating}
              className="w-full py-4 bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 disabled:from-gray-700 disabled:to-gray-800 text-white font-semibold rounded-xl transition-all duration-300 flex items-center justify-center gap-3 group"
            >
              {isCreating ? (
                <>
                  <Loader className="w-5 h-5 animate-spin" />
                  Creating Campaign...
                </>
              ) : (
                <>
                  <Zap className="w-5 h-5 group-hover:scale-110 transition-transform" />
                  Generate Campaign
                </>
              )}
            </button>
          </div>

          {/* Campaign Result */}
          <div className="rounded-2xl border border-gray-900 bg-gradient-to-br from-gray-900/50 to-black/50 backdrop-blur p-8">
            {createdCampaign ? (
              <div className="space-y-6">
                {/* Success Header */}
                <div className="flex items-center gap-3 p-4 rounded-xl bg-green-950/20 border border-green-500/50">
                  <CheckCircle className="w-6 h-6 text-green-500 flex-shrink-0" />
                  <div>
                    <h3 className="text-lg font-bold text-green-400">Campaign Created!</h3>
                    <p className="text-sm text-gray-400">{createdCampaign.campaign_name}</p>
                  </div>
                </div>

                {/* Campaign Info */}
                <div className="space-y-3">
                  <div className="flex justify-between items-center p-3 rounded-lg bg-black/30">
                    <span className="text-gray-400">Campaign ID</span>
                    <code className="text-orange-500 font-mono text-sm">{createdCampaign.campaign_id}</code>
                  </div>
                  <div className="flex justify-between items-center p-3 rounded-lg bg-black/30">
                    <span className="text-gray-400">Difficulty</span>
                    <span className="font-semibold" style={{ color: getDifficultyColor(createdCampaign.difficulty) }}>
                      Level {createdCampaign.difficulty}
                    </span>
                  </div>
                  <div className="flex justify-between items-center p-3 rounded-lg bg-black/30">
                    <span className="text-gray-400">Machines</span>
                    <span className="text-white font-semibold">{createdCampaign.machines.length}</span>
                  </div>
                </div>

                {/* Machines List */}
                <div>
                  <h4 className="text-sm font-semibold text-gray-400 mb-3">Your Machines</h4>
                  <div className="space-y-2 max-h-64 overflow-y-auto">
                    {createdCampaign.machines.map((machine, index) => (
                      <div
                        key={machine.machine_id}
                        className="p-4 rounded-xl bg-black/30 border border-gray-800 hover:border-orange-500/50 transition-all duration-300 group"
                      >
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center gap-3">
                            <div 
                              className="w-8 h-8 rounded-lg flex items-center justify-center text-white font-bold text-sm"
                              style={{ backgroundColor: getDifficultyColor(machine.difficulty) }}
                            >
                              {index + 1}
                            </div>
                            <div>
                              <h5 className="text-white font-semibold">{machine.variant}</h5>
                              <p className="text-xs text-gray-500">Level {machine.difficulty}</p>
                            </div>
                          </div>
                          <Target className="w-5 h-5 text-gray-600 group-hover:text-orange-500 transition-colors" />
                        </div>
                        
                        {machine.port && (
                          <div className="mt-2 p-2 rounded-lg bg-gray-900/50 border border-gray-800">
                            <p className="text-xs text-gray-500 mb-1">Access URL</p>
                            <code className="text-orange-500 text-sm">
                              http://localhost:{machine.port}
                            </code>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>

                {/* Action Button */}
                <button
                  onClick={() => navigate(`/campaigns/${createdCampaign.campaign_id}`)}
                  className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl transition-all duration-300 flex items-center justify-center gap-2 group"
                >
                  View Campaign Details
                  <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </button>
              </div>
            ) : (
              <div className="h-full flex items-center justify-center">
                <div className="text-center text-gray-600">
                  <Target className="w-16 h-16 mx-auto mb-4 opacity-20" />
                  <p>Configure and create a campaign to see results here</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Campaigns;
