# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import datetime

class Rental(models.Model):
    _name = 'library.rental'
    _description = 'Book rental'
    _rec_name = 'book_id'
    _order = "rental_date desc,return_date desc"

    customer_id = fields.Many2one(
        'res.partner',
        'Customer',
        domain=[('customer','=',True), ],
        required=True,
    )
    book_id = fields.Many2one(
        'product.product',
        'Book',
        domain=[('book','=',True), ('book_state','=','available')],
        required=True,
    )
    rental_date =  fields.Date(string='Rental date', required=True, default=lambda self: fields.Date.today())
    return_date =  fields.Date(string='Return date', required=True)
    state = fields.Selection([('draft', 'Draft'), ('rented', 'Rented'), ('returned', 'Returned'), ('lost', 'Lost')],
                            group_expand='_read_group_state',
                            default="draft")

    is_late = fields.Boolean(string='Is Late', compute='_compute_is_late')

    @api.multi
    def write(self, vals):
        if (vals.get('state') == 'returned'):
            for record in self:
                self.book_id.book_state = 'available'

        return super(Rental, self).write(vals)

    @api.depends('return_date')
    def _compute_is_late(self):
        for record in self:
            if record.state == 'rented':
                record.is_late = datetime.strptime(record.return_date, '%Y-%m-%d') < datetime.today()
            else:
                record.is_late = False

    @api.model
    def _read_group_state(self, stages, domain, order):
        return ['draft', 'rented', 'returned', 'lost'];

    @api.multi
    def action_confirm(self):
        for rec in self:
            rec.state = 'rented'
            rec.book_id.book_state = 'rented'
            rec.add_fee('time')

    @api.multi
    def add_fee(self, type):
        for rec in self:
            if type == 'time':
                price_id = self.env.ref('library.price_rent')
                delta_dates = fields.Date.from_string(rec.return_date) - fields.Date.from_string(rec.rental_date)
                amount = delta_dates.days * price_id.price/price_id.duration
            elif type == 'loss':
                price_id = self.env.ref('library.price_loss')
                amount = price_id.price
            else:
                return

            self.env['library.payment'].create({
                'customer_id': rec.customer_id.id,
                'date': rec.rental_date,
                'amount': - amount,
                })

    @api.multi
    def action_return(self):
        for rec in self:
            rec.state = 'returned'
            rec.book_id.book_state = 'available'

    @api.multi
    def action_lost(self):
        for rec in self:
            rec.state = 'lost'
            rec.book_id.book_state = 'lost'
            rec.book_id.active = False
            rec.add_fee('loss')

