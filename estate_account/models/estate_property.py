from odoo import models, Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        
        result = super().action_sold()
        
        for record in self:

            invoice = self.env['account.move'].create({
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',  # Customer Invoice
                'invoice_line_ids': [

                    Command.create({
                        'name': f'Commission for {record.name}, (Selling Price: {record.selling_price:,.2f})',
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06,
                    }),

                    Command.create({
                        'name': 'Administrative fees',
                        'quantity': 1,
                        'price_unit': 100.00,
                    }),
                ],
            })
            
            print(f"Invoice created: {invoice.id} for property: {record.name}")
        
        return result