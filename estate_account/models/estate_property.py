from odoo import fields, models, Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self):
        invoice_lines = [
            {"name": self.name, "quantity": 1, "price_unit": self.selling_price * (self.selling_price * 0.01)},
            {"name": 'administrative fees', "quantity": 1, "price_unit": 100.00}
        ]
        invoice = {
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            "invoice_line_ids": [line for line in invoice_lines],
        }
        self.env['account.move'].create(invoice)
        return super().action_sold_property()
