import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    // This forces Vite to only ever load ONE copy of React, fixing the hook error
    dedupe: ['react', 'react-dom']
  }
})