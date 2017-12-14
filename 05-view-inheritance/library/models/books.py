# -*- coding: utf-8 -*-
from odoo import models, fields

class Books(models.Model):
    _name = 'library.book'
    _description = 'Book'

    name = fields.Char(string='Title')
    authors_ids = fields.Many2many('library.partner', string="Authors")
    edition_date =  fields.Date(string='Edition date',)
    isbn = fields.Char(string='ISBN')
    publisher_id = fields.Many2one('library.publisher', string='Publisher')
    copy_ids = fields.One2many('library.copy', 'book_id', string="Book Copies")


class BookCopy(models.Model):
    _name = 'library.copy'
    _description = 'Book Copy'
    _rec_name = 'reference'

    book_id = fields.Many2one('library.book', string="Book",
                              required=True, ondelete="cascade", delegate=True)
    reference = fields.Char(string="Reference")
    rental_ids = fields.One2many('library.rental', 'copy_id', string='Rentals')
