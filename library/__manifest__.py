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

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        "data/library_data.xml",
        "data/views.xml",
    ],
    # only loaded in demonstration mode
    'demo': [],
}