from odoo import api, models, _, fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
#This method checks if the total amount of a sale order exceeds the maximum allowed for the partner. It is currently commented out and will not be used unless the # characters at the beginning of the lines are removed.

#     def check_max_amount(self): 
#         for order in self:
#             max_amount = order.partner_id.max_amount
#             if max_amount:
#                 total_amount = sum(line.price_total for line in order.order_line)
#                 if total_amount > max_amount:
#                     raise ValidationError(_("The total amount of this sale order exceeds the maximum allowed for the partner."))

# # 56

#This method overrides the base create() method for sale orders and calls the check_max_amount() method after the sale order is created.
# def create(self, vals):
#     order = super().create(vals)
#     order.check_max_amount()
#     return order

# This method overrides the base write() method for sale orders and calls the check_max_amount() method after the sale order is modified.
# def write(self, vals):
#     res = super().write(vals)
#     self.check_max_amount()
#     return res


# This method overrides the base action_confirm() method for sale orders, and adds additional functionality to it. When a sale order is confirmed, the method creates calendar events for training sessions based on the training dates and employees specified in the sale order lines.
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

#This method is defined twice in the code, with the second definition overwriting the first. The method creates an activity for a manager, requesting approval for a quotation. The manager is either the one with the least approvals waiting to be assigned, or the one with the manageruser user id.
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

    # Add the 'approval_count' field to the SaleOrder model
    # This will add an approval_count field to the SaleOrder model, and every time the action_confirm method is called (which happens when the sale order is approved), the approval_count field will be incremented by 1.
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    approval_count = fields.Integer(string='Approval Count', default=0)

    # Increment the 'approval_count' field every time the sale order is approved
    def action_confirm(self):
        # Call the super method to confirm the sale order
        super(SaleOrder, self).action_confirm()
        # Increment the 'approval_count' field
        self.approval_count += 1


 

    