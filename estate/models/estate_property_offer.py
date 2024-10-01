from odoo import models, fields, api

# this is creating a table
class RealEstate(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    # this is creating fields in the table
    price = fields.Float(copy=False, required=True)
    status = fields.Selection(
        default="received", required=True,
        selection=[('received', 'Offer Received'), ('accepted', 'Offer Accepted'), ('refused', 'Refused')],
        )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default = 7, required=True)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if not record.create_date:
                record.date_deadline = fields.Date.add(value=fields.Date.today(), days=record.validity)
            else:
                record.date_deadline = fields.Date.add(value=record.create_date, days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if not record.create_date:
                record.validity = (record.date_deadline - fields.Date.today()).days
            else:
                record.validity = (record.date_deadline - fields.Date.to_date(record.create_date)).days