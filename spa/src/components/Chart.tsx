import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import type { GraphData } from '../dto/graph.dto';
import './Chart.scss';

interface ChartProps {
  graphData: GraphData;
  // color?: string; // Suppression de la duplication
  color?: string; // Ajout de la prop color
}

const Chart = ({ graphData, color = "#8884d8" }: ChartProps) => {
  // Calcul des valeurs min et max avec une marge de 1000€
  const prices = graphData.data.map(item => item.price);
  const minPrice = Math.min(...prices) - 1000;
  const maxPrice = Math.max(...prices) + 1000;
  return (
    <div className="chart">
      <ResponsiveContainer  height={200}>
        <AreaChart
          data={graphData.data}
          margin={{
            top: 10,
            right: 30,
            left: 0,
            bottom: 0,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="timestamp"
            tickFormatter={(value) => new Date(value).toLocaleDateString()}
          />
          <YAxis
            domain={[minPrice, maxPrice]}
            tickFormatter={(value) => `${value.toLocaleString()} €`}
          />
          <Tooltip
            labelFormatter={(value) => new Date(value).toLocaleString()}
            formatter={(value: number) => [`${value.toLocaleString()} €`, 'Prix']}
          />
          <Area
            type="monotone"
            dataKey="price"
            stroke={color}
            fill={color}
            fillOpacity={0.3}
          />
        </AreaChart>
      </ResponsiveContainer>

      <div className="card-footer">
        <div className="card-footer__stats">
          <div className="card-footer__stats__info">
            Version: {graphData.meta.version}
          </div>
          <div className="card-footer__stats__info">
            <span className='card-footer__stats__info__value'>{graphData.data[graphData.data.length -1].price} €</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chart;