// Ce script initialise l'utilisateur et la base pour MongoDB, adapté à votre .env

db.createUser({ // doit être synchro avec .env
  user: "flasktesla",
  pwd: "alexPass",
  roles: [
    {
      role: "readWrite",
      db: "flaskapp"
    }
  ]
});

// Création de la collection pour historiser les stocks de voitures avec validation JSON Schema (optionnel)
db = db.getSiblingDB("flaskapp");
db.createCollection("stock_history_model3", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["timestamp", "year", "data"],
      properties: {
        timestamp: {
          bsonType: "date",
          description: "Date de l'historisation"
        },
        year: {
          bsonType: "int",
          description: "Année du stock historisé"
        },
        version: {
          bsonType: "string",
          description: "Version de la voiture ex M3WD"
        },
        data: {
          bsonType: "object",
          description: "Le JSON brut du stock de voitures"
        }
      }
    }
  }
});
