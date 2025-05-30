import requests
from datetime import datetime
from flask import current_app
from app import mongo
import os
import json

class TeslaHistoryService:
    def __init__(self):
        self.collection_m3 = mongo.db.stock_history_model3

    def fetch_and_store_stock_model3(self, year):
        # Préparation des paramètres pour l'API Tesla
        params_dict = {
            "query": {
                "model": "m3",
                "condition": "used",
                "options": {
                    "TRIM": ["M3RWD"],
                    "Year": [str(year)]
                },
                "arrangeby": "Price",
                "order": "asc",
                "market": "FR",
                "language": "fr",
                "super_region": "north america",
                "lng": -1.6744,
                "lat": 48.11,
                "zip": "35200",
                "range": 0,
                "region": "FR"
            },
            "offset": 0,
            "count": 24,
            "outsideOffset": 0,
            "outsideSearch": False,
            "isFalconDeliverySelectionEnabled": False,
            "version": None
        }
        query_str = json.dumps(params_dict)
        api_url = f'https://www.tesla.com/inventory/api/v4/inventory-results?query={requests.utils.quote(query_str)}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0',
            'Accept': '*/*',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Connection': 'keep-alive',
            'Referer': 'https://www.tesla.com/fr_FR/inventory/used/m3?TRIM=M3RWD&Year={year}&arrangeby=plh&zip=35200&range=0',
        }
        try:
            response = requests.get(api_url, headers=headers, timeout=90)
            print(response)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            current_app.logger.error(f"Erreur lors de l'appel API Tesla: {e}")
            return None

        # Prépare le document avec timestamp et année
        document = {
            'timestamp': datetime.utcnow(),
            'year': year,
            'data': data
        }
        # Insère dans la collection
        result = self.collection_m3.insert_one(document)
        return str(result.inserted_id)
