from marshmallow import Schema, fields

class GraphPointSchema(Schema):
    timestamp = fields.Integer(required=True, description="Timestamp en millisecondes")
    price = fields.Float(required=True, description="Prix en euros")
    text = fields.String(description="Texte descriptif du point")
    vin = fields.String(description="VIN du véhicule (optionnel)")
    paint = fields.String(description="Couleur de la peinture (optionnel)")
    odometer = fields.Integer(description="Kilométrage du véhicule (optionnel)")

class MetaSchema(Schema):
    total_points = fields.Integer(required=True, description="Nombre total de points avant normalisation")
    normalized_points = fields.Integer(required=True, description="Nombre de points après normalisation")
    year = fields.Integer(description="Année filtrée (optionnel)")
    version = fields.String(description="Version Tesla filtrée (optionnel)")

class LinksSchema(Schema):
    self = fields.String(required=True, description="URL de la ressource courante")
    next = fields.String(description="URL de la page suivante")
    prev = fields.String(description="URL de la page précédente")

class GraphDataSchema(Schema):
    meta = fields.Nested(MetaSchema, required=True)
    data = fields.List(fields.Nested(GraphPointSchema), required=True)
    links = fields.Nested(LinksSchema, required=True)

class GraphQueryArgsSchema(Schema):
    year = fields.Integer(description="Année à filtrer")
    version = fields.String(description="Version Tesla à filtrer")
    paint = fields.String(description="Couleur de peinture à filtrer")
    points = fields.Integer(description="Nombre de points souhaités", load_default=25)
    time_range = fields.String(description="Plage temporelle (all, 1y, 6m, 3m, 1m, 1w)", load_default="all")