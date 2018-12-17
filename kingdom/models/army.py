# -*- coding: utf-8 -*-
from odoo import fields, models


class Army(models.Model):
    _name = 'kingdom.army'
    _description = "Armies"

    commander = fields.Many2one('res.users')
    infantry_count = fields.Integer(string="Number of infantry units")
    cavalry_count = fields.Integer(string="Number of cavalry units")
