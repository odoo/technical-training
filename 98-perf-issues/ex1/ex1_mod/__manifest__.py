# -*- coding: utf-8 -*-
{
    'name': "perf ex1",

    'summary': """

        """,

    'description': """
There's a perf issue in this module when importing.

    """,

    'author': "Odoo",
    'website': "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Training',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['mail'],

    # always loaded
    'data': [
        'views/course.xml',
        'views/session.xml',
        'views/registration.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
}
