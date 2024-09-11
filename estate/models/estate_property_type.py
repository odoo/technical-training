from datetime import datetime, timedelta
from odoo import fields, models
from odoo import api

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Properties type"
    _order = "name"

    name = fields.Char(string="Name", required=True, help="Property type")

    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties', help='Type properties')

    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string="Offers")

    offer_count = fields.Integer(string="Offers Count", default=0, compute="_compute_offer_count")


    # constraints
    _sql_constraints = [
        ('unique_property_type_name', 'UNIQUE(name)', 'A property cannot have duplicate types.'),
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for property_type_record in self:
            property_type_record.offer_count = len(property_type_record.offer_ids)
    
    def get_offer_count(self):
        # Recuperar valor
        return self.offer_count