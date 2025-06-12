from typing import List, Optional
from datetime import datetime
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
                              points: int = 25) -> GraphDataDTO:
        """
        Génère les données pour le graphe d'évolution des prix minimums.
        """
        # Récupération des données brutes
        raw_data = CalculService.get_min_price_per_capture(year, version)
        
        # Normalisation des points
        normalized_points = GraphService.normalize_points(raw_data, points)
        
        # Construction du DTO
        return GraphDataDTO(
            meta=MetaDTO(
                total_points=len(raw_data),
                normalized_points=len(normalized_points),
                year=year,
                version=version
            ),
            data=normalized_points,
            links=LinksDTO(
                self=f"/api/graphs/min-price?year={year if year else ''}&version={version if version else ''}"
            )
        )