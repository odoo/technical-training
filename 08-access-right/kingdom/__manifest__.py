# -*- coding: utf-8 -*-
{
    'name': "Kingdom",

    'description': "The management of the Kingdom",

    'author': "Odoo",
    'website': "http://www.odoo.com",

    'category': 'Academy',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'data/kindgdom_data.xml',
        'views/menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
}
