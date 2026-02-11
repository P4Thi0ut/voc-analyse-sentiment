/**
 * Data Service - Fetches mock JSON data from mocked-api folder
 * This isolates data access so swapping to real API later is trivial
 */

// BASE_URL is "/" locally and "/voc-analyse-sentiment/" on GitHub Pages.
// It ensures fetch paths resolve correctly regardless of where the app is hosted.
const BASE = import.meta.env.BASE_URL;

export const dataService = {
  /**
   * Fetch global statistics
   */
  async getStats() {
    const response = await fetch(`${BASE}mocked-api/stats_dpd.json`);
    return await response.json();
  },

  /**
   * Fetch word cloud data (aggregated keywords)
   */
  async getWordCloud() {
    const response = await fetch(`${BASE}mocked-api/word-cloud_dpd.json`);
    return await response.json();
  },

  /**
   * Fetch timeline data (monthly volume and satisfaction)
   */
  async getTimeline() {
    const response = await fetch(`${BASE}mocked-api/timeline_dpd.json`);
    return await response.json();
  },

  /**
   * Fetch themes aggregation data
   */
  async getThemes() {
    const response = await fetch(`${BASE}mocked-api/themes_dpd.json`);
    return await response.json();
  },

  /**
   * Fetch conversations/verbatims list
   */
  async getConversations() {
    const response = await fetch(`${BASE}mocked-api/conversations_dpd.json`);
    return await response.json();
  },

  /**
   * Fetch KPI metrics
   */
  async getKPIs() {
    const response = await fetch(`${BASE}mocked-api/kpis_dpd.json`);
    return await response.json();
  },

  /**
   * Fetch prioritization matrix data
   */
  async getPrioritizationMatrix() {
    const response = await fetch(`${BASE}mocked-api/prioritization-matrix_dpd.json`);
    return await response.json();
  },

  /**
   * Fetch site performance data (V2)
   */
  async getSitePerformance() {
    const response = await fetch(`${BASE}mocked-api/site-performance_dpd.json`);
    return await response.json();
  },

  /**
   * Fetch channel comparison data (V2)
   */
  async getChannelComparison() {
    const response = await fetch(`${BASE}mocked-api/channel-comparison_dpd.json`);
    return await response.json();
  }
};
