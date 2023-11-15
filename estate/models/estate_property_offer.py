from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


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
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    _sql_constraints = [
        ('check_price', 'CHECK(price >= 0)', 'The Offer Price should be positive.')
    ]

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
            record.property_id.selling_price = record.price
            record.property_id.seller_id = record.partner_id

    def estate_property_offer_refused_action(self):
        self.status = "refused"

    @api.model
    def create(self, vals):
        property_id = vals.get('property_id')
        if property_id:
            property_obj = self.env['estate.property'].browse(property_id)

            # Check if there is any existing offer with a higher price
            existing_offers = self.env['estate.property.offer'].search([
                ('property_id', '=', property_id),
                ('price', '>', vals.get('price', 0))
            ])
            if existing_offers:
                raise ValidationError("You cannot create an offer with a lower price than existing offers.")

            # Set the property state to 'Offer Received'
            property_obj.state = 'offer_received'

        return super(EstatePropertyOffer, self).create(vals)