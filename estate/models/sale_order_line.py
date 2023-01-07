from odoo import fields, models, Command

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    training_date = fields.Char(string="Training Date")
    employee_id = fields.Many2one('hr.employee', string="Employee")
    is_recurring = fields.Boolean(string='Is Recurring')


# # That will open the wizard when clicked,
# <button name="%(training_date_wizard_action)d" string="Choose Training Date" type="action" class="oe_highlight"/>

# Add a selection field to specify the recurrence frequency
    recurrence_frequency = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ], string='Recurrence Frequency')

# Add a integer field to specify the number of recurrences
    recurrence_count = fields.Integer(string='Recurrence Count')

# Add a method to generate recurring training records
  
    def create_recurring_training(self):
        # Iterate through each record
        for record in self:
            # Check if the training is recurring
            if record.is_recurring:
                # Calculate the recurrence interval in days based on the frequency
                if record.recurrence_frequency == 'daily':
                    interval = 1
                elif record.recurrence_frequency == 'weekly':
                    interval = 7
                elif record.recurrence_frequency == 'monthly':
                    interval = 30
                elif record.recurrence_frequency == 'yearly':
                    interval = 365

                # Generate the recurring training records
                for i in range(1, record.recurrence_count+1):
                    # Create a new training record with the same values as the original record
                    new_record = record.copy()
                    # Increment the training date by the recurrence interval
                    new_record.training_date = fields.Date.from_string(new_record.training_date) + timedelta(days=interval)
                    # Save the new record
                    new_record.save()


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