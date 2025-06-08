import { useState } from 'react';
import type { FormEvent } from 'react';
import { graphService, type GraphQueryParams } from './api/graphService';
import type { GraphData } from './dto/graph.dto';

const App = () => {
  const [graphData, setGraphData] = useState<GraphData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const [formData, setFormData] = useState<GraphQueryParams>({
    year: 2023,
    version: 'M3RWD',
    points: 25
  });

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const data = await graphService.getMinPriceEvolution(formData);
      setGraphData(data);
    } catch (err) {
      setError('Erreur lors du chargement des données');
      console.error('Erreur:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div>Chargement...</div>;
  }

  return (
    <>
      <h1>Tesla Tracker</h1>
      <p>Application de suivi de véhicule Tesla</p>
      
      <form onSubmit={handleSubmit} className="graph-form">
        <div>
          <label htmlFor="year">Année:</label>
          <input
            type="number"
            id="year"
            value={formData.year}
            onChange={(e) => setFormData(prev => ({ ...prev, year: parseInt(e.target.value) }))}
            required
          />
        </div>

        <div>
          <label htmlFor="version">Version:</label>
          <input
            type="text"
            id="version"
            value={formData.version}
            onChange={(e) => setFormData(prev => ({ ...prev, version: e.target.value }))}
            required
          />
        </div>

        <div>
          <label htmlFor="points">Nombre de points:</label>
          <input
            type="number"
            id="points"
            value={formData.points}
            onChange={(e) => setFormData(prev => ({ ...prev, points: parseInt(e.target.value) }))}
            min="1"
            required
          />
        </div>

        <button type="submit">Générer le graphique</button>
      </form>

      {error && <div className="error">Erreur: {error}</div>}

      {graphData && (
        <div className="graph-data">
          <h2>Prix minimum</h2>
          <p>Année: {graphData.meta.year}</p>
          <p>Version: {graphData.meta.version}</p>
          <p>Nombre total de points: {graphData.meta.totalPoints}</p>
          <p>Points normalisés: {graphData.meta.normalizedPoints}</p>
          {/* Ici, vous pourrez ajouter un composant de graphique pour visualiser les données */}
        </div>
      )}
    </>
  );
};

export default App;
