# -*- coding: utf-8 -*-
{
    'name': "Library Management",

    'summary': """
        Library management""",

    'description': """
        Manage a Library: customers, books, etc....
    """,

    'author': "Odoo",
    'website': "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Training',
    'version': '0.1',
    'application': True,

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'web_enterprise', 'base_geolocalize'],

    # always loaded
    'data': [
        "assets.xml",
        "data/library_data.xml",
        "data/cron.xml",
        "data/prices.xml",
        "views/menus.xml",
        "views/customer.xml",
        "views/book.xml",
        "views/author.xml",
        "views/rental.xml",
        "views/payment.xml",
        "views/price.xml",
        "views/dashboard.xml",
    ],
    # only loaded in demonstration mode
    'demo': [],

    # static templates
    'qweb': [
        "static/src/xml/dashboard.xml",
    ],
}
