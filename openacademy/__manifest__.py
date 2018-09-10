# -*- coding: utf-8 -*-
{
    'name': "OpenAcademy",

    'summary': """
        Course management""",

    'description': """
        Open Academy allow you to manager you course, session, teacher and attendee.
    """,

    'author': "Odoo",
    'website': "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Academy',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'data/openacademy_data.xml',
        'views/courses.xml',
        'views/sessions.xml',
        'views/partners.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
}
