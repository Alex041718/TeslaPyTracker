import { useEffect, useState, type ChangeEvent } from 'react';
import type { SelectChangeEvent } from '@mui/material/Select';
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
  Select,
  MenuItem,
  FormControl,
  InputLabel,
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
  initialYear?: number;
  initialVersion?: string;
  initialPaint?: string;
  initialPoints?: number;
  color?: string; // Couleur personnalisable
}

const MinPriceChart = ({color,initialYear,initialVersion,initialPaint,initialPoints}:MinPriceChartProps) => {
  const [formData, setFormData] = useState<GraphQueryParams>({
    year: initialYear,
    version: initialVersion ?? 'M3RWD',
    paint: initialPaint,
    points: initialPoints ?? 100,
  });

  const handleInputChange = (field: keyof GraphQueryParams) =>
    (e: SelectChangeEvent<string | number> | ChangeEvent<HTMLInputElement>) => {
      let value: string | number | undefined;
      
      if (field === 'version' || field === 'paint') {
        value = e.target.value || undefined;
      } else if (field === 'year') {
        value = e.target.value ? Number(e.target.value) : undefined;
      } else {
        value = Number(e.target.value);
      }
      
      setFormData(prev => ({ ...prev, [field]: value }));
    };

  return (
    <Card className='min-price-chart'>
      <CardHeader
        title={`Tesla - Prix minimum ${formData.year ? formData.year : 'toutes années'}`}
        subheader={`Visualisez l'évolution des prix minimum pour ${formData.version} ${formData.year ? `en ${formData.year}` : 'sur toutes les années'}`}
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
          <FormControl size="small" sx={{ minWidth: 120 }}>
            <InputLabel>Année</InputLabel>
            <Select
              value={formData.year || ''}
              label="Année"
              onChange={handleInputChange('year')}
              displayEmpty
            >
              <MenuItem value="">Toutes années</MenuItem>
              {[2020, 2021, 2022, 2023, 2024].map((year) => (
                <MenuItem key={year} value={year}>
                  {year}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          
          <FormControl size="small" sx={{ minWidth: 120 }}>
            <InputLabel>Version</InputLabel>
            <Select
              value={formData.version}
              label="Version"
              onChange={handleInputChange('version')}
            >
              {['M3RWD', 'LRRWD', 'LRAWD', 'PAWD'].map((version) => (
                <MenuItem key={version} value={version}>
                  {version}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          
          <TextField
            label="Couleur"
            value={formData.paint || ''}
            onChange={handleInputChange('paint') as (e: ChangeEvent<HTMLInputElement>) => void}
            placeholder="Ex: WHITE, BLACK..."
            size="small"
            sx={{ maxWidth: '120px' }}
          />
          
          <TextField
            label="Points"
            type="number"
            value={formData.points}
            onChange={handleInputChange('points') as (e: ChangeEvent<HTMLInputElement>) => void}
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
