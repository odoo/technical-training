from odoo import api, models, _, fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    def check_max_amount(self):
        for order in self:
            max_amount = order.partner_id.max_amount
            if max_amount:
                total_amount = sum(line.price_total for line in order.order_line)
                if total_amount > max_amount:
                    raise ValidationError(_("The total amount of this sale order exceeds the maximum allowed for the partner."))


def create(self, vals):
    order = super().create(vals)
    order.check_max_amount()
    return order

def write(self, vals):
    res = super().write(vals)
    self.check_max_amount()
    return res

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


 

    