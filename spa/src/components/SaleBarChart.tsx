import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import type { SalePoint } from '../dto/sales.dto.ts';
import { fetchDailySales, type BarQueryParams } from '../api/salesService.ts';
import './sale-bar-chart.scss';


interface SaleBarChartProps {
  params: BarQueryParams
  color?: string;
}

const SaleBarChart = ({ params, color = '#2192D9' }: SaleBarChartProps) => {
  const [salesData, setSalesData] = useState<SalePoint[]>([]);

  useEffect(() => {
    const loadSalesData = async () => {
      try {
        const response = await fetchDailySales(params);
        setSalesData(response.data);
      } catch (error) {
        console.error('Erreur lors du chargement des données de ventes', error);
      }
    };

    loadSalesData();
  }, [params]);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return `${date.getDate()}/${date.getMonth() + 1}`;
  };

  // Calculer la somme totale des ventes
  const totalSales = salesData.reduce((total, item) => total + item.sales_count, 0);
  
  return (
    <div className="sales-bar-chart">
      <h2>Statistiques de ventes - {params.version || 'Toutes versions'}</h2>
      <div className="sales-bar-chart__container">
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={salesData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="date"
              tickFormatter={formatDate}
              interval="preserveStartEnd"
            />
            <YAxis />
            <Tooltip
              labelFormatter={(label) => formatDate(label)}
              formatter={(value) => [`${value}`, 'Ventes']}
            />
            <Legend />
            <Bar
              dataKey="sales_count"
              fill={color}
              name="Nombre de ventes"
              radius={[4, 4, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
      
      {salesData.length > 0 && (
        <div className="sales-bar-chart__total">
          <p>Total des ventes: <strong>{totalSales}</strong></p>
        </div>
      )}
    </div>
  );
};

export default SaleBarChart;