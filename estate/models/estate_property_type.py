from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char()

    _sql_constraints = [
        ('check_name_unique', 'UNIQUE(_name)', 'The name must be unique!')
    ]