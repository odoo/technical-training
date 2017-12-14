# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _

class Price(models.Model):
    _name = 'library.price'

    name = fields.Char('Name',)
    duration = fields.Float('Duration in days',)
    price = fields.Float('Price',)
    type = fields.Selection([('time', 'Based on time'), ('one', 'Oneshot'),], default="time")
