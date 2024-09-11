{
    "name": "Estate",  # The name that will appear in the App list
    "version": "16.0.0",  # Version
    "application": True,  # This line says the module is an App, and not a module
    "depends": ["base"],  # dependencies
    "data": [
        'security/ir.model.access.csv',
        # estate property
        'views/estate_property_views.xml',
        # estate property offer
        'views/estate_property_offer_views.xml',
        # estate property type
        'views/estate_property_type_views.xml',
        # estate property tag
        'views/estate_property_tag_views.xml',
        'views/res_users.xml',
        'views/estate_menus.xml',
    ],
    "installable": True,
    'license': 'LGPL-3',
}
