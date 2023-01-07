from odoo import fields, models, Command

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    training_date = fields.Char(string="Training Date")
    employee_id = fields.Many2one('hr.employee', string="Employee")


# This function takes a partner and an amount as inputs, and returns an integer value representing the required approval level for the sale. The value is determined by the amount of the sale, with higher amounts requiring higher approval levels.
def get_approval_level(partner, amount):
  if amount < 500:
    return 0 # no approval needed
  elif amount < 2000:
    return 1 # level 1 and above can approve
  elif amount < 5000:
    return 2 # level 2 and above can approve
  else:
    return 3 # level 3 and above can approve

#This function takes a manager level as an input and returns a string representing the group that the manager belongs to, based on their level.
def get_manager_group(manager_level):
  if manager_level == 0:
    return "no approval privileges"
  elif manager_level == 1:
    return "manager level 1 "
  elif manager_level == 2:
    return "manager level 2"
  else:
    return "manager level 3 and above"


#This function takes a partner, an amount, and a manager level as inputs, and uses the get_approval_level() and get_manager_group() functions to determine whether the sale can be confirmed by the manager. If the sale can be confirmed, the function returns True, otherwise it returns False
def can_confirm_sale_order(partner, amount, manager_level):
  required_approval_level = get_approval_level(partner, amount)
  manager_group = get_manager_group(manager_level)
  if required_approval_level <= manager_level:
    print(f"Sale order can be confirmed by {manager_group}.")
    return True
  else:
    print(f"Sale order cannot be confirmed by {manager_group}.")
    return False

# example usage
partner = "ABC Partners"
amount = 1500
manager_level = 1

can_confirm_sale_order(partner, amount, manager_level)