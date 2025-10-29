from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date, timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        string="Status",
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
        ondelete="cascade",
    )
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type",
        string="Property Type",
        related="property_id.property_type_id",
        store=True,
    )

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=False)

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self) -> None:
        for offer in self:
            created = (offer.create_date or fields.Datetime.now())
            base_date = created.date()
            offer.date_deadline = base_date + timedelta(days=offer.validity or 0)

    def _inverse_date_deadline(self) -> None:
        for offer in self:
            created = (offer.create_date or fields.Datetime.now())
            base_date = created.date()
            if offer.date_deadline:
                delta = offer.date_deadline - base_date
                offer.validity = max(delta.days, 0)

    # Make the form reactive while editing (no need to wait for save)
    @api.onchange("validity")
    def _onchange_validity(self):
        for offer in self:
            created = (offer.create_date or fields.Datetime.now())
            base_date = created.date()
            offer.date_deadline = base_date + timedelta(days=offer.validity or 0)

    @api.onchange("date_deadline")
    def _onchange_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                created = (offer.create_date or fields.Datetime.now())
                base_date = created.date()
                delta = offer.date_deadline - base_date
                offer.validity = max(delta.days, 0)

    # Actions on offers
    def action_accept(self):
        for offer in self:
            if offer.property_id.state == "sold":
                raise UserError("Cannot accept an offer on a sold property.")
            # set other offers to refused
            siblings = offer.property_id.offer_ids - offer
            siblings.write({"status": "refused"})
            offer.status = "accepted"
            offer.property_id.write({
                "buyer_id": offer.partner_id.id,
                "selling_price": offer.price,
                "state": "offer_accepted",
            })
        return True

    def action_refuse(self):
        self.status = "refused"
        return True

    # SQL constraints
    _sql_constraints = [
        (
            "offer_price_strictly_positive",
            "CHECK(price > 0)",
            "The offer price must be strictly positive.",
        ),
    ]

    # When an offer is created, mark the property as having an offer
    @api.model_create_multi
    def create(self, vals_list):
        # Business rule: price must be strictly higher than any existing offer on the property
        props = self.env["estate.property"]
        for vals in vals_list:
            property_id = vals.get("property_id")
            if property_id:
                prop = self.env["estate.property"].browse(property_id)
                props |= prop
                existing_max = max(prop.offer_ids.mapped("price") or [0.0])
                if vals.get("price") is not None and vals["price"] <= existing_max:
                    raise UserError("Offer must be higher than all existing offers for this property.")

        records = super().create(vals_list)
        # Set property state to Offer Received for affected properties
        props.filtered(lambda p: p.state == "new").state = "offer_received"
        return records
