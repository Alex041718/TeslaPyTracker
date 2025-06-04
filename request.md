Pour obtenir le prix le plus bas pour chaque capture temporelle
```mongo
db["stock_history_model3"].aggregate([
  // Déplie le tableau results pour accéder à chaque véhicule
  { $unwind: "$data.results" },
  
  // Groupe par timestamp (la date de capture) et trouve le prix minimum
  { $group: {
    _id: "$timestamp",
    minPrice: { $min: "$data.results.Price" },
    year: { $first: "$year" }
  }},
  
  // Trie par date de capture
  { $sort: { _id: 1 } }
])
````
