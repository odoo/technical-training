from email.policy import default

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order ="id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.add(fields.date.today(), months=3))
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    garden = fields.Boolean()
    garden_orientation = fields.Selection([("north", "North"),("south", "South"), ("east", "East"),("west", "West")])
    active= fields.Boolean(default=True)
    state = fields.Selection(selection = [("new","New"),("offer_received","Offer Received"),
                              ("offer_accepted","Offer Accepted"),("sold","Sold"),("cancelled","Cancelled")],
                             default="new",
                             copy=False,
                             required=True)
    postcode = fields.Char()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden_area = fields.Integer()
    living_area = fields.Integer()
    property_type_id = fields.Many2one("estate.property.type", string="Property type")
    salesperson_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", copy=False)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    best_price = fields.Float(compute="_compute_best_price")
    total_area = fields.Integer(compute="_compute_total_area")

    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)",
         'The expected price must be strictly positive'),
        ("check_selling_price", "CHECK(selling_price >= 0)",
        'The selling price must be positive'),
    ]

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property in self:
            if property.offer_ids:
                property.best_price = max (property.offer_ids.mapped("price"))
            else:
                property.best_price = 0

    @api.depends('garden_area','living_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.garden_area + property.living_area

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
                self.garden_area = 10
                self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False


    def action_cancel_property(self):
        for property in self:
            property.state = "cancelled"

    def action_sell_property(self):
        for property in self:
            if property.state == "cancelled":
                raise UserError(_("Cancelled properties cannot be sold"))
            property.state = "sold"


    @api.constrains('selling_price','expected_price')
    def _check_selling_price(self):
        for property in self:
            if (not float_is_zero(property.selling_price, precision_rounding = 0.01) and
                float_compare(property.selling_price, 0.9 * property.expected_price, precision_rounding=0.01) < 0
            ):
                raise ValidationError(_(''))

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_canceled(self):
        for property in self:
            if property.state not in ("new", "cancelled"):
                raise UserError(_("Only new or canceiled property can be deleted"))
