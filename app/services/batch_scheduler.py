import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from apscheduler.schedulers.blocking import BlockingScheduler
from app import create_app, mongo
from app.services.batch_service import BatchService

def run_batch():
    print("Batch lancé...")
    results = BatchService().fetch_and_store_multiple()
    print("Résultats:", results)

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        scheduler = BlockingScheduler()
        # Lance le batch immédiatement au démarrage
        run_batch()
        # Puis planifie les exécutions suivantes à intervalle régulier
        scheduler.add_job(run_batch, 'interval', minutes=60)
        print("Batch scheduler démarré (toutes les 60 minutes)...")
        scheduler.start()
