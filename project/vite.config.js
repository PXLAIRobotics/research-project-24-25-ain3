import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  base: '/research-project-24-25-ain3/',
  plugins: [
    vue()
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  test: {
    environment: 'jsdom', // Zorg ervoor dat de testomgeving 'jsdom' is, zodat window.location en andere DOM-functies goed werken
    globals: true, // Maakt globale toegang mogelijk tot 'describe', 'it', etc.
    coverage: {
      reporter: ['text', 'json', 'html'], // Optioneel voor testdekking
    },
  },
})
