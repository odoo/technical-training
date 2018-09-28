# -*- coding: utf-8 -*-

import logging
import random

from odoo import http
from odoo.http import request
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import date, datetime

logger = logging.getLogger(__name__)


class OrderRoute(http.Controller):
    @http.route(['/awesome_tshirt/order'], type='http', auth='public')
    def make_order(self):
        """
        Renders the public page to make orders
        """
        return request.render('awesome_tshirt.order_public_page')

    @http.route(['/awesome_tshirt/validate_order'], type='http', auth="public", methods=['POST'], website=True)
    def validate_order(self, name, email, address, quantity, size, url):
        """
        Creates an order (and optionnaly a partner) with the given data
        """
        Partner = request.env['res.partner'].sudo()
        customer = Partner.search([('email', '=', email)], limit=1)
        if not customer:
            customer = Partner.create({
                'street': address,
                'email': email,
                'name': name,
            })
        request.env['awesome_tshirt.order'].create({
            'customer_id': customer.id,
            'quantity': quantity,
            'size': size,
            'image_url': url,
        })
        return request.render('awesome_tshirt.thank_you')

    @http.route('/awesome_tshirt/statistics', type='json', auth='user')
    def get_statistics(self):
        """
        Returns a dict of statistics about the orders:
            'average_quantity': the average number of t-shirts by order
            'average_time': the average time (in hours) elapsed between the
                moment an order is created, and the moment is it sent
            'nb_cancelled_orders': the number of cancelled orders, this month
            'nb_new_orders': the number of new orders, this month
            'total_amount': the total amount of orders, this month
        """
        Order = request.env['awesome_tshirt.order']
        first_day = date.today().replace(day=1).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        last_day = datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        this_month_domain = [('create_date', '>=', first_day), ('create_date', '<=', last_day)]
        new_this_month_domain = expression.AND([this_month_domain, [('state', '=', 'new')]])
        nb_new_orders = Order.search_count(new_this_month_domain)
        cancelled_this_month_domain = expression.AND([this_month_domain, [('state', '=', 'cancelled')]])
        nb_cancelled_orders = Order.search_count(cancelled_this_month_domain)
        total_amount = Order.read_group(new_this_month_domain, ['amount'], [])[0]['amount']
        total_quantity = Order.read_group(this_month_domain, ['quantity'], [])[0]['quantity']
        nb_orders = Order.search_count(this_month_domain)
        orders_by_size = Order.read_group([['state', '!=', 'cancelled']], [], ['size'])

        return {
            'average_quantity': 0 if not nb_orders else round(total_quantity / nb_orders, 2),
            'average_time': (random.random() * 44) + 4,  # simulate a delay between 4 and 48 hours
            'nb_cancelled_orders': nb_cancelled_orders,
            'nb_new_orders': nb_new_orders,
            'orders_by_size': {g['size']: g['quantity'] for g in orders_by_size},
            'total_amount': total_amount or 0,
        }

    @http.route('/awesome_tshirt/bafienistalkingtoyou', type='json', auth='user')
    def bafienistalkingtoyou(self):
        """
        Returns a message to display in the HomeMenu
        """
        if random.random() > 0.5:
            return "Bafien is watching you"
        return "Bafien is totally sane. Also, please work harder."
