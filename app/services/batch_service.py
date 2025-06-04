from app.services.tesla_history_service import TeslaHistoryService
import time

class BatchService:
    def __init__(self):
        self.tesla_service = TeslaHistoryService()
        self.params = [
            {'year': 2021, 'version': 'M3RWD'},
            {'year': 2022, 'version': 'M3RWD'},
            {'year': 2023, 'version': 'M3RWD'},
            {'year': 2024, 'version': 'M3RWD'},
        ]

    def fetch_and_store_multiple(self, params_list=None):
        if params_list is None:
            params_list = self.params
        results = []
        for params in params_list:
            year = params['year']
            version = params['version']
            inserted_id = self.tesla_service.fetch_and_store_stock_model3(year, version)
            results.append({
                'year': year,
                'version': version,
                'inserted_id': inserted_id
            })

            time.sleep(20)
            if inserted_id is None:
                print(f"Erreur lors de l'insertion pour {year} {version}.")
                continue
            else:
                print(f"Batch pour {year} {version} terminé, ID inséré: {inserted_id}")
        print("Tous les batches traités.")
        return results

# Exemple d'utilisation :
# params = [
#     {'year': 2022, 'version': 'M3WD'},
#     {'year': 2023, 'version': 'M3WD'}
# ]
# BatchService().fetch_and_store_multiple(params)