# -*- coding: utf-8 -*-
from odoo import fields, models


class Company(models.Model):
    _inherit = 'res.company'

    king = fields.Many2one('res.users', help="May his reign be long")
    true_heir_throne = fields.Many2one('res.users', string="True Heir to the Throne", help="Nobody can be aware of this!")
