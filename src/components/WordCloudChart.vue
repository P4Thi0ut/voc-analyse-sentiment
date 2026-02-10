<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
    <h3 class="text-lg font-semibold text-gray-900 mb-4">Nuage de mots thématique</h3>
    <div v-if="loading" class="h-64 flex items-center justify-center">
      <div class="text-gray-400">Chargement...</div>
    </div>
    <div v-else>
      <div class="relative flex items-center justify-center" style="min-height: 400px;">
        <canvas ref="canvas" class="w-full" style="max-width: 100%;"></canvas>
        <div
          v-if="hoveredKeyword"
          class="absolute bg-white border border-gray-300 rounded-lg shadow-lg p-3 z-10 pointer-events-none"
          :style="{ left: tooltipX + 'px', top: tooltipY + 'px' }"
        >
          <div class="font-semibold text-gray-900">{{ hoveredKeyword.value }}</div>
          <div class="text-sm text-gray-600 mt-1">Occurrences: {{ hoveredKeyword.count }}</div>
          <div class="text-sm text-gray-600">
            Positif: {{ getPercentage(hoveredKeyword.sentiment.positive, hoveredKeyword.count) }}%
          </div>
          <div class="text-sm text-gray-600">
            Neutre: {{ getPercentage(hoveredKeyword.sentiment.neutral, hoveredKeyword.count) }}%
          </div>
          <div class="text-sm text-gray-600">
            Négatif: {{ getPercentage(hoveredKeyword.sentiment.negative, hoveredKeyword.count) }}%
          </div>
        </div>
      </div>
      <!-- Legend -->
      <div class="mt-4 flex items-center justify-center space-x-6 pt-4 border-t border-gray-200">
        <div class="flex items-center space-x-2">
          <div class="w-4 h-4 rounded-full bg-green-500"></div>
          <span class="text-sm text-gray-600">≥ 70% positif</span>
        </div>
        <div class="flex items-center space-x-2">
          <div class="w-4 h-4 rounded-full bg-yellow-500"></div>
          <span class="text-sm text-gray-600">40-70% positif</span>
        </div>
        <div class="flex items-center space-x-2">
          <div class="w-4 h-4 rounded-full bg-red-500"></div>
          <span class="text-sm text-gray-600">&lt; 40% positif</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import cloud from 'd3-cloud';
import { scaleLinear } from 'd3-scale';
import { dataService } from '../services/dataService';

export default {
  name: 'WordCloudChart',
  data() {
    return {
      loading: true,
      keywords: [],
      hoveredKeyword: null,
      tooltipX: 0,
      tooltipY: 0,
      words: []
    };
  },
  async mounted() {
    await this.loadData();
    this.$nextTick(() => {
      this.setupEventListeners();
    });
  },
  methods: {
    async loadData() {
      try {
        this.keywords = await dataService.getWordCloud();
        this.loading = false;
        this.$nextTick(() => {
          this.renderWordCloud();
        });
      } catch (error) {
        console.error('Error loading word cloud:', error);
        this.loading = false;
      }
    },
    getSentimentColor(keyword) {
      const total = keyword.sentiment.positive + keyword.sentiment.neutral + keyword.sentiment.negative;
      const positiveRatio = keyword.sentiment.positive / total;
      
      if (positiveRatio >= 0.7) {
        return '#10b981'; // green-500
      } else if (positiveRatio >= 0.4) {
        return '#eab308'; // yellow-500
      } else {
        return '#ef4444'; // red-500
      }
    },
    getPercentage(value, total) {
      return total > 0 ? ((value / total) * 100).toFixed(1) : '0.0';
    },
    renderWordCloud() {
      if (!this.$refs.canvas || this.keywords.length === 0) return;

      const canvas = this.$refs.canvas;
      const ctx = canvas.getContext('2d');
      const width = canvas.parentElement.clientWidth - 48; // padding
      const height = 400;

      canvas.width = width;
      canvas.height = height;

      // Calculate font size range based on counts
      const counts = this.keywords.map(k => k.count);
      const minCount = Math.min(...counts);
      const maxCount = Math.max(...counts);
      const fontSizeScale = scaleLinear()
        .domain([minCount, maxCount])
        .range([14, 48]);

      const words = this.keywords.map(keyword => ({
        text: keyword.value,
        size: fontSizeScale(keyword.count),
        keyword: keyword
      }));

      cloud()
        .size([width, height])
        .words(words)
        .padding(5)
        .rotate(() => 0)
        .font('Arial')
        .fontSize(d => d.size)
        .on('end', (words) => {
          this.words = words;
          this.drawWords(ctx, words, width, height);
        })
        .start();
    },
    drawWords(ctx, words, width, height) {
      ctx.clearRect(0, 0, width, height);
      
      // Translate to center - d3-cloud positions words relative to center (0,0)
      ctx.save();
      ctx.translate(width / 2, height / 2);
      
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';

      words.forEach(word => {
        ctx.fillStyle = this.getSentimentColor(word.keyword);
        ctx.font = `${word.size}px Arial`;
        ctx.fillText(word.text, word.x, word.y);

        // Store word bounds for hover detection (in canvas coordinates)
        const metrics = ctx.measureText(word.text);
        word.bounds = {
          left: (width / 2) + word.x - metrics.width / 2,
          right: (width / 2) + word.x + metrics.width / 2,
          top: (height / 2) + word.y - word.size / 2,
          bottom: (height / 2) + word.y + word.size / 2
        };
      });
      
      ctx.restore();
    },
    handleMouseMove(event) {
      if (!this.$refs.canvas) return;

      const canvas = this.$refs.canvas;
      const rect = canvas.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;

      const hovered = this.words.find(word => {
        return x >= word.bounds.left && x <= word.bounds.right &&
               y >= word.bounds.top && y <= word.bounds.bottom;
      });

      if (hovered) {
        this.hoveredKeyword = hovered.keyword;
        this.tooltipX = event.clientX - rect.left + 10;
        this.tooltipY = event.clientY - rect.top - 10;
        canvas.style.cursor = 'pointer';
      } else {
        this.hoveredKeyword = null;
        canvas.style.cursor = 'default';
      }
    },
    handleClick(event) {
      if (this.hoveredKeyword) {
        // Emit event to filter verbatims by this keyword
        this.$emit('keyword-clicked', this.hoveredKeyword.value);
      }
    },
    setupEventListeners() {
      if (this.$refs.canvas) {
        this.$refs.canvas.addEventListener('mousemove', this.handleMouseMove);
        this.$refs.canvas.addEventListener('click', this.handleClick);
      }
    }
  },
  beforeUnmount() {
    if (this.$refs.canvas) {
      this.$refs.canvas.removeEventListener('mousemove', this.handleMouseMove);
      this.$refs.canvas.removeEventListener('click', this.handleClick);
    }
  }
};
</script>

