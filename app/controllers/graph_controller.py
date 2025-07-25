from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.services.graph_service import GraphService
from app.schemas.graph_schema import GraphDataSchema, GraphQueryArgsSchema
from datetime import datetime

graph_bp = Blueprint(
    'graphs',
    __name__,
    url_prefix='/api/graphs',
    description='Opérations sur les graphes'
)

@graph_bp.route('/min-price')
class MinPriceGraph(MethodView):
    @graph_bp.response(200, GraphDataSchema)
    @graph_bp.arguments(GraphQueryArgsSchema, location='query')
    def get(self, args):
        """Obtenir l'évolution du prix minimum
        
        Retourne un graphe montrant l'évolution du prix minimum des Tesla
        à travers le temps, avec possibilité de filtrer par année et version.
        Les données sont normalisées pour limiter le nombre de points.
        """
        try:
            year = args.get('year')
            version = args.get('version')
            paint = args.get('paint')
            points = args.get('points', 25)
            
            graph_data = GraphService.get_min_price_evolution(year, version, paint, points)
            
            # Conversion des datetime en timestamps pour la sérialisation JSON
            for point in graph_data.data:
                point.timestamp = int(point.timestamp.timestamp() * 1000)
            
            return graph_data
            
        except Exception as e:
            abort(500, message=str(e))