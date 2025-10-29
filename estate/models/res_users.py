from odoo import models, fields


class ResUsers(models.Model):
    _inherit = "res.users"

    # Properties assigned to the salesperson (this user)
    # Only show available properties (New or Offer Received)
    property_ids = fields.One2many(
        comodel_name="estate.property",
        inverse_name="salesman_id",
        string="Properties",
        domain=[("state", "in", ("new", "offer_received"))],
    )


