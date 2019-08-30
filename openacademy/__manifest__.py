# -*- coding: utf-8 -*-
{
    'name':        "OpenAcademy",

    'summary':
                   """
                   Openacademy
                   """,

    'description': """
        Manage course, classes, teachers, students, ...
    """,

    'author':      "Odoo",
    'website':     "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category':    'OpenAcademy',
    'version':     '0.1',

    # any module necessary for this one to work correctly
    'depends':     ['base'],

    # always loaded
    'data':        [
        "security/ir.model.access.csv",
        "data/openacademy_data.xml",
    ],
    # only loaded in demonstration mode
    'demo':        [],
    'license': 'AGPL-3',
}
