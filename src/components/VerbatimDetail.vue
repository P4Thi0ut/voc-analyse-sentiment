<template>
  <div v-if="verbatim" class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mt-6">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-lg font-semibold text-gray-900">Détail du verbatim</h3>
      <button
        @click="close"
        class="text-gray-400 hover:text-gray-600"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- Main Content -->
      <div class="md:col-span-2">
        <div class="mb-4">
          <h4 class="text-sm font-medium text-gray-500 mb-2">Texte complet</h4>
          <div class="bg-gray-50 rounded-lg p-4 text-sm text-gray-900 whitespace-pre-wrap">
            {{ verbatim.fullText }}
          </div>
        </div>

        <div v-if="verbatim.feedbacks && verbatim.feedbacks.length > 0" class="mt-6">
          <h4 class="text-sm font-medium text-gray-500 mb-3">Points de feedback</h4>
          <div class="space-y-4">
            <div
              v-for="(feedback, index) in verbatim.feedbacks"
              :key="index"
              class="border border-gray-200 rounded-lg p-4"
            >
              <div class="mb-2">
                <p class="text-sm text-gray-700 font-medium">{{ feedback.feedback_point }}</p>
              </div>
              <div class="mb-3">
                <p class="text-sm text-gray-600 italic">"{{ feedback.text }}"</p>
              </div>
              <div v-if="feedback.tags && feedback.tags.length > 0" class="flex flex-wrap gap-2">
                <span
                  v-for="tag in feedback.tags"
                  :key="tag.id"
                  class="px-3 py-1 text-xs rounded-full font-medium"
                  :class="getTagClass(tag.sentiment)"
                >
                  {{ tag.label }}
                  <span class="ml-1 text-xs opacity-75">({{ tag.confidence_score }}/5)</span>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Metadata Sidebar -->
      <div class="md:col-span-1">
        <div class="bg-gray-50 rounded-lg p-4 space-y-4">
          <div>
            <h4 class="text-sm font-medium text-gray-500 mb-2">Métadonnées</h4>
            <dl class="space-y-2 text-sm">
              <div>
                <dt class="text-gray-500">Date</dt>
                <dd class="text-gray-900 font-medium">{{ formatDate(verbatim.date) }}</dd>
              </div>
              <div>
                <dt class="text-gray-500">Type</dt>
                <dd class="text-gray-900">
                  <span
                    class="px-2 py-1 text-xs font-medium rounded-full"
                    :class="verbatim.type === 'email' ? 'bg-blue-100 text-blue-800' : 'bg-purple-100 text-purple-800'"
                  >
                    {{ verbatim.type === 'email' ? 'Email' : 'Appel' }}
                  </span>
                </dd>
              </div>
              <div>
                <dt class="text-gray-500">Sentiment</dt>
                <dd class="text-gray-900">
                  <span
                    class="px-2 py-1 text-xs font-medium rounded-full"
                    :class="getSentimentBadgeClass(verbatim.sentiment)"
                  >
                    {{ getSentimentLabel(verbatim.sentiment) }}
                  </span>
                </dd>
              </div>
              <div v-if="verbatim.metadata">
                <template v-if="verbatim.metadata.agent_id">
                  <dt class="text-gray-500">Agent ID</dt>
                  <dd class="text-gray-900">{{ verbatim.metadata.agent_id }}</dd>
                </template>
                <template v-if="verbatim.metadata.duration">
                  <dt class="text-gray-500">Durée</dt>
                  <dd class="text-gray-900">{{ verbatim.metadata.duration }}</dd>
                </template>
                <template v-if="verbatim.metadata.site">
                  <dt class="text-gray-500">Site</dt>
                  <dd class="text-gray-900">{{ verbatim.metadata.site }}</dd>
                </template>
              </div>
            </dl>
          </div>

          <div v-if="verbatim.themes && verbatim.themes.length > 0">
            <h4 class="text-sm font-medium text-gray-500 mb-2">Thèmes</h4>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="theme in verbatim.themes"
                :key="theme"
                class="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded"
              >
                {{ theme }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'VerbatimDetail',
  props: {
    verbatim: {
      type: Object,
      default: null
    }
  },
  methods: {
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
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
    getTagClass(sentiment) {
      // sentiment: 0 = negative, 1 = positive (from the data structure)
      if (sentiment === 1) {
        return 'bg-green-100 text-green-800';
      } else if (sentiment === 0) {
        return 'bg-red-100 text-red-800';
      } else {
        return 'bg-yellow-100 text-yellow-800';
      }
    },
    close() {
      this.$emit('close');
    }
  }
};
</script>

