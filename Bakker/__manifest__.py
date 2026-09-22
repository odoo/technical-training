{
    "name": "Bakker",  # The name that will appear in the App list
    "version": "18.0.1.0.5",  # Version
    "application": True,  # This line says the module is an App, and not a module
    "depends": ["base", "mail"],  # dependencies
    "data": [
        "data/bakker_koeken_categorie_data.xml",
        "data/bakker_koeken_tags_data.xml",
        "data/bakker_koeken_data.xml",
        "data/bakker_email_template.xml",
        "security/ir.model.access.csv",
        "views/bakker_koeken_categorie_views.xml",
        "views/bakker_koeken_tags_views.xml",
        "views/bakker_koeken_views.xml",
        "views/bakker_verkoop_views.xml",
        "reports/bakker_factuur_report.xml",
    ],
    "installable": True,
    'license': 'LGPL-3',
}
