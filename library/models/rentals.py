# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _

class Rentals(models.Model):
    _name = 'library.rental'
    _description = 'Book rental'

    customer_id = fields.Many2one(
        'library.partner',
        'Customer',
    )
    book_id = fields.Many2one(
        'library.book',
        'Book',
    )
    rental_date =  fields.Date(string='Rental date',)
    return_date =  fields.Date(string='Return date',)
