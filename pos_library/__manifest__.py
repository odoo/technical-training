# -*- coding: utf-8 -*-
{
    'name': "Library PoS",

    'summary': "Library PoS",

    'description': """
        Handle a Library Rentals
    """,

    'author': "Odoo",
    'website': "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Training',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['library', 'point_of_sale'],

    # always loaded
    'data': [
    ],
    # only loaded in demonstration mode
    'demo': [],
}
