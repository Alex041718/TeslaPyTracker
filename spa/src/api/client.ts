import axios from 'axios';
import type { AxiosResponse, AxiosError } from 'axios';
import { API_BASE_URL } from '../config/env.config';

export const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Intercepteur pour gérer les erreurs globalement
apiClient.interceptors.response.use(
    (response: AxiosResponse) => response,
    (error: AxiosError) => {
        if (error.response) {
            // Erreur avec réponse du serveur
            console.error('Erreur API:', error.response.data);
        } else if (error.request) {
            // Erreur sans réponse du serveur
            console.error('Erreur réseau:', error.request);
        } else {
            // Autre type d'erreur
            console.error('Erreur:', error.message);
        }
        return Promise.reject(error);
    }
);