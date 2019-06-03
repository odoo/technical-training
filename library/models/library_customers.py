from odoo import api, fields, models
from odoo.exceptions import Warning


class Customers(models.Model):
    _name = 'library.partner'
    _description = 'Partner'

    name = fields.Char('Name', required=True)
    address = fields.Char('Address')
    mail = fields.Char('Email address')

    rented_books_ids = fields.One2many('library.rental', 'customer_id', string='Rented books')


