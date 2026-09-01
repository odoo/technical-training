from odoo import api, fields, models

class Offer(models.Model):
        _name = "estate.property.offer"
        _description = "Offers"

        price = fields.Float(required=True)
        buyer_id = fields.Many2one("res.partner", string="Partner")
        validity = fields.Integer(default=7, required=True, string="Validity (days)")
        deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline", string="Deadline Date")
        status = fields.Selection(
                selection=[
                    ("new", "New"),
                    ("accepted", "Accepted"),
                    ("refused", "Refused"),
                ],
                default="new",
                copy=False,
                required=True,
        )

        property_id = fields.Many2one("estate.property", required=True)

        @api.depends("validity", "create_date")
        def _compute_deadline(self):
            for estate in self:
                create_date = estate.create_date or fields.Date.today()
                estate.deadline = fields.Date.add(create_date, days=estate.validity)

        def _inverse_deadline(self):
            for estate in self:
                estate.validity = (estate.deadline - fields.Date.to_date(estate.create_date)).days

        def action_accept_offer(self):
            self.status = "accepted"
            for offer in self:
                offer.property_id.selling_price = offer.price

        def action_refuse_offer(self):
            self.status = "refused"
            