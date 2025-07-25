import { apiClient } from './client';
import type { SalesData } from '../dto/sales.dto';

export interface BarQueryParams {
    year?: number;      // Année à filtrer (obligatoire)
    version: string;   // Version Tesla à filtrer (obligatoire)
}

export const fetchDailySales = async (params: BarQueryParams): Promise<SalesData> => {
    try {
        const response = await apiClient.get<SalesData>('/api/sales/daily', {
            params: { year: params.year, version: params.version }
        });
        return response.data;
    } catch (error) {
        console.error('Erreur lors de la récupération des ventes', error);
        throw error;
    }
};