# -*- coding: utf-8 -*-
import logging
import random
import time

from odoo import models, fields, api
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class TShirtOrder(models.Model):
    _name = 'awesome_tshirt.order'
    _description = 'Awesome T-shirt Orders'

    @api.model
    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    amount = fields.Float('Amount', compute='_compute_amount', store=True)
    customer_id = fields.Many2one('res.partner', string="Customer")
    image_url = fields.Char('Image', help="encodes the url of the image")
    is_late = fields.Boolean('Is late', compute='_compute_is_late')
    quantity = fields.Integer('Quantity', default="1")
    size = fields.Selection([
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL')], default='m', required="True")
    state = fields.Selection([
        ('new', 'New'),
        ('printed', 'Printed'),
        ('sent', 'Sent'),
        ('cancelled', 'Cancelled')], default='new', required="True", group_expand='_expand_states')

    @api.depends('quantity')
    def _compute_amount(self):
        for record in self:
            unit_price = 15
            if record.size == 's':
                unit_price = 12
            elif record.size in ['xl', 'xxl']:
                unit_price = 18
            if record.quantity > 5:
                unit_price = unit_price * 0.9
            record.amount = record.quantity * unit_price

    @api.depends('create_date')
    def _compute_is_late(self):
        for record in self:
            record.is_late = record.create_date < datetime.today() - timedelta(days=7)

    @api.multi
    def print_label(self):
        """
        This method simulate the printing of a label. It is slow (> 500ms), and
        if randomly fails. It returns True if the label has been printed, False
        otherwise
        """
        time.sleep(0.5)
        if random.random() < 0.1:
            _logger.info('Printer not connected')
            return False
        _logger.info('Label printed')
        return True
