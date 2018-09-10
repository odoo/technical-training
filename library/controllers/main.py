
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import date


class LibraryController(http.Controller):

    @http.route('/library/statistics', type='json', auth='user')
    def library_statistics(self):
        Book = request.env['product.product']
        Payment = request.env['library.payment']
        Rental = request.env['library.rental']
        first_day = date.today().replace(day=1).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        last_day = date.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        rental_month_domain = [('rental_date', '>=', first_day), ('rental_date', '<=', last_day)]
        book_month_domain = [('date', '>=', first_day), ('date', '<=', last_day)]
        lost_books = Rental.search([('state', '=', 'lost')] + rental_month_domain)
        nb_rentals = Rental.search_count(rental_month_domain)

        return {
            'money_in': sum(Payment.search(book_month_domain).mapped('amount')),
            'nb_rentals': nb_rentals,
            'nb_lost_books': len(lost_books),
            'money_lost': sum(lost_books.mapped('book_id').mapped('acquisition_price')),
            'nb_available_books': Book.search_count([('book', '=', True), ('book_state', '=', 'available')]),
            'nb_rented_books': Book.search_count([('book', '=', True), ('book_state', '=', 'rented')]),
            'nb_lost_books_total': Book.search_count([('book', '=', True), ('book_state', '=', 'lost')]),
        }
