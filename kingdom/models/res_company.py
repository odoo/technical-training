# -*- coding: utf-8 -*-

from odoo import models, fields


class Company(models.Model):
    """ Adds fields for general information about the kindgon """

    _inherit = 'res.company'

    king = fields.Many2one('res.users', help="May his reign be long")
    true_heir_throne = fields.Many2one('res.users', string="True Heir to the Throne",
        help="Nobody can be aware of this!")
