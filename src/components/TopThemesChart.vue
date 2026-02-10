<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
    <h3 class="text-lg font-semibold text-gray-900 mb-4">Thèmes les plus fréquents</h3>
    <div v-if="loading" class="h-64 flex items-center justify-center">
      <div class="text-gray-400">Chargement...</div>
    </div>
    <div v-else class="h-80">
      <Bar :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script>
import { Bar } from 'vue-chartjs';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { dataService } from '../services/dataService';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export default {
  name: 'TopThemesChart',
  components: {
    Bar
  },
  data() {
    return {
      loading: true,
      themes: [],
      chartData: null,
      chartOptions: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'top'
          },
          tooltip: {
            callbacks: {
              label: (context) => {
                const label = context.dataset.label || '';
                const value = context.parsed.x;
                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : '0.0';
                return `${label}: ${value} (${percentage}%)`;
              }
            }
          }
        },
        scales: {
          x: {
            stacked: true,
            beginAtZero: true,
            title: {
              display: true,
              text: 'Nombre de mentions'
            }
          },
          y: {
            stacked: true,
            title: {
              display: true,
              text: 'Thèmes'
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
        this.themes = await dataService.getThemes();
        // Sort by count descending
        this.themes.sort((a, b) => b.count - a.count);
        
        this.chartData = {
          labels: this.themes.map(theme => theme.theme),
          datasets: [
            {
              label: 'Positif',
              data: this.themes.map(theme => theme.sentiment.positive),
              backgroundColor: 'rgba(16, 185, 129, 0.8)',
              borderColor: 'rgba(16, 185, 129, 1)',
              borderWidth: 1
            },
            {
              label: 'Neutre',
              data: this.themes.map(theme => theme.sentiment.neutral),
              backgroundColor: 'rgba(234, 179, 8, 0.8)',
              borderColor: 'rgba(234, 179, 8, 1)',
              borderWidth: 1
            },
            {
              label: 'Négatif',
              data: this.themes.map(theme => theme.sentiment.negative),
              backgroundColor: 'rgba(239, 68, 68, 0.8)',
              borderColor: 'rgba(239, 68, 68, 1)',
              borderWidth: 1
            }
          ]
        };
        this.loading = false;
      } catch (error) {
        console.error('Error loading themes:', error);
        this.loading = false;
      }
    }
  }
};
</script>

