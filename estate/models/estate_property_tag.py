from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name desc"


    name = fields.Char(required=True)
    color = fields.Integer("Color Index")


_sql_constraints = [
        ("unique_name", "UNIQUE(name)",
        'Tag name should be unique.')
    ]