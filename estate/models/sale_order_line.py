from odoo import fields, models, Command

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    training_date = fields.Char(string="Training Date")
    
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    employee_id = fields.Many2one('res.partner', string="Employee")