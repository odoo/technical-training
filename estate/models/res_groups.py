from odoo import fields, models

class ResGroups(models.Model):
    _inherit = 'res.groups'
    max_amount = fields.Float(string="Training Max Price (Approval)") #Création d'un nouveau champ dans la DB de type Float

