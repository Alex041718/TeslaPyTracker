from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.services.sales_service import SalesService
from app.schemas.sales_schema import SaleDataSchema
from marshmallow import Schema, fields

sales_bp = Blueprint(
    'sales',
    __name__,
    url_prefix='/api/sales',
    description='Opérations sur les ventes de Tesla'
)

class SalesQueryArgsSchema(Schema):
    year = fields.Integer(required=False)
    version = fields.String(required=False)

@sales_bp.route('/daily')
class DailySalesGraph(MethodView):
    @sales_bp.response(200, SaleDataSchema)
    @sales_bp.arguments(SalesQueryArgsSchema, location='query')
    def get(self, args):
        """Obtenir les ventes journalières de Tesla

        Retourne un graphique des ventes journalières, 
        avec possibilité de filtrer par année et version.
        """
        try:
            year = args.get('year')
            version = args.get('version')
            
            sales_service = SalesService()
            daily_sales = sales_service.calculate_daily_sales(year, version)
            
            return {"data": daily_sales}
        
        except Exception as e:
            abort(500, message=str(e))