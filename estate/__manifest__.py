{
    "name": "Real Estate",  # The name that will appear in the App list
    "version": "17.0.1.0.0",  # Version
    "application": True,  # This line says the module is an App, and not a module
    "depends": ["base"],  # dependencies
    "data": [
        "security/ir.model.access.csv",
        "views/estate_actions.xml", # add action bevor all other views, so their every time loaded before
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_menus.xml"
    ],
    "installable": True,
    'license': 'LGPL-3',
}
