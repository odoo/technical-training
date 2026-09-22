from odoo import models, fields

class BakkerKoekenTags(models.Model):
    _name = "bakker_koeken_tags"
    _description = "Tags voor bakker koeken"
    _order = "name asc"
    

    name = fields.Char(string="Tag naam", required=True)
    color = fields.Integer(string="Kleur", default=1)