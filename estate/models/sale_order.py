from odoo import api, models, _, fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

     @api.constrains('partner_id', 'order_line')
    def check_max_amount(self):
      for order in self:
        if order.partner_id.max_amount > 0:
          total_amount = sum(line.price_total for line in order.order_line)
          if total_amount > order.partner_id.max_amount:
            raise ValidationError(_("The total amount of this sale order exceeds the maximum allowed for the partner."))



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


 

    