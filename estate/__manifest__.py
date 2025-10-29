{
    "name": "Estate",
    "version": "18.0.1.0.0",
    "application": True,
    "depends": ["base"],
    "data": [
        # Security files first
        "security/ir.model.access.csv",

        # Data files in dependency order
        # "data/estate_property_type_data.xml",  # Base data first
        # "data/estate_property_tag_data.xml",   # Independent data
        # "data/estate_property_offer_data.xml", # Depends on property types

        # Views and menus last
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/res_users_views.xml",
        "views/estate_menus.xml",
    ],
    "installable": True,
    "license": "LGPL-3",
}
