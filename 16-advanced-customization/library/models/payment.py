# -*- coding: utf-8 -*-
from odoo import models, fields


class Payment(models.Model):
    _name = 'library.payment'

    date = fields.Date(string='Date', required=True, default=lambda self: fields.Date.today())
    amount = fields.Float('Amount')
    customer_id = fields.Many2one('res.partner', 'Customer', domain=[('customer', '=', True)])
