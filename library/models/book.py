# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Books(models.Model):
    _inherit = 'product.product'

    author_ids = fields.Many2many("res.partner", string="Authors", domain=[('author', '=', True)])
    edition_date = fields.Date()
    isbn = fields.Char(string='ISBN', unique=True)
    publisher_id = fields.Many2one('res.partner', string='Publisher', domain=[('publisher', '=', True)])
    copy_ids = fields.One2many('library.copy', 'book_id', string="Book Copies")
    book = fields.Boolean(string='Is a Book', default=False)


class BookCopy(models.Model):
    _name = 'library.copy'
    _description = 'Book Copy'

    book_id = fields.Many2one('product.product', string="Book", domain=[('book', "=", True)], required=True, ondelete="cascade", delegate=True)
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


class Wizard(models.TransientModel):
    _name = 'library.wizard'
    _description = 'Wizard to add attendees to a session'

    @api.model
    def default_get(self, fields):
        res = super(Wizard, self).default_get(fields)
        res.update({'copy_ids': [(6, 0, self._context.get('active_ids', []))]})
        return res

    copy_ids = fields.Many2many('library.copy', string="Book copies", required=True)
    customer_id = fields.Many2one('res.partner', string="Customer")
    rental_ids = fields.Many2many('library.rental')
    return_date = fields.Date()

    @api.model
    def create(self, vals):
        res = super(Wizard, self).create(vals)
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
