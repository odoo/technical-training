from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char()

    # _sql_constraints = [
    #     ('check_name', 'CHECK(_name >= 0)', 'The Type Name should be unique.')
    # ]