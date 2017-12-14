# -*- coding: utf-8 -*-
{
    'name': "Cooperative Management",

    'summary': """
        Cooperative management""",

    'description': """
        Manage a cooperative group 
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
        "data/coop_data.xml",
        "data/task_template.xml",
    ],
    # only loaded in demonstration mode
    'demo': [],
}
