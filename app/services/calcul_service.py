import pymongo
from app import mongo

class CalculService:
    @staticmethod
    def get_min_price_per_capture(year=None, version=None, paint=None):
        """
        Retourne le prix le plus bas pour chaque capture temporelle (timestamp),
        avec possibilité de filtrer par année, version et couleur de peinture.
        """
        # Utilise un pipeline optimisé :
        # - $match en premier (indexable)
        # - $project pour ne garder que les champs utiles
        # - $unwind pour déplier les résultats
        # - $match pour filtrer par couleur si spécifiée
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
                'results': '$data.results'
            }},
            { '$unwind': '$results' }
        ]
        
        # Ajout du filtre par couleur après l'unwind si spécifié
        if paint is not None:
            pipeline.append({
                '$match': {
                    'results.PAINT.0': paint
                }
            })
        
        pipeline += [
            { '$group': {
                '_id': '$timestamp',
                'minPrice': { '$min': '$results.Price' },
                'year': { '$first': '$year' },
                'vin': { '$first': '$results.VIN' },  # Ajout du VIN dans le regroupement
                'version': { '$first': '$version' },
                'paint': { '$first': { '$arrayElemAt': ['$results.PAINT', 0] } },  # Extraction de la première couleur du tableau
                'odometer': { '$first': '$results.Odometer' }  # Ajout du champ Odometer
            }},
            { '$sort': { '_id': 1 } }
        ]
        results = list(mongo.db.stock_history_model3.aggregate(pipeline))
        for doc in results:
            doc['timestamp'] = doc.pop('_id')
        return results
