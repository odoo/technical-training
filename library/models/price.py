# -*- coding: utf-8 -*-
from odoo import models, fields


class Price(models.Model):
    _name = 'library.price'
    _description = 'Price'

    name = fields.Char()
    duration = fields.Float('Duration in days')
    price = fields.Float()
    type = fields.Selection([('time', 'Based on time'), ('one', 'Oneshot')], default="time")
