// src/services/api.js - Enhanced API Service
const API_BASE_URL = 'http://localhost:8000';

class APIService {
  // Helper method for API calls
  async request(endpoint, options = {}) {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'API request failed' }));
        throw new Error(error.detail || 'API request failed');
      }

      return await response.json();
    } catch (error) {
      console.error(`API Error (${endpoint}):`, error);
      throw error;
    }
  }

  // Stats & Dashboard
  async getStats() {
    return this.request('/api/stats');
  }

  async getPlatformStats() {
    return this.request('/api/statistics');
  }

  // Blueprints
  async getBlueprints() {
    return this.request('/api/blueprints');
  }

  async getBlueprint(blueprintId) {
    return this.request(`/api/blueprints/${blueprintId}`);
  }

  // Campaigns - ENHANCED
  async createCampaign(userId, campaignName, difficulty, count = null) {
    return this.request('/api/campaigns', {
      method: 'POST',
      body: JSON.stringify({
        user_id: userId,
        campaign_name: campaignName,
        difficulty: difficulty,
        count: count
      }),
    });
  }

  // NEW: Get user's campaigns
  async getUserCampaigns(userId) {
    return this.request(`/api/users/${userId}/campaigns`);
  }

  // NEW: Get specific campaign details
  async getCampaign(campaignId) {
    return this.request(`/api/campaigns/${campaignId}`);
  }

  // NEW: Get machines for a campaign
  async getCampaignMachines(campaignId) {
    return this.request(`/api/campaigns/${campaignId}/machines`);
  }

  async getCampaignProgress(campaignId, userId) {
    return this.request(`/api/campaigns/${campaignId}/progress?user_id=${userId}`);
  }

  // Machines
  async getMachines() {
    return this.request('/api/machines');
  }

  async getMachine(machineId) {
    return this.request(`/api/machines/${machineId}`);
  }

  async getMachineStats(machineId) {
    return this.request(`/api/machines/${machineId}/stats`);
  }

  // Flags
  async validateFlag(machineId, flag, userId) {
    return this.request('/api/flags/validate', {
      method: 'POST',
      body: JSON.stringify({
        machine_id: machineId,
        flag: flag,
        user_id: userId
      }),
    });
  }

  // Docker Management - ALL CONTAINERS
  async startContainers() {
    return this.request('/api/docker/start', {
      method: 'POST',
    });
  }

  async stopContainers() {
    return this.request('/api/docker/stop', {
      method: 'POST',
    });
  }

  async restartContainers() {
    return this.request('/api/docker/restart', {
      method: 'POST',
    });
  }

  async destroyContainers() {
    return this.request('/api/docker/destroy', {
      method: 'DELETE',
    });
  }

  async getDockerStatus() {
    return this.request('/api/docker/status');
  }

  // NEW: Get containers by campaign
  async getCampaignContainers(campaignId) {
    return this.request(`/api/docker/campaign/${campaignId}/containers`);
  }

  // Docker Management - INDIVIDUAL CONTAINERS
  async startContainer(containerId) {
    console.log('Starting container:', containerId);
    return this.request(`/api/docker/container/${containerId}/start`, {
      method: 'POST',
    });
  }

  async stopContainer(containerId) {
    console.log('Stopping container:', containerId);
    return this.request(`/api/docker/container/${containerId}/stop`, {
      method: 'POST',
    });
  }

  async restartContainer(containerId) {
    console.log('Restarting container:', containerId);
    return this.request(`/api/docker/container/${containerId}/restart`, {
      method: 'POST',
    });
  }

  async removeContainer(containerId) {
    console.log('Removing container:', containerId);
    return this.request(`/api/docker/container/${containerId}`, {
      method: 'DELETE',
    });
  }

  async getContainerLogs(containerId, tail = 100) {
    console.log('Getting logs for container:', containerId);
    return this.request(`/api/docker/container/${containerId}/logs?tail=${tail}`);
  }

  // Users
  async createUser(username, email, role = 'student') {
    return this.request('/api/users', {
      method: 'POST',
      body: JSON.stringify({
        username: username,
        email: email,
        role: role
      }),
    });
  }

  async getUser(userId) {
    return this.request(`/api/users/${userId}`);
  }

  async getUserProgress(userId) {
    return this.request(`/api/users/${userId}/progress`);
  }

  // Leaderboard
  async getLeaderboard(limit = 100, timeframe = 'all_time') {
    return this.request(`/api/leaderboard?limit=${limit}&timeframe=${timeframe}`);
  }

  // Config Management
  async getConfigs() {
    return this.request('/api/configs');
  }

  async getConfig(category) {
    return this.request(`/api/configs/${category}`);
  }

  async createConfig(configData) {
    return this.request('/api/configs', {
      method: 'POST',
      body: JSON.stringify(configData),
    });
  }

  async updateConfig(category, configData) {
    return this.request(`/api/configs/${category}`, {
      method: 'PUT',
      body: JSON.stringify(configData),
    });
  }

  async deleteConfig(category) {
    return this.request(`/api/configs/${category}`, {
      method: 'DELETE',
    });
  }

  async generateFromConfig(category) {
    return this.request(`/api/configs/${category}/generate`, {
      method: 'POST',
    });
  }

  async generateAllConfigs() {
    return this.request('/api/configs/generate-all', {
      method: 'POST',
    });
  }

  async createConfigWithMachine(configData) {
    return this.request('/api/configs?auto_generate=true', {
      method: 'POST',
      body: JSON.stringify(configData),
    });
  }

  // NEW: Generate complete machine from existing config (full pipeline)
  async generateMachineFromConfig(category) {
    return this.request(`/api/configs/${category}/generate-machine`, {
      method: 'POST',
    });
  }

  // EXISTING: Just generate blueprint (no machine)
  async generateFromConfig(category) {
    return this.request(`/api/configs/${category}/generate`, {
      method: 'POST',
    });
  }

  // Health Check
  async healthCheck() {
    return this.request('/health');
  }
}

// Export as default (singleton pattern)
const apiService = new APIService();
export default apiService;
