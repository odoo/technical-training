from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char()

    # _sql_constraints = [
    #     ('check_name', 'CHECK(_name >= 0)', 'The Tag Name should be unique.')
    # ]