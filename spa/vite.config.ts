import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  
  const host = env.HOST || 'localhost'
  const port = env.FLASK_PORT || '5555'
  
  return {
    plugins: [react()],
    server: {
      host: host,
      allowedHosts: [host]
    },
    define: {
      'import.meta.env.VITE_API_BASE_URL': JSON.stringify(env.VITE_API_BASE_URL || `http://${host}:${port}`)
    }
  }
})
