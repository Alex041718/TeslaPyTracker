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
  Box,
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
    timeRange: 'all',
  });

  const handleInputChange = (field: keyof GraphQueryParams) =>
    (e: SelectChangeEvent<string | number> | ChangeEvent<HTMLInputElement>) => {
      let value: string | number | undefined;
      
      if (field === 'version' || field === 'paint' || field === 'timeRange') {
        value = e.target.value || undefined;
      } else if (field === 'year') {
        value = e.target.value ? Number(e.target.value) : undefined;
      } else {
        value = Number(e.target.value);
      }
      
      setFormData(prev => ({ ...prev, [field]: value }));
    };

  // Fonction pour générer un sous-titre dynamique
  const getSubheader = () => {
    let subheader = `Visualisez l'évolution des prix minimum pour ${formData.version}`;
    
    if (formData.year) {
      subheader += ` en ${formData.year}`;
    } else {
      subheader += ' sur toutes les années';
    }
    
    if (formData.timeRange && formData.timeRange !== 'all') {
      let period = '';
      switch(formData.timeRange) {
        case '1y': period = 'dernière année'; break;
        case '6m': period = 'derniers 6 mois'; break;
        case '3m': period = 'derniers 3 mois'; break;
        case '1m': period = 'dernier mois'; break;
        case '1w': period = 'dernière semaine'; break;
      }
      if (period) {
        subheader += ` (${period})`;
      }
    }
    
    return subheader;
  };

  return (
    <Card className='min-price-chart'>
      <CardHeader
        title={`Tesla - Prix minimum ${formData.year ? formData.year : 'toutes années'}`}
        subheader={getSubheader()}
        sx={{
          borderBottom: '1px solid #e0e0e0',
          padding: { xs: '16px 16px', sm: '16px 24px' },
          '& .MuiCardHeader-title': {
            fontSize: { xs: '1rem', sm: '1.2rem' },
            fontWeight: 600
          },
          '& .MuiCardHeader-subheader': {
            fontSize: { xs: '0.8rem', sm: '0.9rem' }
          }
        }}
      />
      <CardContent sx={{ p: { xs: 2, sm: 3 } }}>
        <Box sx={{ 
          backgroundColor: 'rgba(0, 0, 0, 0.02)', 
          borderRadius: 1, 
          p: { xs: 1.5, sm: 2 },
          mb: 3
        }}>
          {/* Première rangée: filtres principaux */}
          <Stack 
            direction={{ xs: 'column', sm: 'row' }} 
            spacing={2}
            sx={{ mb: 2 }}
          >
            <FormControl
              size="small"
              sx={{
                minWidth: { xs: '100%', sm: 120 },
                flex: { xs: '1', sm: '1' }
              }}
            >
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
            
            <FormControl
              size="small"
              sx={{
                minWidth: { xs: '100%', sm: 120 },
                flex: { xs: '1', sm: '1' }
              }}
            >
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
              sx={{
                flex: { xs: '1', sm: '1' }
              }}
            />
            
            <TextField
              label="Points"
              type="number"
              value={formData.points}
              onChange={handleInputChange('points') as (e: ChangeEvent<HTMLInputElement>) => void}
              inputProps={{ min: "1" }}
              size="small"
              sx={{
                flex: { xs: '1', sm: '1' }
              }}
            />
          </Stack>
          
          {/* Deuxième rangée: période */}
          <Box sx={{ 
            display: 'flex', 
            justifyContent: 'center',
            borderTop: '1px solid rgba(0, 0, 0, 0.06)',
            pt: 2
          }}>
            <Box sx={{ 
              display: 'flex', 
              alignItems: 'center',
              width: { xs: '100%', sm: '50%' }
            }}>
              <Box component="span" sx={{ 
                mr: 1, 
                color: 'text.secondary', 
                fontSize: '0.875rem',
                whiteSpace: 'nowrap'
              }}>
                Période:
              </Box>
              <FormControl
                fullWidth
                size="small"
              >
                <Select
                  value={formData.timeRange || 'all'}
                  onChange={handleInputChange('timeRange')}
                  displayEmpty
                  variant="outlined"
                >
                  <MenuItem value="all">Depuis toujours</MenuItem>
                  <MenuItem value="1y">1 an</MenuItem>
                  <MenuItem value="6m">6 mois</MenuItem>
                  <MenuItem value="3m">3 mois</MenuItem>
                  <MenuItem value="1m">1 mois</MenuItem>
                  <MenuItem value="1w">1 semaine</MenuItem>
                </Select>
              </FormControl>
            </Box>
          </Box>
        </Box>

        <ChartContainer color={color} params={formData} />
      </CardContent>
    </Card>
  );
};

export default MinPriceChart;
