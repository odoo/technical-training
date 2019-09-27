# -*- coding: utf-8 -*-
{
    'name':        "Library Management training",

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
    'version':     '0.2',

    # any module necessary for this one to work correctly
    'depends':     ['base'],

    # always loaded
    'data':        [
        #"security/ir.model.access.csv",
        "data/library_data.xml",
        "views/rental.xml",
        "views/book.xml",
        "views/partner.xml",
        "views/menu.xml",
    ],
    # only loaded in demonstration mode
    'demo':        [],
    'license': 'AGPL-3',
}
