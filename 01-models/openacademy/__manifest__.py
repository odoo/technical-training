# -*- coding: utf-8 -*-
{
    'name': "OpenAcademy",

    'summary': """
        Openacademy""",

    'description': """
        Manage course, classes, teachers, students, ...
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
        "data/openacademy_data.xml",
    ],
    # only loaded in demonstration mode
    'demo': [],
}
