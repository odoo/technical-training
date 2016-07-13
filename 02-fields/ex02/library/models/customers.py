# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions, _

class Partner(models.Model):
    _name = 'library.partner'

    name = fields.Char(string='Name')
    email = fields.Char(string='Email')
    address = fields.Text(string='Address')
    partner_type = fields.Selection([('customer', 'Customer'), ('author', 'Author')], default="customer")
    rental_ids = fields.One2many(
        'library.rental',
        'customer_id',
        string='Rentals',)

