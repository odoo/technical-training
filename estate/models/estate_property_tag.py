from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"

    # SQL Constraints
    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 
         'The property type name must be unique.'),
    ]

    name = fields.Char(required=True)
    color = fields.Integer()