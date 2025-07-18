import { useEffect, useState, type ChangeEvent } from 'react';
import { graphService, type GraphQueryParams } from '../api/graphService';
import type { GraphData } from '../dto/graph.dto';
import Chart from './Chart';
import './minPriceChart.scss';
import {
  Card,
  CardContent,
  CardHeader,
  TextField,
  Stack,
  Alert,
  AlertTitle,
} from '@mui/material';

const ChartContainer = ({ params, color }: { params: GraphQueryParams, color?:string }) => {
  const [graphData, setGraphData] = useState<GraphData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      setError(null);

      try {
        const data = await graphService.getMinPriceEvolution(params);
        setGraphData(data);
      } catch (err) {
        setError('Erreur lors du chargement des données');
        console.error('Erreur:', err);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [params]);

  if (loading) return <div>Chargement du graphique...</div>;
  if (error) return (
    <Alert severity="error" sx={{ mt: 3 }}>
      <AlertTitle>Erreur</AlertTitle>
      {error}
    </Alert>
  );
  if (!graphData) return null;

  return <Chart color={color} graphData={graphData} />;
};

interface MinPriceChartProps {
  initialYear: number;
  initialVersion?: string;
  initialPoints?: number;
  color?: string; // Couleur personnalisable
}

const MinPriceChart = ({color,initialYear,initialVersion,initialPoints}:MinPriceChartProps) => {
  const [formData, setFormData] = useState<GraphQueryParams>({
    year: initialYear ??2023,
    version: initialVersion ?? 'M3RWD',
    points: initialPoints ?? 100,
  });

  const handleInputChange = (field: keyof GraphQueryParams) => (e: ChangeEvent<HTMLInputElement>) => {
    const value = field === 'version' ? e.target.value : parseInt(e.target.value);
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <Card className='min-price-chart'>
      <CardHeader
        title= {`Tesla - Prix minimum ${formData.year}`}
        subheader={`Visualisez l'évolution des prix minimum pour ${formData.version} `}
        sx={{
          borderBottom: '1px solid #e0e0e0',
          '& .MuiCardHeader-title': {
            fontSize: '1.2rem',
            fontWeight: 600
          }
        }}
      />
      <CardContent sx={{ p: 3 }}>
        <Stack direction="row" spacing={2} sx={{
          mb: 3,
          p: 2,
          borderRadius: 1
        }}>
          <TextField
            label="Année"
            type="number"
            value={formData.year}
            onChange={handleInputChange('year')}
            size="small"
            sx={{ maxWidth: '100px' }}
          />
          
          <TextField
            label="Version"
            value={formData.version}
            onChange={handleInputChange('version')}
            size="small"
            sx={{ maxWidth: '100px' }}
          />
          
          <TextField
            label="Points"
            type="number"
            value={formData.points}
            onChange={handleInputChange('points')}
            inputProps={{ min: "1" }}
            size="small"
            sx={{ maxWidth: '100px' }}
          />
        </Stack>

        <ChartContainer color={color}  params={formData} />

        
      </CardContent>
    </Card>
  );
};

export default MinPriceChart;
