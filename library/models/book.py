# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Books(models.Model):
    _inherit = 'product.product'

    author_ids = fields.Many2many("res.partner", string="Authors", domain=[('is_author', '=', True)])
    edition_date = fields.Date()
    isbn = fields.Char(string='ISBN', unique=True)
    publisher_id = fields.Many2one('res.partner', string='Publisher', domain=[('is_publisher', '=', True)])

    copy_ids = fields.One2many('library.copy', 'book_id', string="Book Copies")
    is_book = fields.Boolean(string='Is a Book', default=False)


class BookCopy(models.Model):
    _name = 'library.copy'
    _description = 'Book Copy'
    _rec_name = 'reference'

    book_id = fields.Many2one('product.product', string="Book", domain=[('is_book', "=", True)], required=True, ondelete="cascade", delegate=True)
    reference = fields.Char(required=True, string="Ref")

    rental_ids = fields.One2many('library.rental', 'copy_id', string='Rentals')
    book_state = fields.Selection([('available', 'Available'), ('rented', 'Rented'), ('lost', 'Lost')], default="available")
    readers_count = fields.Integer(compute="_compute_readers_count")

    def open_readers(self):
        self.ensure_one()
        reader_ids = self.rental_ids.mapped('customer_id')
        return {
            'name':      'Readers of %s' % (self.name),
            'type':      'ir.actions.act_window',
            'res_model': 'res.partner',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'domain':    [('id', 'in', reader_ids.ids)],
            'target':    'new',
        }

    @api.depends('rental_ids.customer_id')
    def _compute_readers_count(self):
        for book in self:
            book.readers_count = len(book.mapped('rental_ids'))
