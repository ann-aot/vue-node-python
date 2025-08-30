import { defineConfig } from 'vite';
import { fileURLToPath, URL } from 'node:url';
import vue from '@vitejs/plugin-vue';
import vuetify from 'vite-plugin-vuetify';
// @ts-expect-error: No type definitions available for vite-plugin-eslint
import eslintPlugin from 'vite-plugin-eslint';

export default defineConfig({
  plugins: [vue(), vuetify({ autoImport: true }), eslintPlugin()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    host: true,
    port: 5173,
    allowedHosts: ['.gitpod.io', 'localhost'],
  },
  preview: {
    host: true,
    port: 5173,
  },
});
