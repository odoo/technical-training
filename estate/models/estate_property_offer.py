from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


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
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(months=+(record.validity))
            else:
                record.date_deadline = fields.Date.today() + relativedelta(months=+(record.validity))

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days
