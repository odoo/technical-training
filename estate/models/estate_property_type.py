from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char()
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(string='Offer Count', compute='_compute_offer_count')

    _sql_constraints = [
        ('check_name_unique', 'UNIQUE(name)', 'The name must be unique!')
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
