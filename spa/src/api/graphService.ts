import { apiClient } from './client';
import type { GraphData } from '../dto/graph.dto';

/**
 * Paramètres requis pour la requête du graphique des prix minimum
 */
export interface GraphQueryParams {
    year: number;      // Année à filtrer (obligatoire)
    version: string;   // Version Tesla à filtrer (obligatoire)
    points: number;    // Nombre de points souhaités (obligatoire)
}

export const graphService = {
    /**
     * Récupère l'évolution du prix minimum des Tesla
     * @param params Paramètres de filtrage obligatoires (année, version, nombre de points)
     * @returns Promise<GraphData> Les données du graphique
     * @example
     * const data = await graphService.getMinPriceEvolution({
     *   year: 2023,
     *   version: 'M3RWD',
     *   points: 25
     * });
     */
    getMinPriceEvolution: async (params: GraphQueryParams): Promise<GraphData> => {
        // Vérification des paramètres obligatoires
        if (!params.year || !params.version || !params.points) {
            throw new Error('Les paramètres year, version et points sont obligatoires');
        }

        // Construction de l'URL avec les paramètres de requête
        const { data } = await apiClient.get<GraphData>('/api/graphs/min-price', {
            params: {
                year: params.year,
                version: params.version,
                points: params.points
            }
        });
        
        // Conversion des timestamps en objets Date
        data.data = data.data.map(point => ({
            ...point,
            timestamp: new Date(point.timestamp)
        }));
        
        return data;
    }
};