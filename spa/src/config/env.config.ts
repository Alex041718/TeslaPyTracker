const host = import.meta.env.HOST || 'localhost';
const port = import.meta.env.FLASK_PORT || '5555';

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || `http://${host}:${port}`;