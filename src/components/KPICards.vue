<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4 mb-6">
    <!-- Card 1: Verbatims Traités -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
      <div class="text-xs font-semibold text-gray-600 uppercase tracking-wide mb-2">
        {{ kpis.verbatims_traites?.label }}
      </div>
      <div class="text-3xl font-bold text-blue-600 mb-1">
        {{ formatNumber(kpis.verbatims_traites?.value) }}
      </div>
      <div v-if="kpis.verbatims_traites?.trend" class="flex items-center text-sm">
        <svg
          v-if="kpis.verbatims_traites.trend_direction === 'up'"
          class="w-4 h-4 text-green-500 mr-1"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path fill-rule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z" clip-rule="evenodd" />
        </svg>
        <svg
          v-else
          class="w-4 h-4 text-red-500 mr-1"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path fill-rule="evenodd" d="M14.707 12.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 14.586V3a1 1 0 012 0v11.586l2.293-2.293a1 1 0 011.414 0z" clip-rule="evenodd" />
        </svg>
        <span :class="kpis.verbatims_traites.trend_direction === 'up' ? 'text-green-600' : 'text-red-600'">
          {{ Math.abs(kpis.verbatims_traites.trend) }}% {{ kpis.verbatims_traites.comparison }}
        </span>
      </div>
    </div>

    <!-- Card 2: Score Satisfaction -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
      <div class="text-xs font-semibold text-gray-600 uppercase tracking-wide mb-2">
        {{ kpis.score_satisfaction?.label }}
      </div>
      <div class="text-3xl font-bold text-green-600 mb-1">
        {{ kpis.score_satisfaction?.value }}{{ kpis.score_satisfaction?.unit }}
      </div>
      <div v-if="kpis.score_satisfaction?.trend" class="flex items-center text-sm">
        <svg
          v-if="kpis.score_satisfaction.trend_direction === 'up'"
          class="w-4 h-4 text-green-500 mr-1"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path fill-rule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z" clip-rule="evenodd" />
        </svg>
        <svg
          v-else
          class="w-4 h-4 text-red-500 mr-1"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path fill-rule="evenodd" d="M14.707 12.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 14.586V3a1 1 0 012 0v11.586l2.293-2.293a1 1 0 011.414 0z" clip-rule="evenodd" />
        </svg>
        <span :class="kpis.score_satisfaction.trend_direction === 'up' ? 'text-green-600' : 'text-red-600'">
          {{ Math.abs(kpis.score_satisfaction.trend) }}% {{ kpis.score_satisfaction.comparison }}
        </span>
      </div>
    </div>

    <!-- Card 3: Promoteurs -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
      <div class="text-xs font-semibold text-gray-600 uppercase tracking-wide mb-2">
        {{ kpis.promoteurs?.label }}
      </div>
      <div class="text-3xl font-bold text-green-600 mb-1">
        {{ formatNumber(kpis.promoteurs?.value) }}
      </div>
      <div class="text-sm text-gray-600">
        {{ kpis.promoteurs?.percentage }}%
      </div>
    </div>

    <!-- Card 4: Passifs -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
      <div class="text-xs font-semibold text-gray-600 uppercase tracking-wide mb-2">
        {{ kpis.passifs?.label }}
      </div>
      <div class="text-3xl font-bold text-gray-500 mb-1">
        {{ formatNumber(kpis.passifs?.value) }}
      </div>
      <div class="text-sm text-gray-600">
        {{ kpis.passifs?.percentage }}%
      </div>
    </div>

    <!-- Card 5: Détracteurs -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
      <div class="text-xs font-semibold text-gray-600 uppercase tracking-wide mb-2">
        {{ kpis.detracteurs?.label }}
      </div>
      <div class="text-3xl font-bold text-red-600 mb-1">
        {{ formatNumber(kpis.detracteurs?.value) }}
      </div>
      <div class="text-sm text-gray-600">
        {{ kpis.detracteurs?.percentage }}%
      </div>
    </div>

    <!-- Card 6: Thème Prioritaire -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
      <div class="text-xs font-semibold text-gray-600 uppercase tracking-wide mb-2">
        {{ kpis.theme_prioritaire?.label }}
      </div>
      <div class="text-xl font-bold text-red-600 mb-2">
        {{ kpis.theme_prioritaire?.theme }}
      </div>
      <div class="text-xs text-gray-600 space-y-1">
        <div>{{ formatNumber(kpis.theme_prioritaire?.mentions) }} mentions</div>
        <div>{{ kpis.theme_prioritaire?.negative_percentage }}% négatif</div>
        <div>Impact: {{ kpis.theme_prioritaire?.impact }}%</div>
      </div>
    </div>
  </div>
</template>

<script>
import { dataService } from '../services/dataService';

export default {
  name: 'KPICards',
  data() {
    return {
      loading: true,
      kpis: {}
    };
  },
  async mounted() {
    await this.loadData();
  },
  methods: {
    async loadData() {
      try {
        this.kpis = await dataService.getKPIs();
        this.loading = false;
      } catch (error) {
        console.error('Error loading KPIs:', error);
        this.loading = false;
      }
    },
    formatNumber(value) {
      if (!value) return '0';
      return new Intl.NumberFormat('fr-FR').format(value);
    }
  }
};
</script>

