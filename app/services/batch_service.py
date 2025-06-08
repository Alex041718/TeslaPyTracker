from app.services.tesla_history_service import TeslaHistoryService
import time
import json
import os

class BatchService:
    def __init__(self):
        self.tesla_service = TeslaHistoryService()
        self.params = self.load_config()

    def load_config(self):
        """
        Charge la configuration du batch depuis le fichier JSON.
        Lève une exception si le fichier n'est pas trouvé ou est invalide.
        """
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'batch_config.json')
        
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                if 'batch_params' not in config:
                    raise KeyError("La clé 'batch_params' est manquante dans le fichier de configuration")
                return config['batch_params']
        except FileNotFoundError:
            raise FileNotFoundError(f"Le fichier de configuration n'a pas été trouvé: {config_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Le fichier de configuration contient du JSON invalide: {str(e)}")
        except KeyError as e:
            raise KeyError(f"Format de configuration invalide: {str(e)}")

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