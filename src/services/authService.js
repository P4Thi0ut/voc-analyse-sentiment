/**
 * Authentication service
 * Validates user credentials against environment variables
 */

export const authService = {
  /**
   * Authenticate user with username and password
   * @param {string} username - The username
   * @param {string} password - The password
   * @returns {Promise<boolean>} - True if credentials are valid
   */
  async login(username, password) {
    // Get credentials from environment variables
    const validUsername = import.meta.env.VITE_LOGIN_USERNAME;
    const validPassword = import.meta.env.VITE_LOGIN_PASSWORD;

    // Check if credentials are configured
    if (!validUsername || !validPassword) {
      console.error('Login credentials not configured in .env file');
      return false;
    }

    // Validate credentials
    if (username === validUsername && password === validPassword) {
      return true;
    }

    return false;
  },

  /**
   * Check if user is authenticated
   * @returns {boolean} - True if user is authenticated
   */
  isAuthenticated() {
    return localStorage.getItem('isAuthenticated') === 'true';
  },

  /**
   * Logout user
   */
  logout() {
    localStorage.removeItem('isAuthenticated');
  }
};

