<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
    <h3 class="text-lg font-semibold text-gray-900 mb-4">Comparaison Email vs Appel</h3>
    <div v-if="loading" class="h-64 flex items-center justify-center">
      <div class="text-gray-400">Chargement...</div>
    </div>
    <div v-else>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-4">
        <!-- Email Donut -->
        <div class="flex flex-col items-center">
          <h4 class="text-sm font-medium text-gray-700 mb-2">Email</h4>
          <div class="w-48 h-48">
            <Doughnut :data="emailChartData" :options="chartOptions" />
          </div>
          <div class="mt-3 text-center">
            <div class="text-2xl font-bold text-gray-900">
              {{ channelData.email.satisfaction_score.toFixed(1) }}%
            </div>
            <div class="text-xs text-gray-500">Score de satisfaction</div>
            <div class="text-sm text-gray-600 mt-2">
              {{ formatNumber(channelData.email.total) }} conversations
            </div>
          </div>
        </div>

        <!-- Call Donut -->
        <div class="flex flex-col items-center">
          <h4 class="text-sm font-medium text-gray-700 mb-2">Appel Téléphonique</h4>
          <div class="w-48 h-48">
            <Doughnut :data="callChartData" :options="chartOptions" />
          </div>
          <div class="mt-3 text-center">
            <div class="text-2xl font-bold text-gray-900">
              {{ channelData.call.satisfaction_score.toFixed(1) }}%
            </div>
            <div class="text-xs text-gray-500">Score de satisfaction</div>
            <div class="text-sm text-gray-600 mt-2">
              {{ formatNumber(channelData.call.total) }} conversations
            </div>
          </div>
        </div>
      </div>

      <!-- Insight Card -->
      <div class="mt-6 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-200">
        <div class="flex items-start">
          <div class="flex-shrink-0">
            <svg class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="ml-3 flex-1">
            <h5 class="text-sm font-semibold text-blue-900 mb-1">Insight</h5>
            <p class="text-sm text-blue-800">
              {{ channelData.insight.message }}
            </p>
            <div class="mt-2 text-xs text-blue-700 font-medium">
              Différence: {{ Math.abs(channelData.insight.difference).toFixed(1) }}%
            </div>
          </div>
        </div>
      </div>

      <!-- Comparison Stats -->
      <div class="mt-4 grid grid-cols-2 gap-4">
        <div class="text-center p-3 bg-gray-50 rounded-md">
          <div class="text-xs text-gray-600 mb-1">Email</div>
          <div class="text-lg font-semibold text-gray-900">
            {{ channelData.email.positive_percentage }}% positif
          </div>
          <div class="text-xs text-red-600 mt-1">
            {{ channelData.email.negative_percentage }}% négatif
          </div>
        </div>
        <div class="text-center p-3 bg-gray-50 rounded-md">
          <div class="text-xs text-gray-600 mb-1">Appel</div>
          <div class="text-lg font-semibold text-gray-900">
            {{ channelData.call.positive_percentage }}% positif
          </div>
          <div class="text-xs text-red-600 mt-1">
            {{ channelData.call.negative_percentage }}% négatif
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Doughnut } from 'vue-chartjs';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { dataService } from '../services/dataService';

ChartJS.register(ArcElement, Tooltip, Legend);

export default {
  name: 'ChannelComparison',
  components: {
    Doughnut
  },
  data() {
    return {
      loading: true,
      channelData: null,
      emailChartData: null,
      callChartData: null,
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'bottom'
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
        this.channelData = await dataService.getChannelComparison();
        
        // Email chart data
        this.emailChartData = {
          labels: ['Positif', 'Neutre', 'Négatif'],
          datasets: [
            {
              data: [
                this.channelData.email.positive,
                this.channelData.email.neutral,
                this.channelData.email.negative
              ],
              backgroundColor: [
                'rgba(16, 185, 129, 0.8)',
                'rgba(234, 179, 8, 0.8)',
                'rgba(239, 68, 68, 0.8)'
              ],
              borderWidth: 0
            }
          ]
        };

        // Call chart data
        this.callChartData = {
          labels: ['Positif', 'Neutre', 'Négatif'],
          datasets: [
            {
              data: [
                this.channelData.call.positive,
                this.channelData.call.neutral,
                this.channelData.call.negative
              ],
              backgroundColor: [
                'rgba(16, 185, 129, 0.8)',
                'rgba(234, 179, 8, 0.8)',
                'rgba(239, 68, 68, 0.8)'
              ],
              borderWidth: 0
            }
          ]
        };

        this.loading = false;
      } catch (error) {
        console.error('Error loading channel comparison:', error);
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

