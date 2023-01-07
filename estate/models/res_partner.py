from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner' # The _inherit attribute specifies that this model will inherit all the fields and behavior of the res.partner model, and add some new functionality to it.
    #  max_amount = fields.Float(string="Maximum allowed amount") #The max_amount field is a new field that is being added to the ResPartner model. It is a floating point field that will store a value representing the maximum allowed amount. The field has a string attribute, "Maximum allowed amount", which will be used as the label for this field in the user interface.
