<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-lg font-semibold text-gray-900">Liste des verbatims</h3>
      <div class="flex items-center space-x-3">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Rechercher..."
          class="px-3 py-2 border border-gray-300 rounded-md text-sm w-64"
        />
        <select
          v-model="sortBy"
          class="px-3 py-2 border border-gray-300 rounded-md text-sm"
        >
          <option value="date">Trier par date</option>
          <option value="sentiment">Trier par sentiment</option>
        </select>
      </div>
    </div>
    <div v-if="loading" class="h-64 flex items-center justify-center">
      <div class="text-gray-400">Chargement...</div>
    </div>
    <div v-else>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Date
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Type
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Extrait
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Sentiment
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Thèmes
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr
              v-for="verbatim in paginatedVerbatims"
              :key="verbatim.id"
              @click="selectVerbatim(verbatim)"
              class="hover:bg-gray-50 cursor-pointer"
            >
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ formatDate(verbatim.date) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <span class="px-2 py-1 text-xs font-medium rounded-full"
                      :class="verbatim.type === 'email' ? 'bg-blue-100 text-blue-800' : 'bg-purple-100 text-purple-800'">
                  {{ verbatim.type === 'email' ? 'Email' : 'Appel' }}
                </span>
              </td>
              <td class="px-6 py-4 text-sm text-gray-900">
                {{ verbatim.extract.substring(0, 150) }}{{ verbatim.extract.length > 150 ? '...' : '' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  class="px-2 py-1 text-xs font-medium rounded-full"
                  :class="getSentimentBadgeClass(verbatim.sentiment)"
                >
                  {{ getSentimentLabel(verbatim.sentiment) }}
                </span>
              </td>
              <td class="px-6 py-4 text-sm text-gray-500">
                <div class="flex flex-wrap gap-1">
                  <span
                    v-for="theme in verbatim.themes.slice(0, 2)"
                    :key="theme"
                    class="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded"
                  >
                    {{ theme }}
                  </span>
                  <span v-if="verbatim.themes.length > 2" class="px-2 py-1 text-xs text-gray-400">
                    +{{ verbatim.themes.length - 2 }}
                  </span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="filteredAndSortedVerbatims.length === 0" class="text-center py-8 text-gray-500">
        Aucun verbatim trouvé
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="flex items-center justify-between border-t border-gray-200 pt-4 mt-4">
        <div class="text-sm text-gray-600">
          Affichage de {{ paginationStart }} à {{ paginationEnd }} sur {{ filteredAndSortedVerbatims.length }} résultats
        </div>
        <div class="flex items-center space-x-2">
          <button
            @click="goToPage(1)"
            :disabled="currentPage === 1"
            class="px-3 py-1.5 text-sm border border-gray-300 rounded-md transition-colors"
            :class="currentPage === 1 ? 'text-gray-300 cursor-not-allowed' : 'text-gray-700 hover:bg-gray-50'"
          >
            «
          </button>
          <button
            @click="goToPage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="px-3 py-1.5 text-sm border border-gray-300 rounded-md transition-colors"
            :class="currentPage === 1 ? 'text-gray-300 cursor-not-allowed' : 'text-gray-700 hover:bg-gray-50'"
          >
            ‹
          </button>

          <template v-for="page in visiblePages" :key="page">
            <span v-if="page === '...'" class="px-2 text-gray-400">...</span>
            <button
              v-else
              @click="goToPage(page)"
              class="px-3 py-1.5 text-sm border rounded-md transition-colors"
              :class="page === currentPage
                ? 'bg-blue-600 text-white border-blue-600'
                : 'border-gray-300 text-gray-700 hover:bg-gray-50'"
            >
              {{ page }}
            </button>
          </template>

          <button
            @click="goToPage(currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="px-3 py-1.5 text-sm border border-gray-300 rounded-md transition-colors"
            :class="currentPage === totalPages ? 'text-gray-300 cursor-not-allowed' : 'text-gray-700 hover:bg-gray-50'"
          >
            ›
          </button>
          <button
            @click="goToPage(totalPages)"
            :disabled="currentPage === totalPages"
            class="px-3 py-1.5 text-sm border border-gray-300 rounded-md transition-colors"
            :class="currentPage === totalPages ? 'text-gray-300 cursor-not-allowed' : 'text-gray-700 hover:bg-gray-50'"
          >
            »
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { dataService } from '../services/dataService';

export default {
  name: 'VerbatimList',
  data() {
    return {
      loading: true,
      verbatims: [],
      searchQuery: '',
      sortBy: 'date',
      selectedVerbatim: null,
      currentPage: 1,
      perPage: 50
    };
  },
  watch: {
    searchQuery() {
      this.currentPage = 1;
    },
    sortBy() {
      this.currentPage = 1;
    }
  },
  computed: {
    filteredAndSortedVerbatims() {
      let filtered = this.verbatims;

      // Filter by search query
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(v =>
          v.extract.toLowerCase().includes(query) ||
          v.fullText.toLowerCase().includes(query) ||
          v.themes.some(t => t.toLowerCase().includes(query))
        );
      }

      // Sort
      if (this.sortBy === 'date') {
        filtered = [...filtered].sort((a, b) => new Date(b.date) - new Date(a.date));
      } else if (this.sortBy === 'sentiment') {
        const sentimentOrder = { positive: 1, neutral: 2, negative: 3 };
        filtered = [...filtered].sort((a, b) => sentimentOrder[a.sentiment] - sentimentOrder[b.sentiment]);
      }

      return filtered;
    },
    totalPages() {
      return Math.ceil(this.filteredAndSortedVerbatims.length / this.perPage);
    },
    paginatedVerbatims() {
      const start = (this.currentPage - 1) * this.perPage;
      const end = start + this.perPage;
      return this.filteredAndSortedVerbatims.slice(start, end);
    },
    paginationStart() {
      if (this.filteredAndSortedVerbatims.length === 0) return 0;
      return (this.currentPage - 1) * this.perPage + 1;
    },
    paginationEnd() {
      return Math.min(this.currentPage * this.perPage, this.filteredAndSortedVerbatims.length);
    },
    visiblePages() {
      const pages = [];
      const total = this.totalPages;
      const current = this.currentPage;

      if (total <= 7) {
        for (let i = 1; i <= total; i++) pages.push(i);
      } else {
        pages.push(1);
        if (current > 3) pages.push('...');
        const start = Math.max(2, current - 1);
        const end = Math.min(total - 1, current + 1);
        for (let i = start; i <= end; i++) pages.push(i);
        if (current < total - 2) pages.push('...');
        pages.push(total);
      }
      return pages;
    }
  },
  async mounted() {
    await this.loadData();
  },
  methods: {
    async loadData() {
      try {
        this.verbatims = await dataService.getConversations();
        this.loading = false;
      } catch (error) {
        console.error('Error loading conversations:', error);
        this.loading = false;
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric' });
    },
    getSentimentLabel(sentiment) {
      const labels = {
        positive: 'Positif',
        neutral: 'Neutre',
        negative: 'Négatif'
      };
      return labels[sentiment] || sentiment;
    },
    getSentimentBadgeClass(sentiment) {
      const classes = {
        positive: 'bg-green-100 text-green-800',
        neutral: 'bg-yellow-100 text-yellow-800',
        negative: 'bg-red-100 text-red-800'
      };
      return classes[sentiment] || 'bg-gray-100 text-gray-800';
    },
    goToPage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
    selectVerbatim(verbatim) {
      this.selectedVerbatim = verbatim;
      this.$emit('verbatim-selected', verbatim);
    }
  }
};
</script>

