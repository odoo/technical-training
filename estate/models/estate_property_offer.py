from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection([("accepted", "Accepted"), ("refused","Refused")], copy=False)
    property_id = fields.Many2one("estate.property", required=True)
    partner_id = fields.Many2one("res.partner", required=True)
    validity = fields.Integer(default = 7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    _sql_constraints = [
        ("check_offer_price", "CHECK(price > 0)",
         'The offer price must be strictly positive')
    ]


    @api.depends('validity','create_date')
    def _compute_deadline(self):
        for offer in self:
            create_date = offer.create_date or fields.Date.today()
            offer.date_deadline = fields.Date.add(create_date, days=offer.validity)


    def _inverse_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - fields.Date.to_date(offer.create_date)).days



    def action_accept_offer(self):
        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id



    def action_refuse_offer(self):
        self.status = "refused"
