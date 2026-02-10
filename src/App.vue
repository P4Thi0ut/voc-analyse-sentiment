<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Top Header -->
    <header class="bg-white border-b border-gray-200">
      <div class="px-6 py-4">
        <div class="flex items-center justify-between">
          <!-- Logo and App Name -->
          <div class="flex items-center space-x-3" style="width: 110px; height: 32px;">
            <img src="/img/icons-v2/logo.svg" alt="Logo" class="h-8 w-8 flex-shrink-0" />
            <img src="/img/icons-v2/deskea.svg" alt="Deskea" class="h-5 flex-shrink-0" style="max-width: 100%;" />
          </div>
          
        </div>
        
        <!-- Secondary Navigation and Filters -->
        <div class="mt-4 flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <!-- Filter Dropdowns -->
            <select class="px-3 py-2 border border-gray-300 rounded-md text-sm bg-white">
              <option>DPD</option>
            </select>
            <select class="px-3 py-2 border border-gray-300 rounded-md text-sm bg-white">
              <option>Toutes les équipes</option>
              <option>ADM</option>
              <option>DPD</option>
              <option>OCC</option>
            </select>
            <select class="px-3 py-2 border border-gray-300 rounded-md text-sm bg-white">
              <option>Tous les projets</option>
              <option>Desti ADM</option>
              <option>Desti OCC</option>
              <option>Expe DPD</option>
            </select>
            <input type="text" placeholder="1 Feb 2026 - 10 Feb 2026" 
                   class="px-3 py-2 border border-gray-300 rounded-md text-sm w-48">
            <select class="px-3 py-2 border border-gray-300 rounded-md text-sm bg-white">
              <option>Extension, Application</option>
            </select>
            <button class="px-4 py-2 bg-purple-600 text-white rounded-md text-sm font-medium hover:bg-purple-700 flex items-center space-x-2">
              <span>Exporter</span>
            </button>
          </div>
        </div>
      </div>
    </header>

    <div class="flex">
      <!-- Left Sidebar -->
      <aside class="w-64 bg-white border-r border-gray-200 min-h-screen flex flex-col">
        <nav class="p-4 space-y-6 flex-1">
          <div>
            <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">Analyse</h3>
            <ul class="space-y-2">
              <li>
                <a href="#" class="flex items-center space-x-2 px-3 py-2 bg-blue-50 text-blue-600 rounded-md font-medium">
                  <span>Dashboard</span>
                </a>
              </li>
            </ul>
          </div>
          
          <div>
            <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">Évaluation</h3>
            <ul class="space-y-2">
              <li>
                <a href="#" @click.prevent="openConversations" class="flex items-center space-x-2 px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-md">
                  <span>Conversations</span>
                </a>
              </li>
              <li>
                <a href="#" @click.prevent="openDashboard" class="flex items-center space-x-2 px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-md">
                  <span>Tableau de bord</span>
                </a>
              </li>
            </ul>
          </div>
        </nav>
        
        <div class="p-4 border-t border-gray-200">
          <ul class="space-y-2">
            <li>
              <a href="#" class="flex items-center space-x-2 px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-md">
                <span>Paramètres</span>
              </a>
            </li>
            <li>
              <a href="#" class="flex items-center space-x-2 px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-md">
                <span>Documentation</span>
              </a>
            </li>
            <li>
              <a href="#" class="flex items-center space-x-2 px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-md">
                <span>Se déconnecter</span>
              </a>
            </li>
          </ul>
        </div>
      </aside>

      <!-- Main Content -->
      <main class="flex-1 p-6">
        <div class="mb-6">
          <h1 class="text-2xl font-bold text-gray-900">Analyse de sentiment</h1>
          <p class="text-gray-600 mt-1">Vue d'ensemble des conversations agent-client</p>
        </div>

        <!-- KPI Cards Section -->
        <KPICards />

        <!-- Row 1: Word Cloud full width -->
        <div class="mb-6">
          <WordCloudChart @keyword-clicked="handleKeywordClick" />
        </div>

        <!-- Row 2: Donut + Top Themes -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <SentimentDonut />
          <TopThemesChart />
        </div>

        <!-- Row 2: Timeline + Prioritization Matrix -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <TimelineChart />
          <PrioritizationMatrix />
        </div>

        <!-- Row 3: Verbatim list and detail -->
        <div>
          <VerbatimList @verbatim-selected="handleVerbatimSelected" />
          <VerbatimDetail :verbatim="selectedVerbatim" @close="selectedVerbatim = null" />
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import KPICards from './components/KPICards.vue';
import SentimentDonut from './components/SentimentDonut.vue';
import WordCloudChart from './components/WordCloudChart.vue';
import TimelineChart from './components/TimelineChart.vue';
import TopThemesChart from './components/TopThemesChart.vue';
import PrioritizationMatrix from './components/PrioritizationMatrix.vue';
import VerbatimList from './components/VerbatimList.vue';
import VerbatimDetail from './components/VerbatimDetail.vue';

export default {
  name: 'App',
  components: {
    KPICards,
    SentimentDonut,
    WordCloudChart,
    TimelineChart,
    TopThemesChart,
    PrioritizationMatrix,
    VerbatimList,
    VerbatimDetail
  },
  data() {
    return {
      selectedVerbatim: null
    };
  },
  methods: {
    handleKeywordClick(keyword) {
      // Could filter verbatims by keyword here
      console.log('Keyword clicked:', keyword);
    },
    handleVerbatimSelected(verbatim) {
      this.selectedVerbatim = verbatim;
    },
    openConversations() {
      window.open('https://app.gramaide.com/conversations-list', '_blank');
    },
    openDashboard() {
      window.open('https://app.gramaide.com/dashboard/evaluate', '_blank');
    }
  }
}
</script>

