from odoo import api, fields, models

class TrainingDateWizard(models.TransientModel):
    _name = 'training.date.wizard'

    # Add a field to hold the selected training date
    training_date = fields.Date(string='Training Date')