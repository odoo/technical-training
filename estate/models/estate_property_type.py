from odoo import models, fields, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"
    
    _sql_constraints = [
        ('check_name_unique', 'UNIQUE(name)', 'Property type name must be unique'),
    ]

    # Basic Information
    sequence = fields.Integer(default=10)
    name = fields.Char(required=True)
    
    # Relationships
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(compute='_compute_offer_count', string='Offers Count')
    
    # Computed Methods
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
    