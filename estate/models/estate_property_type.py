from odoo import models, fields

# this is creating a table
class RealEstate(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    # this is creating fields in the table
    name = fields.Char(copy=False, required=True)