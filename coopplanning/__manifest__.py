# -*- coding: utf-8 -*-
{
    'name':        "Cooperative Management",

    'summary':
                   """
                   Cooperative management
                   """,

    'description': """
        Manage a cooperative group 
    """,

    'author':      "Odoo",
    'website':     "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category':    'Cooperative Planning',
    'version':     '0.4',

    # any module necessary for this one to work correctly
    'depends':     ['base'],

    # always loaded
    'data':        [
        "security/ir.model.access.csv",
        "views/task_views.xml",
        "views/daynumber_views.xml",
        "views/menu_views.xml",
        "data/coop_data.xml",
        "data/task_template.xml",
    ],
    # only loaded in demonstration mode
    'demo':        [],
    'license': 'AGPL-3',
}
