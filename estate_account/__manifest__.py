{
    "name": "Estate Account",
    "version": "18.0.1.0.5",
    "application": False,  # This is a module, not an app
    "depends": ["estate", "account"],  # Depends on both estate and account modules
    'data': [
        'security/ir.model.access.csv',
    ],
    "installable": True,
    'license': 'LGPL-3',
}
