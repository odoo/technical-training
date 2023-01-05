from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "The property tag model"
    _order = "tag_name"
    _rec_name = 'tag_name'
    
    
    tag_name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('name_uniq', 'UNIQUE (tag_name)',
         'The Tag name must be unique!')
    ]
