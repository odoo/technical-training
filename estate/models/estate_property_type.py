from odoo import models, fields, api

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "The property type model"
    _order = "sequence"
    _rec_name = 'property_type'
    
    # Fields

    property_type = fields.Char()
    
    # Relational Fields
    
    property_ids = fields.One2many('estate.property', 'property_type_id')
    
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    
    # Compute Fields
    
    offer_count = fields.Integer(compute='_check_offer_count')

    sequence = fields.Integer('Sequence', default=1,
                              help="Used to order stages. Lower is better.")

    _sql_constraints = [
        ('type_unique', 'UNIQUE (property_type)',
         'The Property type must be unique!')
    ]
    
    @api.depends('offer_ids')
    def _check_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    # def view_offers(self):
    #     self.ensure_one()
    #     return {
    #         "type": "ir.actions.act_window",
    #         "name": "Property Offers",
    #         "res_model": "estate.property.offer",
    #         "view_mode": "tree,form"
    #         # "domain": [("change_id", "=", self.id)],
    #         # "context": "{'create': False}"
    #     }

    
