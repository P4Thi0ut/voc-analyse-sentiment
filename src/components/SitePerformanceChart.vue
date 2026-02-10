<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-lg font-semibold text-gray-900">Performance par Site</h3>
      <button
        v-if="selectedSite"
        @click="clearFilter"
        class="text-sm text-blue-600 hover:text-blue-800"
      >
        Effacer le filtre
      </button>
    </div>
    <div v-if="loading" class="h-64 flex items-center justify-center">
      <div class="text-gray-400">Chargement...</div>
    </div>
    <div v-else class="h-96">
      <Bar ref="chart" :data="chartData" :options="chartOptions" />
    </div>
    <div v-if="selectedSite" class="mt-4 p-3 bg-blue-50 rounded-md text-sm text-blue-800">
      <strong>Filtre actif:</strong> {{ selectedSite }} - Dashboard filtré sur ce site
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
  name: 'SitePerformanceChart',
  components: {
    Bar
  },
  props: {
    selectedSite: {
      type: String,
      default: null
    }
  },
  emits: ['site-selected'],
  data() {
    return {
      loading: true,
      sites: [],
      averageSatisfaction: 0,
      chartData: null,
      chartOptions: null
    };
  },
  async mounted() {
    await this.loadData();
  },
  watch: {
    selectedSite() {
      this.updateChartColors();
    }
  },
  methods: {
    getChartOptions() {
      const self = this; // Store component reference
      return {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              label: (context) => {
                const site = self.sites[context.dataIndex];
                return [
                  `Satisfaction: ${site.satisfaction_percentage.toFixed(1)}%`,
                  `Volume: ${self.formatNumber(site.volume)} conversations`,
                  `Positif: ${site.positive} | Neutre: ${site.neutral} | Négatif: ${site.negative}`
                ];
              }
            }
          }
        },
        scales: {
          x: {
            beginAtZero: true,
            max: 100,
            title: {
              display: true,
              text: 'Score de satisfaction (%)'
            },
            ticks: {
              callback: function(value) {
                return value + '%';
              }
            }
          },
          y: {
            title: {
              display: true,
              text: 'Sites'
            }
          }
        },
        onClick: (event, elements) => {
          if (elements.length > 0) {
            const index = elements[0].index;
            const site = self.sites[index];
            self.$emit('site-selected', site.site);
          }
        },
        onHover: (event, elements) => {
          if (event.native && event.native.target) {
            event.native.target.style.cursor = elements.length > 0 ? 'pointer' : 'default';
          }
        }
      };
    },
    async loadData() {
      try {
        this.sites = await dataService.getSitePerformance();
        // Sort by satisfaction descending
        this.sites.sort((a, b) => b.satisfaction_percentage - a.satisfaction_percentage);
        
        // Calculate average
        const total = this.sites.reduce((sum, site) => sum + site.satisfaction_percentage, 0);
        this.averageSatisfaction = total / this.sites.length;
        
        // Initialize chart options after data is loaded
        this.chartOptions = this.getChartOptions();
        
        this.updateChartData();
        this.loading = false;
      } catch (error) {
        console.error('Error loading site performance:', error);
        this.loading = false;
      }
    },
    updateChartData() {
      this.chartData = {
        labels: this.sites.map(site => site.site),
        datasets: [
          {
            label: 'Satisfaction (%)',
            data: this.sites.map(site => site.satisfaction_percentage),
            backgroundColor: this.sites.map(site => {
              if (this.selectedSite && site.site === this.selectedSite) {
                return 'rgba(59, 130, 246, 0.8)'; // Blue for selected
              }
              return site.satisfaction_percentage >= this.averageSatisfaction
                ? 'rgba(16, 185, 129, 0.8)' // Green for above average
                : 'rgba(239, 68, 68, 0.8)'; // Red for below average
            }),
            borderColor: this.sites.map(site => {
              if (this.selectedSite && site.site === this.selectedSite) {
                return 'rgba(59, 130, 246, 1)';
              }
              return site.satisfaction_percentage >= this.averageSatisfaction
                ? 'rgba(16, 185, 129, 1)'
                : 'rgba(239, 68, 68, 1)';
            }),
            borderWidth: 2
          }
        ]
      };
    },
    updateChartColors() {
      if (this.chartData) {
        this.chartData.datasets[0].backgroundColor = this.sites.map(site => {
          if (this.selectedSite && site.site === this.selectedSite) {
            return 'rgba(59, 130, 246, 0.8)';
          }
          return site.satisfaction_percentage >= this.averageSatisfaction
            ? 'rgba(16, 185, 129, 0.8)'
            : 'rgba(239, 68, 68, 0.8)';
        });
        this.chartData.datasets[0].borderColor = this.sites.map(site => {
          if (this.selectedSite && site.site === this.selectedSite) {
            return 'rgba(59, 130, 246, 1)';
          }
          return site.satisfaction_percentage >= this.averageSatisfaction
            ? 'rgba(16, 185, 129, 1)'
            : 'rgba(239, 68, 68, 1)';
        });
      }
    },
    clearFilter() {
      this.$emit('site-selected', null);
    },
    formatNumber(value) {
      if (!value) return '0';
      return new Intl.NumberFormat('fr-FR').format(value);
    }
  }
};
</script>

