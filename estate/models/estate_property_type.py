from odoo import api, models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "name"

    # SQL Constraints
    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 
         'The property type name must be unique.'),
    ]

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1, help="Used to order types")
    property_ids = fields.One2many(
        "estate.property",
        "property_type_id",
        string="Properties"
    )

    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_type_id",
        string="Offers"
    )
    offer_count = fields.Integer(
        string="Offers Count",
        compute="_compute_offer_count"
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)