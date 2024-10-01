{
    "name": "Estate",  # The name that will appear in the App list
    "version": "18.0.0.24",  # Version
    "application": True,  # This line says the module is an App, and not a module
    "depends": ["base"],  # dependencies
    "data": [
        # views
        "views/estate_property_views.xml",
        "views/estate_property_settings_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_menus.xml",

        # security
        "security/res_groups.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [
        "demo/demo.xml",
    ],
    "installable": True,
    'license': 'LGPL-3',
}
