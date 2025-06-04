from flask import Blueprint, jsonify, request
from app.services.tesla_history_service import TeslaHistoryService

bp = Blueprint('tesla_history', __name__, url_prefix='/tesla-history')

@bp.route('/model3/<int:year>/<string:version>', methods=['POST', 'GET'])
def fetch_and_store_model3(year,version):
    if request.method == 'GET':
        return jsonify({"message": "Route OK (GET)", "year": year}), 200
    service = TeslaHistoryService()
    inserted_id = service.fetch_and_store_stock_model3(year,version)
    if inserted_id:
        return jsonify({"status": "success", "inserted_id": inserted_id}), 201
    else:
        return jsonify({"status": "error", "message": "Erreur lors de l'appel ou de l'insertion"}), 500
