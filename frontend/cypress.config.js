import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:5173', // Vue dev server URL
    supportFile: 'cypress/support/e2e.js',
    specPattern: 'cypress/e2e/**/*.cy.js',
    setupNodeEvents() {
      // implement node event listeners here if needed
      // removed unused 'on' and 'config' parameters
    },
  },
});
