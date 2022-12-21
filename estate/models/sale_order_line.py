from odoo import fields, models, Command

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    training_date = fields.Date(string = "Training Date")
    employee = fields.Many2one("hr.employee", "Employee")