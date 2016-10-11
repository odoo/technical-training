# -*- coding: utf-8 -*-

from odoo import models, fields


class Users(models.Model):
    """ Adds fields for general information about the kindgon """

    _inherit = 'res.users'

    city = fields.Many2one('kingdom.city')
