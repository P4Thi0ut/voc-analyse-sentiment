<template>
  <div class="min-h-screen flex">
    <!-- Left Section - Logo Display -->
    <div class="hidden md:flex md:w-2/3 bg-gray-200 items-center justify-center">
      <div class="text-center">
        <h1 class="text-6xl font-bold">
          <span class="text-indigo-700">desk</span>
          <span class="text-teal-500">ea</span>
        </h1>
      </div>
    </div>

    <!-- Right Section - Login Form -->
    <div class="w-full md:w-1/3 bg-white flex items-center justify-center p-8">
      <div class="w-full max-w-md">
        <!-- Small Logo -->
        <div class="mb-8 text-center">
          <h2 class="text-2xl font-bold text-gray-400 mb-2">
            <span class="text-gray-300">desk</span><span class="text-gray-300">ea</span>
          </h2>
        </div>

        <!-- Title -->
        <h1 class="text-3xl font-bold text-gray-800 mb-2">S'identifier</h1>
        <p class="text-gray-600 mb-8">Bienvenue à nouveau sur votre compte.</p>

        <!-- Error Message -->
        <div v-if="errorMessage" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-md text-red-700 text-sm">
          {{ errorMessage }}
        </div>

        <!-- Login Form -->
        <form @submit.prevent="handleLogin" class="space-y-4">
          <!-- Username Field -->
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <input
              v-model="username"
              type="text"
              placeholder="Utilisateur"
              class="w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent"
              required
            />
          </div>

          <!-- Password Field -->
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <input
              v-model="password"
              type="password"
              placeholder="Mot de passe"
              class="w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent"
              required
            />
          </div>

          <!-- Login Button -->
          <button
            type="submit"
            :disabled="isLoading"
            class="w-full py-3 bg-teal-500 hover:bg-teal-600 text-white font-medium rounded-lg transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="!isLoading">Se connecter</span>
            <span v-else>Connexion...</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { authService } from '../services/authService';

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '',
      isLoading: false
    };
  },
  methods: {
    async handleLogin() {
      this.errorMessage = '';
      this.isLoading = true;

      try {
        const isValid = await authService.login(this.username, this.password);
        
        if (isValid) {
          // Store authentication state
          localStorage.setItem('isAuthenticated', 'true');
          // Redirect to dashboard
          this.$router.push('/dashboard');
        } else {
          this.errorMessage = 'Nom d\'utilisateur ou mot de passe incorrect.';
        }
      } catch (error) {
        this.errorMessage = 'Une erreur est survenue lors de la connexion.';
        console.error('Login error:', error);
      } finally {
        this.isLoading = false;
      }
    }
  }
};
</script>

