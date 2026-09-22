{
    "name": "Estate", 
    "version": "16.0.0",  
    "application": True,  
    "depends": ["base"],  
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",        
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
        'views/res_users_views.xml',
    ],
    "installable": True,
    "application": True,
    'license': 'LGPL-3',
}
