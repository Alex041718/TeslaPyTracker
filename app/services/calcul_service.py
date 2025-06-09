import pymongo
from app import mongo

class CalculService:
    @staticmethod
    def get_min_price_per_capture(year=None, version=None):
        """
        Retourne le prix le plus bas pour chaque capture temporelle (timestamp),
        avec possibilité de filtrer par année et version.
        """
        # Utilise un pipeline optimisé :
        # - $match en premier (indexable)
        # - $project pour ne garder que les champs utiles
        # - $unwind pour déplier les résultats
        # - $group pour le min
        # - $sort à la fin
        pipeline = []
        if year is not None or version is not None:
            match = {}
            if year is not None:
                match['year'] = year
            if version is not None:
                match['version'] = version
            pipeline.append({'$match': match})
        pipeline += [
            { '$project': {
                'timestamp': 1,
                'year': 1,
                'version': 1,
                'price': '$data.results.Price',
                'vin': '$data.results.VIN',  # Ajout du champ VIN
                'results': '$data.results'
            }},
            { '$unwind': '$results' },
            { '$group': {
                '_id': '$timestamp',
                'minPrice': { '$min': '$results.Price' },
                'year': { '$first': '$year' },
                'version': { '$first': '$version' }
            }},
            { '$sort': { '_id': 1 } }
        ]
        results = list(mongo.db.stock_history_model3.aggregate(pipeline))
        for doc in results:
            doc['timestamp'] = doc.pop('_id')
        return results
