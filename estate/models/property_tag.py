from odoo import fields, models

class PropertyTag(models.Model):
        _name = "estate.property.tag"
        _description = "Property Tag"

        name = fields.Char(required=True)
        description = fields.Text()
        active = fields.Boolean(default=True)