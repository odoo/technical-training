from odoo import fields, models, Command

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    training_date = fields.Char(string="Training Date")
    employee_id = fields.Many2one('hr.employee', string="Employee")

    
# def get_approval_level(partner, amount):
#   if amount < 500:
#     return 0 # no approval needed
#   elif amount < 2000:
#     return 1 # level 1 and above can approve
#   elif amount < 5000:
#     return 2 # level 2 and above can approve
#   else:
#     return 3 # level 3 and above can approve

# def get_manager_group(manager_level):
#   if manager_level == 0:
#     return "no approval privileges"
#   elif manager_level == 1:
#     return "level 1"
#   elif manager_level == 2:
#     return "level 2"
#   else:
#     return "level 3 and above"

# def can_confirm_sale_order(partner, amount, manager_level):
#   required_approval_level = get_approval_level(partner, amount)
#   manager_group = get_manager_group(manager_level)
#   if required_approval_level <= manager_level:
#     print(f"Sale order can be confirmed by {manager_group}.")
#     return True
#   else:
#     print(f"Sale order cannot be confirmed by {manager_group}.")
#     return False

# # example usage
# partner = "ABC Partners"
# amount = 1500
# manager_level = 1

# can_confirm_sale_order(partner, amount, manager_level)