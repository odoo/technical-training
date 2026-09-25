from odoo import models, fields

class EstateAccount(models.Model):
    _name = "estate.account"
    _description = "Estate Account Integration"

    # Basic Information
    name = fields.Char(required=True)
    description = fields.Text()
