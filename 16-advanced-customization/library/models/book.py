# -*- coding: utf-8 -*-
from odoo import models, fields


class Book(models.Model):
    _inherit = 'product.product'

    author_ids = fields.Many2many(
        comodel_name="res.partner",
        string="Authors",
        domain=[('author', '=', True)],
    )
    edition_date = fields.Date(string='Edition date',)
    isbn = fields.Char(string='ISBN')
    publisher_id = fields.Many2one(
        'res.partner',
        string='Publisher',
        domain=[('publisher', '=', True)],
    )
    rental_ids = fields.One2many(
        'library.rental',
        'book_id',
        string='Rentals')
    book = fields.Boolean('is a book', default=False)
    book_state = fields.Selection(
        [('available', 'Available'), ('rented', 'Rented'), ('lost', 'Lost')],
        default="available",
    )
    acquisition_year = fields.Integer(string='Acquisition Year')
    acquisition_price = fields.Float('Acquisition Price')
