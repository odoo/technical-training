from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(string="Sequence", default=10)

    _sql_constraints = [
        ("estate_property_type_name_uniq", "unique(name)", "Property type name must be unique."),
    ]
    
    # Inline list: related properties
    property_ids = fields.One2many(
        comodel_name="estate.property",
        inverse_name="property_type_id",
        string="Properties",
    )

    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_type_id",
        string="Offers",
    )
    offer_count = fields.Integer(string="Offers", compute="_compute_offer_count")

    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)
    
