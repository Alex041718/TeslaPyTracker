from marshmallow import Schema, fields, post_load
from app.dto.sales_dto import SalePointDTO
from marshmallow.validate import Range

class SalePointSchema(Schema):
    date = fields.DateTime()
    sales_count = fields.Integer(validate=Range(min=0))
    sold_vins = fields.List(fields.String())

    @post_load
    def make_sale_point(self, data, **kwargs):
        return SalePointDTO(**data)

class SaleDataSchema(Schema):
    data = fields.List(fields.Nested(SalePointSchema))