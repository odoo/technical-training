# -*- coding: utf-8 -*-
from odoo import api, exceptions, fields, models


class SelectBooksToRent(models.TransientModel):
    _name = 'select_books.wizard'
    _description = 'Wizard to select books to rent'

    @api.model
    def default_get(self, fields):
        res = super(SelectBooksToRent, self).default_get(fields)
        res.update({'copy_ids': [(6, 0, self._context.get('active_ids', []))]})
        return res

    copy_ids = fields.Many2many('library.copy', string="Book copies", required=True)
    customer_id = fields.Many2one('res.partner', string="Customer")
    rental_ids = fields.Many2many('library.rental')
    return_date = fields.Date()

    @api.model
    def create(self, vals):
        res = super(SelectBooksToRent, self).create(vals)
        return res

    def next_step(self):
        for copy in self.copy_ids:
            copy.rental_ids |= self.env['library.rental'].create({'copy_id': copy.id, 'customer_id': self.customer_id.id, 'return_date': self.return_date})
        return {
            'name':      'Rentals of %s' % (self.customer_id.name),
            'type':      'ir.actions.act_window',
            'res_model': 'library.rental',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'domain':    [('state', '=', "draft"), ('customer_id', "=", self.customer_id.id)],
            'target':    'self',
        }