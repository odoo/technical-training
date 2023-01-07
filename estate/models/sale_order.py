from odoo import api, models, _, fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
#     def check_max_amount(self):
#         for order in self:
#             max_amount = order.partner_id.max_amount
#             if max_amount:
#                 total_amount = sum(line.price_total for line in order.order_line)
#                 if total_amount > max_amount:
#                     raise ValidationError(_("The total amount of this sale order exceeds the maximum allowed for the partner."))

# # 56


# def create(self, vals):
#     order = super().create(vals)
#     order.check_max_amount()
#     return order

# def write(self, vals):
#     res = super().write(vals)
#     self.check_max_amount()
#     return res

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

def request_approval(self):
    self.ensure_one()
    # create an activity for a manager
    self.activity_schedule(
        'mail.mail_activity_data_todo',
        user_id=self.env.ref('my_module.manageruser').id,
        note=('Approval needed for quotation %s') % self.name,
    )



def request_approval(self):
    self.ensure_one()
    # get the manager with the least approvals waiting to be assigned
    manager = self.env['res.users'].search([('groups_id', '=', self.env.ref('my_module.manager_group').id)],
                                           order='approval_count ASC').id
    # create an activity for the selected manager
    self.activity_schedule(
        'mail.mail_activity_data_todo',
        userid=manager,
        note=('Approval needed for quotation %s') % self.name,
    )

 

    