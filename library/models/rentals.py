# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _

class Rentals(models.Model):
    _name = 'library.rental'
    _description = 'Book rental'

    customer_id = fields.Many2one('library.partner', string='Customer')
    copy_id = fields.Many2one('library.copy', string="Book Copy")
    book_id = fields.Many2one('library.book', string='Book', related='copy_id.book_id', readonly=True)
    rental_date =  fields.Date(string='Rental date', default=fields.Date.context_today)
    return_date = fields.Date(string='Return date')
