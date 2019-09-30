# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Books(models.Model):
    _name = 'library.book_child'
    _description = 'Book'

    _inherits = {
        'library.book': 'book_child_id'
    }

    def _get_book_reference(self):
        book_parent_id = self.env.context.get('book_parent_id')    

        to_return = ''

        if book_parent_id:

            book_parent_obj = self.env['library.book'].browse(book_parent_id)

            to_return = str(book_parent_id) + '_' + str(book_parent_obj.next_ref_id) #str(len(self.env['library.book'].browse(book_parent_id).book_child_ids))
            book_parent_obj.next_ref_id += 1

        return to_return

    book_child_id = fields.Many2one('library.book', string='Book')
    reference = fields.Char(string='Book reference', default=_get_book_reference)
    rental_ids = fields.One2many('library.rental', 'book_child_id', string='Rentals')    

    name = fields.Char(compute='_compute_name')

    @api.multi
    def _compute_name(self):
        for record in self:
            record.name = record.reference

