import { apiClient } from './client';
import type { GraphData } from '../dto/graph.dto';

/**
 * Paramètres requis pour la requête du graphique des prix minimum
 */
export interface GraphQueryParams {
    year?: number;     // Année à filtrer (optionnel - si non fourni, agrège toutes les années)
    version: string;   // Version Tesla à filtrer (obligatoire)
    paint?: string;    // Couleur de peinture à filtrer (optionnel)
    points: number;    // Nombre de points souhaités (obligatoire)
    timeRange?: string; // Plage temporelle (optionnel - 'all', '1y', '6m', '3m', '1m', '1w')
}

export const graphService = {
    /**
     * Récupère l'évolution du prix minimum des Tesla
     * @param params Paramètres de filtrage (version et points obligatoires, année optionnelle)
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
        if (!params.version || !params.points) {
            throw new Error('Les paramètres version et points sont obligatoires');
        }

        // Construction des paramètres de requête
        const queryParams: Record<string, string | number> = {
            version: params.version,
            points: params.points
        };

        // Ajout du paramètre year s'il est spécifié
        if (params.year) {
            queryParams.year = params.year;
        }

        // Ajout du paramètre paint s'il est spécifié
        if (params.paint) {
            queryParams.paint = params.paint;
        }
        
        // Ajout du paramètre timeRange s'il est spécifié
        if (params.timeRange) {
            queryParams.time_range = params.timeRange;
        }

        // Construction de l'URL avec les paramètres de requête
        const { data } = await apiClient.get<GraphData>('/api/graphs/min-price', {
            params: queryParams
        });
        
        // Conversion des timestamps en objets Date
        data.data = data.data.map(point => ({
            ...point,
            timestamp: new Date(point.timestamp)
        }));
        
        return data;
    }
};