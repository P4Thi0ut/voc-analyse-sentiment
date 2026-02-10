<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
    <h3 class="text-lg font-semibold text-gray-900 mb-4">Matrice de Priorisation (Impact × Fréquence)</h3>
    <div v-if="loading" class="h-96 flex items-center justify-center">
      <div class="text-gray-400">Chargement...</div>
    </div>
    <div v-else class="relative">
      <canvas ref="canvas" style="width: 100%; height: 500px;"></canvas>
      <!-- Tooltip -->
      <div
        v-if="hoveredTheme"
        class="absolute bg-white border border-gray-300 rounded-lg shadow-lg p-3 z-10 pointer-events-none"
        :style="{ left: tooltipX + 'px', top: tooltipY + 'px' }"
      >
        <div class="font-semibold text-gray-900">{{ hoveredTheme.label }}</div>
        <div class="text-sm text-gray-600 mt-1">Mentions: {{ formatNumber(hoveredTheme.mentions) }}</div>
        <div class="text-sm text-gray-600">Fréquence: {{ hoveredTheme.frequency }}%</div>
        <div class="text-sm text-gray-600">Impact: {{ hoveredTheme.impact > 0 ? '+' : '' }}{{ hoveredTheme.impact }}%</div>
        <div class="text-sm text-green-600">Positif: {{ hoveredTheme.positive_pct }}%</div>
        <div class="text-sm text-red-600">Négatif: {{ hoveredTheme.negative_pct }}%</div>
      </div>
    </div>
  </div>
</template>

<script>
import { dataService } from '../services/dataService';

const QUADRANT_COLORS = {
  priorities: { bg: 'rgba(239, 68, 68, 0.06)', bubble: '#ef4444', label: 'PRIORITÉS', labelColor: '#dc2626' },
  emerging: { bg: 'rgba(249, 115, 22, 0.06)', bubble: '#f97316', label: 'SIGNAUX ÉMERGENTS', labelColor: '#ea580c' },
  strengths: { bg: 'rgba(16, 185, 129, 0.06)', bubble: '#10b981', label: 'FORCES', labelColor: '#059669' },
  neutral: { bg: 'rgba(156, 163, 175, 0.06)', bubble: '#9ca3af', label: 'NEUTRE', labelColor: '#6b7280' }
};

export default {
  name: 'PrioritizationMatrix',
  data() {
    return {
      loading: true,
      matrixData: null,
      hoveredTheme: null,
      tooltipX: 0,
      tooltipY: 0,
      bubbles: [],
      // Chart area dimensions (set on render)
      chartArea: { left: 0, top: 0, right: 0, bottom: 0, width: 0, height: 0 }
    };
  },
  async mounted() {
    await this.loadData();
  },
  methods: {
    async loadData() {
      try {
        this.matrixData = await dataService.getPrioritizationMatrix();
        this.loading = false;
        this.$nextTick(() => {
          this.render();
          this.setupEvents();
        });
      } catch (error) {
        console.error('Error loading prioritization matrix:', error);
        this.loading = false;
      }
    },

    render() {
      const canvas = this.$refs.canvas;
      if (!canvas || !this.matrixData) return;

      const dpr = window.devicePixelRatio || 1;
      const rect = canvas.parentElement.getBoundingClientRect();
      const width = rect.width;
      const height = 500;

      canvas.width = width * dpr;
      canvas.height = height * dpr;
      canvas.style.width = width + 'px';
      canvas.style.height = height + 'px';

      const ctx = canvas.getContext('2d');
      ctx.scale(dpr, dpr);

      // Margins
      const margin = { top: 30, right: 30, bottom: 50, left: 60 };
      const chartW = width - margin.left - margin.right;
      const chartH = height - margin.top - margin.bottom;

      this.chartArea = {
        left: margin.left,
        top: margin.top,
        right: width - margin.right,
        bottom: height - margin.bottom,
        width: chartW,
        height: chartH
      };

      // Clear
      ctx.clearRect(0, 0, width, height);

      // Data ranges
      const themes = this.matrixData.themes;
      const freqs = themes.map(t => t.frequency);
      const impacts = themes.map(t => t.impact);
      const mentions = themes.map(t => t.mentions);

      const maxFreq = Math.max(...freqs) * 1.2;
      const maxImpact = Math.max(...impacts.map(Math.abs)) * 1.4;
      const maxMentions = Math.max(...mentions);
      const minMentions = Math.min(...mentions);

      // Frequency threshold (10% as per spec)
      const freqThreshold = 10;
      // Impact threshold = 0

      // Scale helpers
      const xScale = (freq) => margin.left + (freq / maxFreq) * chartW;
      const yScale = (impact) => margin.top + chartH / 2 - (impact / maxImpact) * (chartH / 2);
      const rScale = (m) => 18 + ((m - minMentions) / (maxMentions - minMentions + 1)) * 28;

      // Threshold positions
      const thresholdX = xScale(freqThreshold);
      const thresholdY = yScale(0);

      // Draw quadrant backgrounds
      // Top-left: PRIORITIES (high impact negative, high frequency)
      ctx.fillStyle = QUADRANT_COLORS.priorities.bg;
      ctx.fillRect(margin.left, margin.top, thresholdX - margin.left, thresholdY - margin.top);

      // Top-right: EMERGING (high impact negative, low frequency)
      ctx.fillStyle = QUADRANT_COLORS.emerging.bg;
      ctx.fillRect(thresholdX, margin.top, margin.left + chartW - thresholdX, thresholdY - margin.top);

      // Bottom-left: STRENGTHS (positive impact, high frequency)
      ctx.fillStyle = QUADRANT_COLORS.strengths.bg;
      ctx.fillRect(margin.left, thresholdY, thresholdX - margin.left, margin.top + chartH - thresholdY);

      // Bottom-right: NEUTRAL (positive impact, low frequency)
      ctx.fillStyle = QUADRANT_COLORS.neutral.bg;
      ctx.fillRect(thresholdX, thresholdY, margin.left + chartW - thresholdX, margin.top + chartH - thresholdY);

      // Draw dashed threshold lines
      ctx.setLineDash([6, 4]);
      ctx.strokeStyle = '#d1d5db';
      ctx.lineWidth = 1;

      // Vertical threshold line
      ctx.beginPath();
      ctx.moveTo(thresholdX, margin.top);
      ctx.lineTo(thresholdX, margin.top + chartH);
      ctx.stroke();

      // Horizontal threshold line (impact = 0)
      ctx.beginPath();
      ctx.moveTo(margin.left, thresholdY);
      ctx.lineTo(margin.left + chartW, thresholdY);
      ctx.stroke();

      ctx.setLineDash([]);

      // Draw quadrant labels
      ctx.font = 'bold 12px Inter, Arial, sans-serif';
      ctx.textAlign = 'left';

      ctx.fillStyle = QUADRANT_COLORS.priorities.labelColor;
      ctx.fillText('PRIORITÉS', margin.left + 10, margin.top + 22);

      ctx.textAlign = 'right';
      ctx.fillStyle = QUADRANT_COLORS.emerging.labelColor;
      ctx.fillText('SIGNAUX ÉMERGENTS', margin.left + chartW - 10, margin.top + 22);

      ctx.textAlign = 'left';
      ctx.fillStyle = QUADRANT_COLORS.strengths.labelColor;
      ctx.fillText('FORCES', margin.left + 10, margin.top + chartH - 10);

      ctx.textAlign = 'right';
      ctx.fillStyle = QUADRANT_COLORS.neutral.labelColor;
      ctx.fillText('NEUTRE', margin.left + chartW - 10, margin.top + chartH - 10);

      // Draw axes
      ctx.strokeStyle = '#e5e7eb';
      ctx.lineWidth = 1;

      // X axis line
      ctx.beginPath();
      ctx.moveTo(margin.left, margin.top + chartH);
      ctx.lineTo(margin.left + chartW, margin.top + chartH);
      ctx.stroke();

      // Y axis line
      ctx.beginPath();
      ctx.moveTo(margin.left, margin.top);
      ctx.lineTo(margin.left, margin.top + chartH);
      ctx.stroke();

      // Axis labels
      ctx.fillStyle = '#6b7280';
      ctx.font = '12px Inter, Arial, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('Fréquence →', margin.left + chartW / 2, height - 10);

      ctx.save();
      ctx.translate(16, margin.top + chartH / 2);
      ctx.rotate(-Math.PI / 2);
      ctx.textAlign = 'center';
      ctx.fillText('Impact →', 0, 0);
      ctx.restore();

      // Draw bubbles
      this.bubbles = [];
      themes.forEach(theme => {
        const x = xScale(theme.frequency);
        const y = yScale(theme.impact);
        const r = rScale(theme.mentions);
        const color = QUADRANT_COLORS[theme.quadrant]?.bubble || '#9ca3af';

        // Bubble
        ctx.beginPath();
        ctx.arc(x, y, r, 0, Math.PI * 2);
        ctx.fillStyle = color + 'cc'; // slightly transparent
        ctx.fill();

        // Label inside bubble
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 11px Inter, Arial, sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';

        // Word-wrap label inside bubble
        const words = theme.label.split(' ');
        if (words.length <= 2 && ctx.measureText(theme.label).width < r * 1.6) {
          ctx.fillText(theme.label, x, y);
        } else {
          // Split into two lines
          const mid = Math.ceil(words.length / 2);
          const line1 = words.slice(0, mid).join(' ');
          const line2 = words.slice(mid).join(' ');
          ctx.fillText(line1, x, y - 7);
          ctx.fillText(line2, x, y + 7);
        }

        // Store bubble info for hover detection
        this.bubbles.push({
          x, y, r, theme
        });
      });
    },

    setupEvents() {
      const canvas = this.$refs.canvas;
      if (!canvas) return;
      canvas.addEventListener('mousemove', this.handleMouseMove);
      canvas.addEventListener('mouseleave', this.handleMouseLeave);
    },

    handleMouseMove(event) {
      const canvas = this.$refs.canvas;
      const rect = canvas.getBoundingClientRect();
      const mx = event.clientX - rect.left;
      const my = event.clientY - rect.top;

      const hovered = this.bubbles.find(b => {
        const dx = mx - b.x;
        const dy = my - b.y;
        return Math.sqrt(dx * dx + dy * dy) <= b.r;
      });

      if (hovered) {
        this.hoveredTheme = hovered.theme;
        this.tooltipX = mx + 15;
        this.tooltipY = my - 15;
        canvas.style.cursor = 'pointer';
      } else {
        this.hoveredTheme = null;
        canvas.style.cursor = 'default';
      }
    },

    handleMouseLeave() {
      this.hoveredTheme = null;
    },

    formatNumber(value) {
      if (!value) return '0';
      return new Intl.NumberFormat('fr-FR').format(value);
    }
  },
  beforeUnmount() {
    const canvas = this.$refs.canvas;
    if (canvas) {
      canvas.removeEventListener('mousemove', this.handleMouseMove);
      canvas.removeEventListener('mouseleave', this.handleMouseLeave);
    }
  }
};
</script>

