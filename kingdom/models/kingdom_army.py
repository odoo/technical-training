# -*- coding: utf-8 -*-

from odoo import models, fields


class Army(models.Model):
    """ Adds fields for general information about the kindgon """

    _name = 'kingdom.army'
    _description = "Armies"

    commander = fields.Many2one('res.users')
    infantry_count = fields.Integer(string="Number of infantry units")
    cavalry_count = fields.Integer(string="Number of cavalry units")
