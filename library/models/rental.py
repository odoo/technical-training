# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Rentals(models.Model):
    _name = 'library.rental'
    _description = 'Book rental'

    customer_id = fields.Many2one('library.partner', string='Customer', domain=[('partner_type', '=', 'customer')])
    book_id = fields.Many2one('library.book', string='Book')
    book_child_id = fields.Many2one('library.book_child', string='Book child')

    rental_date = fields.Date()
    return_date = fields.Date()

    customer_address = fields.Text(related='customer_id.address')
    customer_email = fields.Char(related='customer_id.email')

    book_authors = fields.Many2many(related='book_id.author_ids')
    book_edition_date = fields.Date(related='book_id.edition_date')
    book_publisher = fields.Many2one(related='book_id.publisher_id')

    @api.onchange('book_id')
    def _campus_onchange(self):
        self.book_child_id = ''
        res = {}
        res['domain']={'book_child_id':[('book_child_id', '=', self.book_id.id)]}
        return res
