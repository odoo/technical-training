from odoo import api, models, _, fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'



def action_confirm(self):
    res = super(SaleOrder, self).action_confirm()
    for order in self:
        for line in order.order_line:
            if line.training_dates and line.employee_id:
                self.env['calendar.event'].create({
                    'name': 'Training session',
                    'start_date': line.training_dates,
                    'stop_date': line.training_dates + timedelta(hours=1),
                    'partner_ids': [(4, line.employee_id.id)],
                })
    return res
 

    