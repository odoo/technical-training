{
    "name": "Estate Account",  # The name that will appear in the App list
    "version": "16.0.0",  # Version
    "application": True,  # This line says the module is an App, and not a module
    "depends": ["estate", "account"],  # dependencies
    "data": [
        'security/ir.model.access.csv'
    ],
    "installable": True,
    'license': 'LGPL-3',
}