{
    "name": "Estate",  # The name that will appear in the App list
    "version": "16.0.0",  # Version
    "application": True,  # This line says the module is an App, and not a module
    "depends": ["base"],  # dependencies
    "data": [
        "security/ir.model.access.csv",
        
        "views/estate_property_views.xml",
        "views/property_type_views.xml",
        "views/property_tag_views.xml",
        "views/offers_view.xml",
        
        "actions/estate_property_menus.xml",
    ],
    "installable": True,
    'license': 'LGPL-3',
}
