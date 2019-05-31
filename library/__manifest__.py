# -*- coding: utf-8 -*-
{
    'name':        "Library Management",

    'summary':
                   """
                   Library management
                   """,

    'description': """
        Manage a Library: customers, books, etc....
    """,

    'author':      "Odoo",
    'website':     "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category':    'Library',
    'version':     '0.7',

    # any module necessary for this one to work correctly
    'depends':     ['base', 'product'],

    # always loaded
    'data':        [
        "security/ir.model.access.csv",
        "views/menus.xml",
        "views/author.xml",
        "views/books.xml",
        "views/customer.xml",
        "views/payment.xml",
        "views/price.xml",
        "views/rental.xml",
        "wizard/select_books_views.xml",
        "data/cron.xml",
        "data/mail.xml",
        "data/library_data.xml",
    ],
    # only loaded in demonstration mode
    'demo':        [],
}
