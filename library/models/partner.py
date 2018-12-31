# -*- coding: utf-8 -*-
from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    is_author = fields.Boolean(string="Is an Author", default="False")
    is_publisher = fields.Boolean(string="Is a Publisher", default="False")

    rental_ids = fields.One2many('library.rental', 'customer_id', string='Rentals')
