from datetime import datetime, timedelta
from datetime import date
from odoo import fields, models
from odoo import api
from odoo import exceptions
from odoo.exceptions import ValidationError

class ResUsers(models.Model):
    _inherit = "res.users"
    
    property_ids = fields.One2many('estate.property', 'salesperson_id', string='Properties', domain="[('active', '=', True), '|', ('state', '=', 'new'), ('state', '=', 'offer_received')]", help='List of properties')
