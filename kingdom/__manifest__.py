# -*- coding: utf-8 -*-
{
    'name':        "Kingdom",

    'summary':
                   """
                   Kingdom""",

    'description': """
        The management of the Kingdom
    """,

    'author':      "Odoo",
    'website':     "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category':    'Kingdom',
    'version':     '0.1',

    # any module necessary for this one to work correctly
    'depends':     ['base'],

    # always loaded
    'data':        [
        "security/ir.model.access.csv",
        'data/kindgdom_data.xml',
        'views/army_views.xml',
        'views/citizen_views.xml',
        'views/economy_views.xml',
        'views/kingdom_views.xml',
        'views/menu_views.xml',
    ],
    # only loaded in demonstration mode
    'demo':        [],
}
