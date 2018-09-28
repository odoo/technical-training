# -*- coding: utf-8 -*-
{
    'name': "Map View",
    'summary': "Defines the 'map' view",
    'description': """
        Defines a new type of view ('awesome_map') which allows to visualize
        records on a map.
    """,

    'version': '0.2',
    'depends': ['base_geolocalize', 'contacts'],
    'data': [
        "views/res_partner.xml",
        "views/templates.xml"
    ],
    'qweb': [
        "static/src/xml/map_view.xml",
    ],
    'license': 'AGPL-3'
}
