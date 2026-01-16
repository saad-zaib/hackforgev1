// web/frontend/src/components/ConfigManager.jsx
// FIXED: All fields added, using SAME API as original
import React, { useState, useEffect } from 'react';
import {
  Settings, Plus, RefreshCw, Trash2, Loader,
  CheckCircle, AlertCircle, FileCode, Hammer,
  ChevronRight, X, Sparkles, Code, Zap, Rocket,
  ChevronDown, ChevronUp
} from 'lucide-react';
import api from '../services/api';

const ConfigManager = () => {
  const [configs, setConfigs] = useState([]);
  const [selectedConfig, setSelectedConfig] = useState(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);
  const [generatingMachine, setGeneratingMachine] = useState(null);
  const [expandedSections, setExpandedSections] = useState({
    basic: true,
    mutation: false,
    variants: false
  });

  // Complete form state - ALL FIELDS FROM JSON
  const [newConfig, setNewConfig] = useState({
    vulnerability_id: '',
    name: '',
    category: '',
    difficulty_range: [1, 5],
    description: '',
    variants: [''],
    entry_points: [''],
    mutation_axes: {
      filters: {
        basic: [''],
        medium: [''],
        advanced: ['']
      },
      contexts: [''],
      sinks: [''],
      encoding: [''],
      output_contexts: ['']
    },
    variant_configs: []
  });

  useEffect(() => {
    loadConfigs();
  }, []);

  const loadConfigs = async () => {
    try {
      setLoading(true);
      const data = await api.getConfigs();
      setConfigs(data);
    } catch (error) {
      showMessage('Failed to load configs: ' + error.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  const showMessage = (text, type = 'info') => {
    setMessage({ text, type });
    setTimeout(() => setMessage(null), 8000);
  };

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const handleCreateConfig = async (e, autoGenerate = true) => {
    e.preventDefault();

    try {
      setLoading(true);

      // Clean up empty strings from arrays
      const cleanConfig = {
        ...newConfig,
        variants: newConfig.variants.filter(v => v.trim()),
        entry_points: newConfig.entry_points.filter(ep => ep.trim()),
        mutation_axes: {
          filters: {
            basic: newConfig.mutation_axes.filters.basic.filter(f => f.trim()),
            medium: newConfig.mutation_axes.filters.medium.filter(f => f.trim()),
            advanced: newConfig.mutation_axes.filters.advanced.filter(f => f.trim())
          },
          contexts: newConfig.mutation_axes.contexts.filter(c => c.trim()),
          sinks: newConfig.mutation_axes.sinks.filter(s => s.trim()),
          encoding: newConfig.mutation_axes.encoding.filter(e => e.trim()),
          output_contexts: newConfig.mutation_axes.output_contexts.filter(oc => oc.trim())
        },
        variant_configs: newConfig.variant_configs
      };

      let result;
      if (autoGenerate) {
        // Use the SAME API method as original
        result = await api.createConfigWithMachine(cleanConfig);

        if (result.auto_generated && result.machine) {
          showMessage(
            `🎉 Config created and machine generated! Machine ID: ${result.machine.machine_id}. Ready at: ${result.machine.url || 'Building...'}`,
            'success'
          );
        } else {
          showMessage('Config created! Machine generation in progress...', 'success');
        }
      } else {
        // Original: Just create config
        result = await api.createConfig(cleanConfig);
        showMessage('Config created successfully!', 'success');
      }

      setShowCreateForm(false);
      loadConfigs();

      // Reset form
      setNewConfig({
        vulnerability_id: '',
        name: '',
        category: '',
        difficulty_range: [1, 5],
        description: '',
        variants: [''],
        entry_points: [''],
        mutation_axes: {
          filters: { basic: [''], medium: [''], advanced: [''] },
          contexts: [''],
          sinks: [''],
          encoding: [''],
          output_contexts: ['']
        },
        variant_configs: []
      });

    } catch (error) {
      showMessage('Failed to create config: ' + error.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateMachine = async (category) => {
    try {
      setGeneratingMachine(category);
      showMessage(`🚀 Generating complete machine from ${category}...`, 'info');

      // SAME API as original
      const result = await api.generateMachineFromConfig(category);

      showMessage(
        `🎉 Machine ready! ID: ${result.machine_id} at ${result.url || 'http://localhost:8080'}`,
        'success'
      );

      setTimeout(() => loadConfigs(), 2000);

    } catch (error) {
      showMessage('Failed to generate machine: ' + error.message, 'error');
    } finally {
      setGeneratingMachine(null);
    }
  };

  const handleGenerateBlueprint = async (category) => {
    try {
      setLoading(true);
      await api.generateFromConfig(category);
      showMessage(`Blueprint generated from ${category} config!`, 'success');
    } catch (error) {
      showMessage('Failed to generate blueprint: ' + error.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateAll = async () => {
    try {
      setLoading(true);
      const result = await api.generateAllConfigs();
      showMessage(`Generated ${result.generated?.length || 0} blueprints!`, 'success');

      if (result.failed && result.failed.length > 0) {
        console.error('Failed configs:', result.failed);
      }
    } catch (error) {
      showMessage('Failed to generate blueprints: ' + error.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteConfig = async (category) => {
    if (!window.confirm(`Delete config: ${category}?`)) return;

    try {
      setLoading(true);
      await api.deleteConfig(category);
      showMessage('Config deleted successfully', 'success');
      loadConfigs();
    } catch (error) {
      showMessage('Failed to delete config: ' + error.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  // Array manipulation helpers
  const addArrayItem = (path, value = '') => {
    setNewConfig(prev => {
      const newState = JSON.parse(JSON.stringify(prev));
      const parts = path.split('.');
      let current = newState;

      for (let i = 0; i < parts.length - 1; i++) {
        current = current[parts[i]];
      }

      const lastKey = parts[parts.length - 1];
      current[lastKey] = [...current[lastKey], value];

      return newState;
    });
  };

  const updateArrayItem = (path, index, value) => {
    setNewConfig(prev => {
      const newState = JSON.parse(JSON.stringify(prev));
      const parts = path.split('.');
      let current = newState;

      for (let i = 0; i < parts.length - 1; i++) {
        current = current[parts[i]];
      }

      const lastKey = parts[parts.length - 1];
      current[lastKey][index] = value;

      return newState;
    });
  };

  const removeArrayItem = (path, index) => {
    setNewConfig(prev => {
      const newState = JSON.parse(JSON.stringify(prev));
      const parts = path.split('.');
      let current = newState;

      for (let i = 0; i < parts.length - 1; i++) {
        current = current[parts[i]];
      }

      const lastKey = parts[parts.length - 1];
      current[lastKey] = current[lastKey].filter((_, i) => i !== index);

      return newState;
    });
  };

  // Variant config helpers
  const addVariantConfig = () => {
    setNewConfig(prev => ({
      ...prev,
      variant_configs: [
        ...prev.variant_configs,
        {
          name: '',
          parameters: []
        }
      ]
    }));
  };

  const updateVariantConfig = (index, field, value) => {
    setNewConfig(prev => {
      const newConfigs = [...prev.variant_configs];
      newConfigs[index] = { ...newConfigs[index], [field]: value };
      return { ...prev, variant_configs: newConfigs };
    });
  };

  const removeVariantConfig = (index) => {
    setNewConfig(prev => ({
      ...prev,
      variant_configs: prev.variant_configs.filter((_, i) => i !== index)
    }));
  };

  const addVariantParameter = (variantIndex) => {
    setNewConfig(prev => {
      const newConfigs = [...prev.variant_configs];
      newConfigs[variantIndex].parameters = [
        ...newConfigs[variantIndex].parameters,
        { name: '', axis: '', default: '' }
      ];
      return { ...prev, variant_configs: newConfigs };
    });
  };

  const updateVariantParameter = (variantIndex, paramIndex, field, value) => {
    setNewConfig(prev => {
      const newConfigs = [...prev.variant_configs];
      newConfigs[variantIndex].parameters[paramIndex][field] = value;
      return { ...prev, variant_configs: newConfigs };
    });
  };

  const removeVariantParameter = (variantIndex, paramIndex) => {
    setNewConfig(prev => {
      const newConfigs = [...prev.variant_configs];
      newConfigs[variantIndex].parameters = newConfigs[variantIndex].parameters.filter((_, i) => i !== paramIndex);
      return { ...prev, variant_configs: newConfigs };
    });
  };

  if (loading && configs.length === 0) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-center">
          <Loader className="w-12 h-12 text-orange-500 animate-spin mx-auto mb-4" />
          <p className="text-gray-400">Loading configs...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-white via-orange-500 to-orange-600 bg-clip-text text-transparent">
            Vulnerability Configs
          </h1>
          <p className="text-gray-400">Create configs and generate ready-to-use machines automatically</p>
        </div>

        {/* Message Toast */}
        {message && (
          <div
            className={`mb-6 p-4 rounded-2xl border flex items-center gap-3 ${
              message.type === 'error'
                ? 'bg-red-950/20 border-red-500/50'
                : message.type === 'success'
                ? 'bg-green-950/20 border-green-500/50'
                : 'bg-blue-950/20 border-blue-500/50'
            }`}
            style={{ animation: 'slideDown 0.3s ease-out' }}
          >
            {message.type === 'error' ? (
              <AlertCircle className="w-5 h-5 text-red-500" />
            ) : message.type === 'success' ? (
              <CheckCircle className="w-5 h-5 text-green-500" />
            ) : (
              <Loader className="w-5 h-5 text-blue-500 animate-spin" />
            )}
            <span className={
              message.type === 'error' ? 'text-red-400' :
              message.type === 'success' ? 'text-green-400' : 'text-blue-400'
            }>{message.text}</span>
          </div>
        )}

        {/* Action Buttons */}
        <div className="mb-8 flex flex-wrap gap-4">
          <button
            onClick={() => setShowCreateForm(!showCreateForm)}
            className="px-6 py-3 bg-orange-500 hover:bg-orange-600 text-white rounded-xl transition-all duration-300 flex items-center gap-2 hover:scale-105 active:scale-95"
          >
            {showCreateForm ? (
              <>
                <X className="w-5 h-5" />
                Cancel
              </>
            ) : (
              <>
                <Plus className="w-5 h-5" />
                Create New Config
              </>
            )}
          </button>

          <button
            onClick={handleGenerateAll}
            disabled={loading || configs.length === 0}
            className="px-6 py-3 bg-green-600 hover:bg-green-700 disabled:bg-gray-800 disabled:opacity-50 text-white rounded-xl transition-all duration-300 flex items-center gap-2 hover:scale-105 active:scale-95"
          >
            <Hammer className="w-5 h-5" />
            Generate All Blueprints
          </button>

          <button
            onClick={loadConfigs}
            disabled={loading}
            className="px-6 py-3 bg-gray-800 hover:bg-gray-700 text-white rounded-xl transition-all duration-300 flex items-center gap-2 hover:scale-105 active:scale-95"
          >
            <RefreshCw className={`w-5 h-5 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </button>
        </div>

        {/* CREATE FORM - ALL FIELDS */}
        {showCreateForm && (
          <div className="mb-8 rounded-2xl border border-gray-900 bg-gradient-to-br from-gray-900/50 to-black/50 backdrop-blur p-6"
            style={{ animation: 'slideUp 0.4s ease-out' }}
          >
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
              <FileCode className="w-6 h-6 text-orange-500" />
              Create New Config
            </h2>

            <form onSubmit={(e) => handleCreateConfig(e, true)} className="space-y-6">
              {/* SECTION 1: Basic Information */}
              <div className="border border-gray-800 rounded-xl p-6 bg-black/30">
                <button
                  type="button"
                  onClick={() => toggleSection('basic')}
                  className="w-full flex items-center justify-between mb-4"
                >
                  <h3 className="text-xl font-bold flex items-center gap-2">
                    <Code className="w-5 h-5 text-orange-500" />
                    Basic Information
                  </h3>
                  {expandedSections.basic ? (
                    <ChevronUp className="w-5 h-5 text-gray-400" />
                  ) : (
                    <ChevronDown className="w-5 h-5 text-gray-400" />
                  )}
                </button>

                {expandedSections.basic && (
                  <div className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-400 mb-2">
                          Vulnerability ID *
                        </label>
                        <input
                          type="text"
                          required
                          value={newConfig.vulnerability_id}
                          onChange={(e) => setNewConfig({...newConfig, vulnerability_id: e.target.value})}
                          className="w-full px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white focus:outline-none focus:border-orange-500 transition-colors"
                          placeholder="e.g., xss_001"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-400 mb-2">
                          Name *
                        </label>
                        <input
                          type="text"
                          required
                          value={newConfig.name}
                          onChange={(e) => setNewConfig({...newConfig, name: e.target.value})}
                          className="w-full px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white focus:outline-none focus:border-orange-500 transition-colors"
                          placeholder="e.g., Cross-Site Scripting"
                        />
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-400 mb-2">
                        Category *
                      </label>
                      <input
                        type="text"
                        required
                        value={newConfig.category}
                        onChange={(e) => setNewConfig({...newConfig, category: e.target.value})}
                        className="w-full px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white focus:outline-none focus:border-orange-500 transition-colors"
                        placeholder="e.g., cross_site_scripting"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-400 mb-2">
                        Difficulty Range (Min - Max)
                      </label>
                      <div className="grid grid-cols-2 gap-4">
                        <input
                          type="number"
                          min="1"
                          max="10"
                          value={newConfig.difficulty_range[0]}
                          onChange={(e) => setNewConfig({
                            ...newConfig,
                            difficulty_range: [parseInt(e.target.value), newConfig.difficulty_range[1]]
                          })}
                          className="w-full px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white focus:outline-none focus:border-orange-500 transition-colors"
                        />
                        <input
                          type="number"
                          min="1"
                          max="10"
                          value={newConfig.difficulty_range[1]}
                          onChange={(e) => setNewConfig({
                            ...newConfig,
                            difficulty_range: [newConfig.difficulty_range[0], parseInt(e.target.value)]
                          })}
                          className="w-full px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white focus:outline-none focus:border-orange-500 transition-colors"
                        />
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-400 mb-2">
                        Description *
                      </label>
                      <textarea
                        required
                        rows="4"
                        value={newConfig.description}
                        onChange={(e) => setNewConfig({...newConfig, description: e.target.value})}
                        className="w-full px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white focus:outline-none focus:border-orange-500 transition-colors resize-none"
                        placeholder="Describe the vulnerability..."
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-400 mb-2">
                        Variants
                      </label>
                      {newConfig.variants.map((variant, index) => (
                        <div key={index} className="flex gap-2 mb-2">
                          <input
                            type="text"
                            value={variant}
                            onChange={(e) => updateArrayItem('variants', index, e.target.value)}
                            className="flex-1 px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white focus:outline-none focus:border-orange-500 transition-colors"
                            placeholder="e.g., Reflected XSS"
                          />
                          <button
                            type="button"
                            onClick={() => removeArrayItem('variants', index)}
                            className="px-4 py-3 bg-red-600/20 hover:bg-red-600/30 text-red-400 rounded-xl transition-colors"
                          >
                            <X className="w-5 h-5" />
                          </button>
                        </div>
                      ))}
                      <button
                        type="button"
                        onClick={() => addArrayItem('variants')}
                        className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-xl transition-colors flex items-center gap-2"
                      >
                        <Plus className="w-4 h-4" />
                        Add Variant
                      </button>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-400 mb-2">
                        Entry Points
                      </label>
                      {newConfig.entry_points.map((ep, index) => (
                        <div key={index} className="flex gap-2 mb-2">
                          <input
                            type="text"
                            value={ep}
                            onChange={(e) => updateArrayItem('entry_points', index, e.target.value)}
                            className="flex-1 px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white focus:outline-none focus:border-orange-500 transition-colors"
                            placeholder="e.g., http_get_param"
                          />
                          <button
                            type="button"
                            onClick={() => removeArrayItem('entry_points', index)}
                            className="px-4 py-3 bg-red-600/20 hover:bg-red-600/30 text-red-400 rounded-xl transition-colors"
                          >
                            <X className="w-5 h-5" />
                          </button>
                        </div>
                      ))}
                      <button
                        type="button"
                        onClick={() => addArrayItem('entry_points')}
                        className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-xl transition-colors flex items-center gap-2"
                      >
                        <Plus className="w-4 h-4" />
                        Add Entry Point
                      </button>
                    </div>
                  </div>
                )}
              </div>

              {/* SECTION 2: Mutation Axes */}
              <div className="border border-gray-800 rounded-xl p-6 bg-black/30">
                <button
                  type="button"
                  onClick={() => toggleSection('mutation')}
                  className="w-full flex items-center justify-between mb-4"
                >
                  <h3 className="text-xl font-bold flex items-center gap-2">
                    <Zap className="w-5 h-5 text-orange-500" />
                    Mutation Axes
                  </h3>
                  {expandedSections.mutation ? (
                    <ChevronUp className="w-5 h-5 text-gray-400" />
                  ) : (
                    <ChevronDown className="w-5 h-5 text-gray-400" />
                  )}
                </button>

                {expandedSections.mutation && (
                  <div className="space-y-6">
                    {/* Filters - Basic */}
                    <div>
                      <label className="block text-sm font-medium text-orange-400 mb-2">
                        Filters - Basic
                      </label>
                      {newConfig.mutation_axes.filters.basic.map((filter, index) => (
                        <div key={index} className="flex gap-2 mb-2">
                          <input
                            type="text"
                            value={filter}
                            onChange={(e) => updateArrayItem('mutation_axes.filters.basic', index, e.target.value)}
                            className="flex-1 px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white focus:outline-none focus:border-orange-500 transition-colors"
                            placeholder="e.g., script_tag"
                          />
                          <button
                            type="button"
                            onClick={() => removeArrayItem('mutation_axes.filters.basic', index)}
                            className="px-4 py-3 bg-red-600/20 hover:bg-red-600/30 text-red-400 rounded-xl transition-colors"
                          >
                            <X className="w-5 h-5" />
                          </button>
                        </div>
                      ))}
                      <button
                        type="button"
                        onClick={() => addArrayItem('mutation_axes.filters.basic')}
                        className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-xl transition-colors flex items-center gap-2"
                      >
                        <Plus className="w-4 h-4" />
                        Add Basic Filter
                      </button>
                    </div>

                    {/* Filters - Medium */}
                    <div>
                      <label className="block text-sm font-medium text-orange-400 mb-2">
                        Filters - Medium
                      </label>
                      {newConfig.mutation_axes.filters.medium.map((filter, index) => (
                        <div key={index} className="flex gap-2 mb-2">
                          <input
                            type="text"
                            value={filter}
                            onChange={(e) => updateArrayItem('mutation_axes.filters.medium', index, e.target.value)}
                            className="flex-1 px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white focus:outline-none focus:border-orange-500 transition-colors"
                            placeholder="e.g., onerror"
                          />
                          <button
                            type="button"
                            onClick={() => removeArrayItem('mutation_axes.filters.medium', index)}
                            className="px-4 py-3 bg-red-600/20 hover:bg-red-600/30 text-red-400 rounded-xl transition-colors"
                          >
                            <X className="w-5 h-5" />
                          </button>
                        </div>
                      ))}
                      <button
                        type="button"
                        onClick={() => addArrayItem('mutation_axes.filters.medium')}
                        className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-xl transition-colors flex items-center gap-2"
                      >
                        <Plus className="w-4 h-4" />
                        Add Medium Filter
                      </button>
                    </div>

                    {/* Filters - Advanced */}
                    <div>
                      <label className="block text-sm font-medium text-orange-400 mb-2">
                        Filters - Advanced
                      </label>
                      {newConfig.mutation_axes.filters.advanced.map((filter, index) => (
                        <div key={index} className="flex gap-2 mb-2">
                          <input
                            type="text"
                            value={filter}
                            onChange={(e) => updateArrayItem('mutation_axes.filters.advanced', index, e.target.value)}
                            className="flex-1 px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white focus:outline-none focus:border-orange-500 transition-colors"
                            placeholder="e.g., javascript_protocol"
                          />
                          <button
                            type="button"
                            onClick={() => removeArrayItem('mutation_axes.filters.advanced', index)}
                            className="px-4 py-3 bg-red-600/20 hover:bg-red-600/30 text-red-400 rounded-xl transition-colors"
                          >
                            <X className="w-5 h-5" />
                          </button>
                        </div>
                      ))}
                      <button
                        type="button"
                        onClick={() => addArrayItem('mutation_axes.filters.advanced')}
                        className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-xl transition-colors flex items-center gap-2"
                      >
                        <Plus className="w-4 h-4" />
                        Add Advanced Filter
                      </button>
                    </div>

                    {/* Contexts */}
                    <div>
                      <label className="block text-sm font-medium text-gray-400 mb-2">
                        Contexts
                      </label>
                      {newConfig.mutation_axes.contexts.map((context, index) => (
                        <div key={index} className="flex gap-2 mb-2">
                          <input
                            type="text"
                            value={context}
                            onChange={(e) => updateArrayItem('mutation_axes.contexts', index, e.target.value)}
                            className="flex-1 px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white focus:outline-none focus:border-orange-500 transition-colors"
                            placeholder="e.g., comment_section"
                          />
                          <button
                            type="button"
                            onClick={() => removeArrayItem('mutation_axes.contexts', index)}
                            className="px-4 py-3 bg-red-600/20 hover:bg-red-600/30 text-red-400 rounded-xl transition-colors"
                          >
                            <X className="w-5 h-5" />
                          </button>
                        </div>
                      ))}
                      <button
                        type="button"
                        onClick={() => addArrayItem('mutation_axes.contexts')}
                        className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-xl transition-colors flex items-center gap-2"
                      >
                        <Plus className="w-4 h-4" />
                        Add Context
                      </button>
                    </div>

                    {/* Sinks */}
                    <div>
                      <label className="block text-sm font-medium text-gray-400 mb-2">
                        Sinks
                      </label>
                      {newConfig.mutation_axes.sinks.map((sink, index) => (
                        <div key={index} className="flex gap-2 mb-2">
                          <input
                            type="text"
                            value={sink}
                            onChange={(e) => updateArrayItem('mutation_axes.sinks', index, e.target.value)}
                            className="flex-1 px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white focus:outline-none focus:border-orange-500 transition-colors"
                            placeholder="e.g., innerHTML"
                          />
                          <button
                            type="button"
                            onClick={() => removeArrayItem('mutation_axes.sinks', index)}
                            className="px-4 py-3 bg-red-600/20 hover:bg-red-600/30 text-red-400 rounded-xl transition-colors"
                          >
                            <X className="w-5 h-5" />
                          </button>
                        </div>
                      ))}
                      <button
                        type="button"
                        onClick={() => addArrayItem('mutation_axes.sinks')}
                        className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-xl transition-colors flex items-center gap-2"
                      >
                        <Plus className="w-4 h-4" />
                        Add Sink
                      </button>
                    </div>

                    {/* Encoding */}
                    <div>
                      <label className="block text-sm font-medium text-gray-400 mb-2">
                        Encoding
                      </label>
                      {newConfig.mutation_axes.encoding.map((enc, index) => (
                        <div key={index} className="flex gap-2 mb-2">
                          <input
                            type="text"
                            value={enc}
                            onChange={(e) => updateArrayItem('mutation_axes.encoding', index, e.target.value)}
                            className="flex-1 px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white focus:outline-none focus:border-orange-500 transition-colors"
                            placeholder="e.g., none, html_entities, base64"
                          />
                          <button
                            type="button"
                            onClick={() => removeArrayItem('mutation_axes.encoding', index)}
                            className="px-4 py-3 bg-red-600/20 hover:bg-red-600/30 text-red-400 rounded-xl transition-colors"
                          >
                            <X className="w-5 h-5" />
                          </button>
                        </div>
                      ))}
                      <button
                        type="button"
                        onClick={() => addArrayItem('mutation_axes.encoding')}
                        className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-xl transition-colors flex items-center gap-2"
                      >
                        <Plus className="w-4 h-4" />
                        Add Encoding
                      </button>
                    </div>

                    {/* Output Contexts */}
                    <div>
                      <label className="block text-sm font-medium text-gray-400 mb-2">
                        Output Contexts
                      </label>
                      {newConfig.mutation_axes.output_contexts.map((oc, index) => (
                        <div key={index} className="flex gap-2 mb-2">
                          <input
                            type="text"
                            value={oc}
                            onChange={(e) => updateArrayItem('mutation_axes.output_contexts', index, e.target.value)}
                            className="flex-1 px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white focus:outline-none focus:border-orange-500 transition-colors"
                            placeholder="e.g., html_body"
                          />
                          <button
                            type="button"
                            onClick={() => removeArrayItem('mutation_axes.output_contexts', index)}
                            className="px-4 py-3 bg-red-600/20 hover:bg-red-600/30 text-red-400 rounded-xl transition-colors"
                          >
                            <X className="w-5 h-5" />
                          </button>
                        </div>
                      ))}
                      <button
                        type="button"
                        onClick={() => addArrayItem('mutation_axes.output_contexts')}
                        className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-xl transition-colors flex items-center gap-2"
                      >
                        <Plus className="w-4 h-4" />
                        Add Output Context
                      </button>
                    </div>
                  </div>
                )}
              </div>

              {/* SECTION 3: Variant Configs */}
              <div className="border border-gray-800 rounded-xl p-6 bg-black/30">
                <button
                  type="button"
                  onClick={() => toggleSection('variants')}
                  className="w-full flex items-center justify-between mb-4"
                >
                  <h3 className="text-xl font-bold flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-orange-500" />
                    Variant Configurations
                  </h3>
                  {expandedSections.variants ? (
                    <ChevronUp className="w-5 h-5 text-gray-400" />
                  ) : (
                    <ChevronDown className="w-5 h-5 text-gray-400" />
                  )}
                </button>

                {expandedSections.variants && (
                  <div className="space-y-4">
                    {newConfig.variant_configs.map((variantConfig, varIndex) => (
                      <div key={varIndex} className="border border-gray-700 rounded-xl p-4 bg-black/20">
                        <div className="flex items-center justify-between mb-4">
                          <h4 className="font-bold text-white">Variant #{varIndex + 1}</h4>
                          <button
                            type="button"
                            onClick={() => removeVariantConfig(varIndex)}
                            className="px-3 py-2 bg-red-600/20 hover:bg-red-600/30 text-red-400 rounded-lg transition-colors"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>

                        <div className="space-y-4">
                          <div>
                            <label className="block text-sm font-medium text-gray-400 mb-2">
                              Variant Name
                            </label>
                            <input
                              type="text"
                              value={variantConfig.name}
                              onChange={(e) => updateVariantConfig(varIndex, 'name', e.target.value)}
                              className="w-full px-4 py-3 bg-black/50 border border-gray-800 rounded-xl text-white focus:outline-none focus:border-orange-500 transition-colors"
                              placeholder="e.g., Reflected XSS"
                            />
                          </div>

                          <div>
                            <label className="block text-sm font-medium text-gray-400 mb-2">
                              Parameters
                            </label>
                            {variantConfig.parameters.map((param, paramIndex) => (
                              <div key={paramIndex} className="grid grid-cols-3 gap-2 mb-2">
                                <input
                                  type="text"
                                  value={param.name}
                                  onChange={(e) => updateVariantParameter(varIndex, paramIndex, 'name', e.target.value)}
                                  className="px-3 py-2 bg-black/50 border border-gray-800 rounded-lg text-white text-sm focus:outline-none focus:border-orange-500"
                                  placeholder="Name"
                                />
                                <input
                                  type="text"
                                  value={param.axis}
                                  onChange={(e) => updateVariantParameter(varIndex, paramIndex, 'axis', e.target.value)}
                                  className="px-3 py-2 bg-black/50 border border-gray-800 rounded-lg text-white text-sm focus:outline-none focus:border-orange-500"
                                  placeholder="Axis"
                                />
                                <div className="flex gap-2">
                                  <input
                                    type="text"
                                    value={param.default}
                                    onChange={(e) => updateVariantParameter(varIndex, paramIndex, 'default', e.target.value)}
                                    className="flex-1 px-3 py-2 bg-black/50 border border-gray-800 rounded-lg text-white text-sm focus:outline-none focus:border-orange-500"
                                    placeholder="Default"
                                  />
                                  <button
                                    type="button"
                                    onClick={() => removeVariantParameter(varIndex, paramIndex)}
                                    className="px-3 py-2 bg-red-600/20 hover:bg-red-600/30 text-red-400 rounded-lg transition-colors"
                                  >
                                    <X className="w-4 h-4" />
                                  </button>
                                </div>
                              </div>
                            ))}
                            <button
                              type="button"
                              onClick={() => addVariantParameter(varIndex)}
                              className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-lg transition-colors flex items-center gap-2 text-sm"
                            >
                              <Plus className="w-4 h-4" />
                              Add Parameter
                            </button>
                          </div>
                        </div>
                      </div>
                    ))}

                    <button
                      type="button"
                      onClick={addVariantConfig}
                      className="w-full px-4 py-3 bg-gray-800 hover:bg-gray-700 text-white rounded-xl transition-colors flex items-center justify-center gap-2"
                    >
                      <Plus className="w-5 h-5" />
                      Add Variant Configuration
                    </button>
                  </div>
                )}
              </div>

              {/* Submit Buttons */}
              <div className="flex gap-4 pt-4">
                <button
                  type="submit"
                  disabled={loading}
                  className="flex-1 px-8 py-4 bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 disabled:from-gray-800 disabled:to-gray-800 disabled:opacity-50 text-white font-bold rounded-xl transition-all duration-300 flex items-center justify-center gap-2 hover:scale-105 active:scale-95"
                >
                  {loading ? (
                    <>
                      <Loader className="w-5 h-5 animate-spin" />
                      Creating & Generating...
                    </>
                  ) : (
                    <>
                      <Rocket className="w-5 h-5" />
                      Create & Generate Machine
                    </>
                  )}
                </button>

                <button
                  type="button"
                  onClick={() => setShowCreateForm(false)}
                  disabled={loading}
                  className="px-8 py-4 bg-gray-800 hover:bg-gray-700 disabled:opacity-50 text-white rounded-xl transition-all duration-300 hover:scale-105 active:scale-95"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Configs List */}
        <div className="rounded-2xl border border-gray-900 bg-gradient-to-br from-gray-900/50 to-black/50 backdrop-blur overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-800">
            <h2 className="text-xl font-bold flex items-center gap-2">
              <Code className="w-5 h-5 text-orange-500" />
              Available Configs ({configs.length})
            </h2>
          </div>

          {configs.length === 0 ? (
            <div className="p-12 text-center">
              <Settings className="w-16 h-16 text-gray-700 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-gray-600 mb-2">No Configs Found</h3>
              <p className="text-gray-500 mb-6">Create your first vulnerability config to get started</p>
              <button
                onClick={() => setShowCreateForm(true)}
                className="px-6 py-3 bg-orange-500 hover:bg-orange-600 text-white rounded-xl transition-all duration-300 inline-flex items-center gap-2 hover:scale-105 active:scale-95"
              >
                <Plus className="w-5 h-5" />
                Create Config
              </button>
            </div>
          ) : (
            <div className="divide-y divide-gray-800">
              {configs.map((config, index) => (
                <div
                  key={config.filename}
                  className="group p-6 hover:bg-gray-900/30 transition-all duration-300"
                  style={{ animation: `slideUp 0.4s ease-out ${index * 0.1}s both` }}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <div className="p-2 rounded-lg bg-orange-500/20">
                          <FileCode className="w-5 h-5 text-orange-500" />
                        </div>
                        <div>
                          <h3 className="text-lg font-bold text-white">{config.name}</h3>
                          <p className="text-sm text-gray-500">
                            {config.vulnerability_id} • {config.category}
                          </p>
                        </div>
                      </div>
                      <div className="ml-11">
                        <p className="text-sm text-gray-400 mb-2">
                          {config.variants_count} variant{config.variants_count !== 1 ? 's' : ''}
                        </p>
                        <code className="text-xs text-orange-500 bg-black/30 px-2 py-1 rounded">
                          {config.filename}
                        </code>
                      </div>
                    </div>

                    <div className="flex gap-2">
                      <button
                        onClick={() => handleGenerateMachine(config.category)}
                        disabled={generatingMachine === config.category}
                        className="px-4 py-2 bg-orange-600/20 hover:bg-orange-600/30 disabled:bg-gray-800 disabled:opacity-50 text-orange-400 rounded-xl transition-all duration-300 flex items-center gap-2 hover:scale-105 active:scale-95"
                        title="Generate complete machine"
                      >
                        {generatingMachine === config.category ? (
                          <>
                            <Loader className="w-4 h-4 animate-spin" />
                            Generating...
                          </>
                        ) : (
                          <>
                            <Rocket className="w-4 h-4" />
                            Generate Machine
                          </>
                        )}
                      </button>

                      <button
                        onClick={() => handleGenerateBlueprint(config.category)}
                        disabled={loading}
                        className="px-4 py-2 bg-green-600/20 hover:bg-green-600/30 disabled:bg-gray-800 disabled:opacity-50 text-green-400 rounded-xl transition-all duration-300 flex items-center gap-2 hover:scale-105 active:scale-95"
                        title="Generate only blueprint"
                      >
                        <Hammer className="w-4 h-4" />
                        Blueprint Only
                      </button>

                      <button
                        onClick={() => handleDeleteConfig(config.category)}
                        disabled={loading}
                        className="px-4 py-2 bg-red-600/20 hover:bg-red-600/30 disabled:bg-gray-800 disabled:opacity-50 text-red-400 rounded-xl transition-all duration-300 flex items-center gap-2 hover:scale-105 active:scale-95"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

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

        @keyframes slideDown {
          from {
            opacity: 0;
            transform: translateY(-10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  );
};

export default ConfigManager;
