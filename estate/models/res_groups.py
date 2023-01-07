from odoo import fields, models

class ResGroups(models.Model):
    _inherit = 'res.groups' #The _inherit attribute specifies that this model will inherit all the fields and behavior of the res.groups model, and add some new functionality to it.
    max_amount = fields.Float(string="Training max price approval") #The max_amount field is a new field that is being added to the ResGroups model. It is a floating point field that will store a value representing the maximum price for which training approval is required. The field has a string attribute, "Training max price approval", which will be used as the label for this field in the user interface.
    
