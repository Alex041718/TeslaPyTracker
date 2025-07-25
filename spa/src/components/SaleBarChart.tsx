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

  return (
    <div className="sales-bar-chart">
      <h2></h2>
      <ResponsiveContainer height={300}>
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
            formatter={(value) => [value, 'Ventes']}
          />
          <Legend />
          <Bar dataKey="sales_count" fill={color} name="Nombre de ventes" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default SaleBarChart;