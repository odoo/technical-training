# -*- coding: utf-8 -*-

from odoo import models, fields


class City(models.Model):
    """ Adds fields for general information about the kindgon """

    _name = 'kingdom.city'
    _description = "Stats for each major city"

    name = fields.Char(required=True)
    citizen_count = fields.Integer(string="Number of citizen")
    production_food = fields.Float(string="Food production", help="Number of tons of production")
