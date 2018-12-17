# -*- coding: utf-8 -*-
from odoo import fields, models


class Books(models.Model):
    _name = 'library.book'
    _description = 'Book'

    name = fields.Char(string='Title')

    author_ids = fields.Many2many("res.partner", string="Authors")
    edition_date = fields.Date()
    isbn = fields.Char(string='ISBN', unique=True)
    publisher_id = fields.Many2one('res.partner', string='Publisher')

    copy_ids = fields.One2many('library.copy', 'book_id', string="Book Copies")


class BookCopy(models.Model):
    _name = 'library.copy'
    _description = 'Book Copy'
    _rec_name = 'reference'

    book_id = fields.Many2one('library.book', string="Book", required=True, ondelete="cascade", delegate=True)
    reference = fields.Char()

    rental_ids = fields.One2many('library.rental', 'copy_id', string='Rentals')
