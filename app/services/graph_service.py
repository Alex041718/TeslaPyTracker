from typing import List, Optional
from datetime import datetime, timedelta
from app.dto.graph_dto import GraphPointDTO, GraphDataDTO, MetaDTO, LinksDTO
from app.services.calcul_service import CalculService
import numpy as np

class GraphService:
    @staticmethod
    def normalize_points(points: List[dict], target_points: int = 25) -> List[GraphPointDTO]:
        """
        Normalise une liste de points pour réduire leur nombre tout en conservant
        les tendances importantes.
        """
        if len(points) <= target_points:
            return [
                GraphPointDTO(
                    timestamp=point['timestamp'],
                    price=point['minPrice'],
                    text=f"Version: {point.get('version', 'N/A')}",
                    vin=point.get('vin', None),  # Ajout du VIN
                    paint=point.get('paint', None),  # Ajout du champ Paint
                    odometer=point.get('odometer', None)  # Ajout du champ Odometer
                ) for point in points
            ]

        # Calcul des indices pour l'échantillonnage
        indices = np.linspace(0, len(points) - 1, target_points, dtype=int)
        
        normalized_points = []
        for idx in indices:
            point = points[idx]
            normalized_points.append(
                GraphPointDTO(
                    timestamp=point['timestamp'],
                    price=point['minPrice'],
                    text=f"Version: {point.get('version', 'N/A')}",
                    vin=point.get('vin', None),  # Ajout du VIN
                    paint=point.get('paint', None),  # Ajout du champ Paint
                    odometer=point.get('odometer', None)  # Ajout du champ Odometer
                )
            )
        
        return normalized_points

    @staticmethod
    def get_min_price_evolution(year: Optional[int] = None,
                              version: Optional[str] = None,
                              paint: Optional[str] = None,
                              points: int = 25,
                              time_range: str = 'all') -> GraphDataDTO:
        """
        Génère les données pour le graphe d'évolution des prix minimums.
        
        Args:
            year: Année à filtrer (optionnel)
            version: Version Tesla à filtrer (obligatoire)
            paint: Couleur de peinture à filtrer (optionnel)
            points: Nombre de points souhaités (obligatoire)
            time_range: Plage temporelle (all, 1y, 6m, 3m, 1m, 1w)
        """
        # Récupération des données brutes
        raw_data = CalculService.get_min_price_per_capture(year, version, paint)
        
        # Filtrage par plage temporelle
        if time_range != 'all' and raw_data:
            now = datetime.now()
            start_date = None
            
            if time_range == '1y':
                start_date = now - timedelta(days=365)
            elif time_range == '6m':
                start_date = now - timedelta(days=180)
            elif time_range == '3m':
                start_date = now - timedelta(days=90)
            elif time_range == '1m':
                start_date = now - timedelta(days=30)
            elif time_range == '1w':
                start_date = now - timedelta(days=7)
            
            if start_date:
                raw_data = [point for point in raw_data if point['timestamp'] >= start_date]
        
        # Normalisation des points
        normalized_points = GraphService.normalize_points(raw_data, points)
        
        # Construction du DTO
        return GraphDataDTO(
            meta=MetaDTO(
                total_points=len(raw_data),
                normalized_points=len(normalized_points),
                year=year,
                version=version,
                time_range=time_range
            ),
            data=normalized_points,
            links=LinksDTO(
                self=f"/api/graphs/min-price?year={year if year else ''}&version={version if version else ''}&paint={paint if paint else ''}&time_range={time_range}"
            )
        )