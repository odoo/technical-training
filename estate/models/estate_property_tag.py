from datetime import datetime, timedelta
from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Properties Tag"
    _order = "name"

    name = fields.Char(string="Name", required=True, help="Tag name")
    color = fields.Integer(string="Color", help="Tag color")

    # constraints
    _sql_constraints = [
        ('unique_property_tag_name', 'UNIQUE(name)', 'A property cannot have duplicate tags.'),
    ]