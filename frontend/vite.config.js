import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss()
  ],
  server: {
    proxy: {
      '/bursary': 'http://localhost:5000', 
      //to re-configure the default Vite server (5173) to default Flask server (5000) 
    },
  },
})