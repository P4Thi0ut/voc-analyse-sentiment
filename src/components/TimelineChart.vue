<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
    <h3 class="text-lg font-semibold text-gray-900 mb-4">Évolution des tendances</h3>
    <div v-if="loading" class="h-64 flex items-center justify-center">
      <div class="text-gray-400">Chargement...</div>
    </div>
    <div v-else class="h-80">
      <Chart type="bar" :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script>
import { Chart } from 'vue-chartjs';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { dataService } from '../services/dataService';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export default {
  name: 'TimelineChart',
  components: {
    Chart
  },
  data() {
    return {
      loading: true,
      timeline: [],
      chartData: null,
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          mode: 'index',
          intersect: false
        },
        plugins: {
          legend: {
            display: true,
            position: 'top'
          },
          tooltip: {
            callbacks: {
              label: (context) => {
                if (context.datasetIndex === 0) {
                  return `Volume: ${context.parsed.y} conversations`;
                } else {
                  return `Satisfaction: ${context.parsed.y}%`;
                }
              }
            }
          }
        },
        scales: {
          x: {
            display: true,
            title: {
              display: true,
              text: 'Mois'
            }
          },
          y: {
            type: 'linear',
            display: true,
            position: 'left',
            title: {
              display: true,
              text: 'Volume'
            },
            beginAtZero: true
          },
          y1: {
            type: 'linear',
            display: true,
            position: 'right',
            title: {
              display: true,
              text: 'Satisfaction (%)'
            },
            beginAtZero: true,
            max: 100,
            grid: {
              drawOnChartArea: false
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
        this.timeline = await dataService.getTimeline();
        this.chartData = {
          labels: this.timeline.map(item => {
            const [year, month] = item.month.split('-');
            const monthNames = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc'];
            return `${monthNames[parseInt(month) - 1]} ${year}`;
          }),
          datasets: [
            {
              label: 'Volume',
              type: 'bar',
              data: this.timeline.map(item => item.volume),
              backgroundColor: 'rgba(59, 130, 246, 0.5)',
              borderColor: 'rgba(59, 130, 246, 1)',
              borderWidth: 1,
              yAxisID: 'y'
            },
            {
              label: 'Satisfaction (%)',
              type: 'line',
              data: this.timeline.map(item => item.satisfaction),
              borderColor: 'rgba(16, 185, 129, 1)',
              backgroundColor: 'rgba(16, 185, 129, 0.1)',
              borderWidth: 2,
              fill: true,
              tension: 0.4,
              yAxisID: 'y1'
            }
          ]
        };
        this.loading = false;
      } catch (error) {
        console.error('Error loading timeline:', error);
        this.loading = false;
      }
    }
  }
};
</script>

