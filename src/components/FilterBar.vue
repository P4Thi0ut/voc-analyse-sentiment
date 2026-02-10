<template>
  <div class="flex items-center space-x-3">
    <!-- Organization Filter -->
    <select
      v-model="filters.organization"
      @change="applyFilters"
      class="px-3 py-2 border border-gray-300 rounded-md text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
    >
      <option value="DPD">DPD</option>
      <option value="TUI">TUI</option>
    </select>

    <!-- Team Filter -->
    <select
      v-model="filters.team"
      @change="applyFilters"
      class="px-3 py-2 border border-gray-300 rounded-md text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
    >
      <option value="all">Toutes les équipes</option>
      <option value="ADM">ADM</option>
      <option value="DPD">DPD</option>
      <option value="OCC">OCC</option>
    </select>

    <!-- Project Filter -->
    <select
      v-model="filters.project"
      @change="applyFilters"
      class="px-3 py-2 border border-gray-300 rounded-md text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
    >
      <option value="all">Tous les projets</option>
      <option value="Desti ADM">Desti ADM</option>
      <option value="Desti OCC">Desti OCC</option>
      <option value="Expe DPD">Expe DPD</option>
    </select>

    <!-- Site Filter (if site is selected) -->
    <select
      v-if="selectedSite"
      v-model="filters.site"
      @change="applyFilters"
      class="px-3 py-2 border border-blue-300 rounded-md text-sm bg-blue-50 text-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
    >
      <option :value="selectedSite">{{ selectedSite }}</option>
      <option value="all">Tous les sites</option>
    </select>

    <!-- Date Range Filter -->
    <div class="flex items-center space-x-2">
      <input
        v-model="filters.dateFrom"
        type="date"
        @change="applyFilters"
        class="px-3 py-2 border border-gray-300 rounded-md text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="De"
      />
      <span class="text-gray-500">à</span>
      <input
        v-model="filters.dateTo"
        type="date"
        @change="applyFilters"
        class="px-3 py-2 border border-gray-300 rounded-md text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="À"
      />
    </div>

    <!-- Sentiment Filter -->
    <div class="flex items-center space-x-2 px-3 py-2 border border-gray-300 rounded-md bg-white">
      <label class="text-xs text-gray-600 mr-2">Sentiment:</label>
      <label class="flex items-center space-x-1 cursor-pointer">
        <input
          v-model="filters.sentiment"
          type="checkbox"
          value="positive"
          @change="applyFilters"
          class="rounded text-green-600 focus:ring-green-500"
        />
        <span class="text-xs text-green-600">Positif</span>
      </label>
      <label class="flex items-center space-x-1 cursor-pointer">
        <input
          v-model="filters.sentiment"
          type="checkbox"
          value="neutral"
          @change="applyFilters"
          class="rounded text-yellow-600 focus:ring-yellow-500"
        />
        <span class="text-xs text-yellow-600">Neutre</span>
      </label>
      <label class="flex items-center space-x-1 cursor-pointer">
        <input
          v-model="filters.sentiment"
          type="checkbox"
          value="negative"
          @change="applyFilters"
          class="rounded text-red-600 focus:ring-red-500"
        />
        <span class="text-xs text-red-600">Négatif</span>
      </label>
    </div>

    <!-- Clear Filters Button -->
    <button
      v-if="hasActiveFilters"
      @click="clearFilters"
      class="px-4 py-2 bg-gray-100 text-gray-700 rounded-md text-sm font-medium hover:bg-gray-200 flex items-center space-x-2"
    >
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
      </svg>
      <span>Effacer</span>
    </button>

    <!-- Active Filters Count Badge -->
    <div
      v-if="activeFilterCount > 0"
      class="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-medium"
    >
      {{ activeFilterCount }} filtre{{ activeFilterCount > 1 ? 's' : '' }} actif{{ activeFilterCount > 1 ? 's' : '' }}
    </div>

    <!-- Export Button -->
    <button
      class="px-4 py-2 bg-purple-600 text-white rounded-md text-sm font-medium hover:bg-purple-700 flex items-center space-x-2"
    >
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <span>Exporter</span>
    </button>
  </div>
</template>

<script>
export default {
  name: 'FilterBar',
  props: {
    selectedSite: {
      type: String,
      default: null
    }
  },
  emits: ['filters-changed'],
  data() {
    return {
      filters: {
        organization: 'DPD',
        team: 'all',
        project: 'all',
        site: null,
        dateFrom: null,
        dateTo: null,
        sentiment: []
      }
    };
  },
  computed: {
    hasActiveFilters() {
      return (
        this.filters.team !== 'all' ||
        this.filters.project !== 'all' ||
        this.filters.site !== null ||
        this.filters.dateFrom !== null ||
        this.filters.dateTo !== null ||
        this.filters.sentiment.length > 0
      );
    },
    activeFilterCount() {
      let count = 0;
      if (this.filters.team !== 'all') count++;
      if (this.filters.project !== 'all') count++;
      if (this.filters.site !== null) count++;
      if (this.filters.dateFrom !== null) count++;
      if (this.filters.dateTo !== null) count++;
      if (this.filters.sentiment.length > 0) count++;
      return count;
    }
  },
  watch: {
    selectedSite(newSite) {
      this.filters.site = newSite || null;
      if (newSite) {
        this.applyFilters();
      }
    }
  },
  methods: {
    applyFilters() {
      this.$emit('filters-changed', { ...this.filters });
    },
    clearFilters() {
      this.filters = {
        organization: 'DPD',
        team: 'all',
        project: 'all',
        site: null,
        dateFrom: null,
        dateTo: null,
        sentiment: []
      };
      this.$emit('filters-changed', { ...this.filters });
    }
  }
};
</script>

