from odoo import models, Command
import logging

_logger = logging.getLogger(__name__)

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        # Add debugging to verify the override is working
        _logger.info("Estate Account: action_sold method called for property: %s", self.name)
        print(f"Estate Account: Selling property '{self.name}' - Creating invoice")
        
        # Create invoice for the property sale
        for record in self:
            # Calculate commission (6% of selling price) and administrative fee
            commission_amount = record.selling_price * 0.06
            admin_fee = 100.00
            
            # Create the invoice
            invoice = self.env['account.move'].create({
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',  # Customer Invoice
                'invoice_line_ids': [
                    Command.create({
                        'name': f'Commission for property: {record.name}',
                        'quantity': 1,
                        'price_unit': commission_amount,
                    }),
                    Command.create({
                        'name': 'Administrative fees',
                        'quantity': 1,
                        'price_unit': admin_fee,
                    }),
                ],
            })
            
            _logger.info("Estate Account: Created invoice %s for property %s", invoice.name, record.name)
            print(f"Estate Account: Created invoice {invoice.name} for property '{record.name}'")
        
        # Call the parent method to maintain original functionality
        return super().action_sold()
