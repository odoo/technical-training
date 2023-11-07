from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    name = fields.Char()
    price = fields.Float()
    status = fields.Selection(
        string='Type',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused') ],
        help="")
    partner_id = fields.Many2one("res.partner", string="Partner")
    property_id = fields.Many2one("estate.property", string="Property")
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    def estate_property_offer_accepted_action(self):
        for record in self:
            record.status = "accepted"

    def estate_property_offer_refused_action(self):
        for record in self:
            record.status = "refused"

    @api.onchange("status")
    def _onchange_status(self):
        for record in self:
            self.selling_price = record.price
            self.seller_id = record.partner_id