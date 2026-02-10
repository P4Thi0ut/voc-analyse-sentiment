/**
 * Data Service - Fetches mock JSON data from mocked-api folder
 * This isolates data access so swapping to real API later is trivial
 */

export const dataService = {
  /**
   * Fetch global statistics
   */
  async getStats() {
    const response = await fetch('/mocked-api/stats.json');
    return await response.json();
  },

  /**
   * Fetch word cloud data (aggregated keywords)
   */
  async getWordCloud() {
    const response = await fetch('/mocked-api/word-cloud.json');
    return await response.json();
  },

  /**
   * Fetch timeline data (monthly volume and satisfaction)
   */
  async getTimeline() {
    const response = await fetch('/mocked-api/timeline.json');
    return await response.json();
  },

  /**
   * Fetch themes aggregation data
   */
  async getThemes() {
    const response = await fetch('/mocked-api/themes.json');
    return await response.json();
  },

  /**
   * Fetch conversations/verbatims list
   */
  async getConversations() {
    const response = await fetch('/mocked-api/conversations.json');
    return await response.json();
  },

  /**
   * Fetch KPI metrics
   */
  async getKPIs() {
    const response = await fetch('/mocked-api/kpis.json');
    return await response.json();
  },

  /**
   * Fetch prioritization matrix data
   */
  async getPrioritizationMatrix() {
    const response = await fetch('/mocked-api/prioritization-matrix.json');
    return await response.json();
  }
};

