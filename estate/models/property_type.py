from odoo import fields, models

class PropertyType(models.Model):
        _name = "estate.property.type"
        _description = "Property Type"

        name = fields.Char(required=True)
        description = fields.Text()
        active = fields.Boolean(default=True)