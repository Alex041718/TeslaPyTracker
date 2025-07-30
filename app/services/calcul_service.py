import pymongo
from app import mongo

class CalculService:
    @staticmethod
    def get_min_price_per_capture(year=None, version=None, paint=None):
        """
        Retourne le prix le plus bas pour chaque capture temporelle (timestamp),
        avec possibilité de filtrer par année, version et couleur de peinture.
        
        Si aucune année n'est spécifiée, utilise une normalisation des timestamps
        pour regrouper les captures proches dans le temps issues de différentes années.
        """
        # Utilise un pipeline optimisé :
        # - $match en premier (indexable)
        # - $project pour ne garder que les champs utiles
        # - $unwind pour déplier les résultats
        # - $match pour filtrer par couleur si spécifiée
        # - $group pour le min
        # - $sort à la fin
        pipeline = []
        
        # Préfiltrage pour améliorer les performances
        if year is not None or version is not None:
            match = {}
            if year is not None:
                match['year'] = year
            if version is not None:
                match['version'] = version
            pipeline.append({'$match': match})
        
        # Première partie du pipeline commune
        pipeline += [
            { '$project': {
                'timestamp': 1,
                'year': 1,
                'version': 1,
                'price': '$data.results.Price',
                'results': '$data.results',
                # Ajout d'un champ normalisé pour les timestamps (arrondi à l'heure)
                'timestamp_normalized': {
                    '$dateToString': {
                        'format': '%Y-%m-%d %H:00:00',
                        'date': '$timestamp'
                    }
                }
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
        
        # Définir la clé de regroupement en fonction de si une année est spécifiée
        group_id = '$timestamp' if year is not None else '$timestamp_normalized'
        
        # Finalisation du pipeline avec le regroupement approprié
        pipeline += [
            { '$group': {
                '_id': group_id,
                'minPrice': { '$min': '$results.Price' },
                'year': { '$first': '$year' },
                'vin': { '$first': '$results.VIN' },
                'version': { '$first': '$version' },
                'paint': { '$first': { '$arrayElemAt': ['$results.PAINT', 0] } },
                'odometer': { '$first': '$results.Odometer' },
                'timestamp_original': { '$first': '$timestamp' } # Conserve le timestamp original
            }},
            { '$sort': { '_id': 1 } }
        ]
        results = list(mongo.db.stock_history_model3.aggregate(pipeline))
        
        # Traitement des résultats pour rétablir un timestamp approprié
        for doc in results:
            # Si on a utilisé le timestamp normalisé, on utilise le timestamp original
            if year is None and 'timestamp_original' in doc:
                doc['timestamp'] = doc.pop('timestamp_original')
            else:
                # Sinon on utilise la clé _id comme avant
                doc['timestamp'] = doc.pop('_id')
                
            # Supprimer le champ timestamp_original s'il existe
            if 'timestamp_original' in doc:
                doc.pop('timestamp_original')
                
        return results
