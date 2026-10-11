import { defineConfig } from 'vite'

export default defineConfig({
  root: './ui',
  server: {
    host: true,
    allowedHosts: ['the-red-flag.onrender.com', '.onrender.com', 'localhost', '127.0.0.1']
  },
  preview: {
    host: '0.0.0.0',
    port: process.env.PORT ? parseInt(process.env.PORT) : 4173,
    allowedHosts: ['the-red-flag.onrender.com', '.onrender.com', 'localhost', '127.0.0.1']
  }
})
