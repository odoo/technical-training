from odoo import api, models, _, fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    employee_id = fields.Many2one('hr.employee', string="Employee")


 

    