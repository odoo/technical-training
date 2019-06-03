# -*- coding: utf-8 -*-
from odoo import fields, models, api, exceptions


class Rentals(models.Model):
    _name = 'library.rental'
    _description = 'Book rental'

    customer_id = fields.Many2one('library.partner', string='Customer', required=True)
    bookcopy_id = fields.Many2one('library.book_copy', string='Book', required=True)

    book_name = fields.Char(related='bookcopy_id.name')
    customer_name = fields.Char(related='customer_id.name')

    rental_date = fields.Date()
    return_date = fields.Date()

    address = fields.Char(related='customer_id.address')
    mail = fields.Char(related='customer_id.mail')

    publisher_id = fields.Many2one(related='bookcopy_id.publisher_id')
    author_ids = fields.Many2many(related='bookcopy_id.author_ids')
    date_published = fields.Date(related='bookcopy_id.date_published')
    isbn = fields.Char(related='bookcopy_id.isbn')


