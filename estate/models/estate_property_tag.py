from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")

    _sql_constraints = [
        ("estate_property_tag_name_uniq", "unique(name)", "Property tag name must be unique."),
    ]
