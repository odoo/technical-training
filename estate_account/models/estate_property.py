from odoo import Command, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        self.ensure_one()
        # Step 2: create an empty customer invoice for the buyer
        buyer = self.buyer_id
        if buyer:
            Move = self.env["account.move"].with_context(default_move_type="out_invoice")
            journal = Move._get_default_journal()
            if not journal:
                raise UserError("No Sales Journal configured for this company.")
            fee_amount = (self.selling_price or 0.0) * 0.06
            Move.create({
                "partner_id": buyer.id,
                "move_type": "out_invoice",
                "journal_id": journal.id,
                "invoice_line_ids": [
                    Command.create({
                        "name": "6% Commission on selling price",
                        "quantity": 1,
                        "price_unit": fee_amount,
                    }),
                    Command.create({
                        "name": "Administrative fees",
                        "quantity": 1,
                        "price_unit": 100.0,
                    }),
                ],
            })
        return super().action_set_sold()


