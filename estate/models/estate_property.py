from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_is_zero, float_compare

class EstateProperty(models.Model):
        _name = "estate.property"
        _description = "Estate Property"

        name = fields.Char(required=True)
        property_tag_ids = fields.Many2many("estate.property.tag", string="Tags")

        description = fields.Text()
        address = fields.Text()
        postcode = fields.Char()
        date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), months=3))
        expected_price = fields.Float()
        selling_price = fields.Float(readonly=False, copy=False)
        bedrooms = fields.Integer(default=2)
        living_area = fields.Float(string="Living Area (sqm)")
        garden = fields.Boolean()
        garden_area = fields.Float(string="Garden Area (sqm)")
        garden_orientation = fields.Selection([("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")])

        total_area = fields.Float(string="Total Area (sqm)", readonly=True, compute="_compute_total_area", store=True)
        best_price = fields.Float(readonly=True,compute="_compute_best_price")
    
        active = fields.Boolean(default=True)
        state = fields.Selection(
                selection=[
                    ("new", "New"),
                    ("offer_received", "Offer received"),
                    ("offer_accepted", "Offer accepted"),
                    ("sold", "Sold"),
                    ("canceled", "Canceled"),
                ],
                default="new",
                copy=False,
                required=True,
        )

        property_type_id = fields.Many2one("estate.property.type", string="Property Type")

        salesman_id = fields.Many2one("res.users", string="Salesman")
        buyer_id = fields.Many2one("res.partner", string="Partner")
    
        offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

        _sql_constraints = [
            ('check_expected_price', 'CHECK(expected_price >= 0)', 'The expected price must me be at least 100.')
        ]

        @api.onchange("garden")
        def _onchange_garden(self):
            if self.garden:
                self.garden_area = 10
                self.garden_orientation = "north"
            else:
                self.garden_area = self.garden_orientation = False
                
        @api.depends("living_area", "garden_area")
        def _compute_total_area(self):
            self.total_area = self.living_area + self.garden_area
            
        @api.depends("offer_ids.price")
        def _compute_best_price(self):
            for property in self:
                if property.offer_ids:
                    property.best_price = max(property.offer_ids.mapped("price"))
                else:
                    property.best_price = 0

        def action_sell_property(self):
            for property in self:
                if property.state == "cancelled":
                    raise UserError(_("Cancelled properties cannot be sold!"))
                property.state = "sold"

        def action_cancel_property(self):
            self.state = "canceled"

        @api.constrains("selling_price", "expected_price")
        def _check_selling_price(self):
            for property in self:
                if (not float_is_zero(property.selling_price, precision_rounding=0.01) and 
                    float_compare(property.selling_price, 0.9 * property.expected_price, precision_rounding=0.01) < 0
                   ):
                    raise ValidationError(_("The selling price should not be lower than 90% of the expected price!"))

        @api.ondelete(at_uninstall=False)
        def _unlink_if_new_or_canceled(self):
            for property in self:
                if property.state not in ("new", "canceled"):
                    raise UserError(_("Only new or canceled property can be deleted!"))

        @api.model_create_multi
        def create(self, vals_list):
            for vals in vals_list:
                property = self.env["estate.property"]