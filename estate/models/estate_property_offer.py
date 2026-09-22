from odoo import api, models, fields
from datetime import datetime, timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    # SQL Constraints
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 
         'The offer price must be strictly positive.'),
    ]

    price = fields.Float(required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date()
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        required=True
    )
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
        ondelete="cascade"
    )

    property_type_id = fields.Many2one(
        related="property_id.property_type_id",
        string="Property Type",
        store=True
    )

    def action_accept(self):
        for record in self:
            # Diğer tüm offer'ları refuse et
            record.property_id.offer_ids.write({'status': 'refused'})
            # Bu offer'ı accept et
            record.status = 'accepted'
            # Property'nin buyer ve selling price'ını set et
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True

    @api.model
    def create(self, vals_list):
        property_obj = self.env['estate.property'].browse(vals_list['property_id'])

        existing_offers = self.search([('property_id', '=', vals_list['property_id'])])
        if existing_offers:
            max_price = max(existing_offers.mapped('price'))
            if vals_list['price'] <= max_price:
                raise UserError("The offer must be higher than existing offers.")
        

        property_obj.state = 'offer_received'

        return super().create(vals_list)