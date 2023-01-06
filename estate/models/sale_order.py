from odoo import api, models, _, fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    employee_id = fields.Many2one('res.partner', string="Employee")


@api.multi
def action_confirm(self):
    # Create the event in the calendar of the selected employee
    self.ensure_one()
    event_vals = {
        'name': 'Training',
        'start': self.order_line.training_date,
        'stop': self.order_line.training_date,
        'partner_ids': [(6, 0, [self.employee_id.id])],
    }
    event = self.env['calendar.event'].create(event_vals)
    return super(SaleOrder, self).action_confirm()    