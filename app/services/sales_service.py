from typing import List, Dict, Optional
from datetime import datetime
from app import mongo
from pymongo import ASCENDING

class SalesService:
    def __init__(self):
        self.collection_m3 = mongo.db.stock_history_model3

    def calculate_daily_sales(self, year: Optional[int] = None, version: Optional[str] = None) -> List[Dict]:
        """
        Calcule les ventes journalières en comparant les stocks successifs.
        
        :param year: Année optionnelle pour filtrer
        :param version: Version optionnelle pour filtrer
        :return: Liste de ventes journalières
        """
        # Construction du pipeline d'agrégation
        pipeline = [
            # Filtrage optionnel par année et version
            {'$match': {k: v for k, v in {'version': version}.items() if v is not None}},
            
            # Trier par timestamp pour avoir un ordre chronologique
            {'$sort': {'timestamp': ASCENDING}},
            
            # Grouper par jour et année
            {'$group': {
                '_id': {
                    'year': {'$year': '$timestamp'},
                    'month': {'$month': '$timestamp'},
                    'day': {'$dayOfMonth': '$timestamp'}
                },
                'captures': {'$push': '$data.results.VIN'}
            }},
            
            # Trier les captures par jour
            {'$sort': {'_id.year': 1, '_id.month': 1, '_id.day': 1}}
        ]
        
        # Exécuter l'agrégation
        daily_captures = list(self.collection_m3.aggregate(pipeline))

        print(f"Daily captures: {daily_captures}")
        
        # Calculer les ventes en comparant les VINs entre captures successives dans un même jour
        daily_sales = []
        sold_vins_global = set()
        for day_data in daily_captures:
            captures = day_data['captures']
            sold_vins_day = set()
            
            # Comparer la première capture de la journée avec la dernière
            if len(captures) >= 2:
                first_vins = set(captures[0])
                last_vins = set(captures[-1])
                sold_vins = first_vins - last_vins

                # Ne compter que les VINs non encore vendus
                new_sold_vins = sold_vins - sold_vins_global
                sold_vins_day.update(new_sold_vins)
                sold_vins_global.update(new_sold_vins)

                # print(f"Date: {day_data['_id']['year']}-{day_data['_id']['month']:02d}-{day_data['_id']['day']:02d}")
                # print(f"First VINs ({len(first_vins)}): {sorted(first_vins)}")
                # print(f"Last VINs ({len(last_vins)}): {sorted(last_vins)}")
                # print(f"Sold VINs ({len(sold_vins)}): {sorted(sold_vins)}")
                # print(f"New Sold VINs (non comptés avant) ({len(new_sold_vins)}): {sorted(new_sold_vins)}")
                # print("----------------------------------------------------")
        
            sales_entry = {
                'date': datetime(
                    day_data['_id']['year'],
                    day_data['_id']['month'],
                    day_data['_id']['day']
                ),
                'sales_count': len(sold_vins_day),
                'sold_vins': list(sold_vins_day)
            }
            
            daily_sales.append(sales_entry)
        
        return daily_sales