<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
    <h3 class="text-lg font-semibold text-gray-900 mb-4">Répartition des sentiments</h3>
    <div v-if="loading" class="h-64 flex items-center justify-center">
      <div class="text-gray-400">Chargement...</div>
    </div>
    <div v-else class="flex flex-col items-center">
      <div class="w-64 h-64">
        <Doughnut :data="chartData" :options="chartOptions" />
      </div>
      <div class="mt-4 flex space-x-6">
        <div class="flex items-center">
          <div class="w-4 h-4 bg-green-500 rounded-full mr-2"></div>
          <span class="text-sm text-gray-600">Positif: {{ stats.positive_percentage }}%</span>
        </div>
        <div class="flex items-center">
          <div class="w-4 h-4 bg-yellow-500 rounded-full mr-2"></div>
          <span class="text-sm text-gray-600">Neutre: {{ stats.neutral_percentage }}%</span>
        </div>
        <div class="flex items-center">
          <div class="w-4 h-4 bg-red-500 rounded-full mr-2"></div>
          <span class="text-sm text-gray-600">Négatif: {{ stats.negative_percentage }}%</span>
        </div>
      </div>
      <div class="mt-2 text-sm text-gray-500">Total: {{ stats.total }} conversations</div>
    </div>
  </div>
</template>

<script>
import { Doughnut } from 'vue-chartjs';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { dataService } from '../services/dataService';

ChartJS.register(ArcElement, Tooltip, Legend);

export default {
  name: 'SentimentDonut',
  components: {
    Doughnut
  },
  data() {
    return {
      loading: true,
      stats: {
        total: 0,
        positive: 0,
        neutral: 0,
        negative: 0,
        positive_percentage: 0,
        neutral_percentage: 0,
        negative_percentage: 0
      },
      chartData: null,
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              label: (context) => {
                const label = context.label || '';
                const value = context.parsed || 0;
                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                const percentage = ((value / total) * 100).toFixed(1);
                return `${label}: ${value} (${percentage}%)`;
              }
            }
          }
        }
      }
    };
  },
  async mounted() {
    await this.loadData();
  },
  methods: {
    async loadData() {
      try {
        this.stats = await dataService.getStats();
        this.chartData = {
          labels: ['Positif', 'Neutre', 'Négatif'],
          datasets: [
            {
              data: [
                this.stats.positive,
                this.stats.neutral,
                this.stats.negative
              ],
              backgroundColor: [
                '#10b981', // green-500
                '#eab308', // yellow-500
                '#ef4444'  // red-500
              ],
              borderWidth: 0
            }
          ]
        };
        this.loading = false;
      } catch (error) {
        console.error('Error loading stats:', error);
        this.loading = false;
      }
    }
  }
};
</script>

