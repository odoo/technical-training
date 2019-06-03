from odoo import api, fields, models, exceptions



class Sessions(models.Model):
    _name = 'openacademy.session'
    _inherit = ['mail.thread']
    _description = 'Sessions'

    name = fields.Char('Title', required=True)
    active = fields.Boolean(default=True)

    instructor_id = fields.Many2one('res.partner', string="Instructor", domain=[('instructor', '=', True)])
    attendee_ids = fields.Many2many('res.partner', string="Atendees")
    course_id = fields.Many2one('openacademy.class', string="Course")

    session_date = fields.Date()

    max_student = fields.Integer('Max seats', related='instructor_id.max_student')

    taken_seats = fields.Float('Taken seats', compute='_compute_taken_seats')

    five_seats = fields.Boolean(default=True)

    currency_id = fields.Many2one('res.currency', 'Currency')

    price = fields.Float('Price')

    product_id = fields.Many2one('product.template', 'Product')

    is_paid = fields.Boolean('Is paid')

    state = fields.Selection([('draft',"Draft"),('confirmed',"Confirmed")], default='draft')



    # @api.depends('max_student', 'attendee_ids')
    # def _compute_taken_seats(self):
    #     for rec in self:
    #         rec.taken_seats = len(rec.attendee_ids)

    @api.multi
    def _draft_to_confirmed(self):
        for record in self:
            if (record.taken_seats / record.max_student) > 0.5 and record.state == 'draft':
                record.state = 'confirmed'
                record.message_post(body="Session changed to confirmed")

    @api.multi
    def write(self, values):
        result = super(Sessions,self).write(values)
        if 'attendee_ids' in values or 'max_student' in values:
            self._draft_to_confirmed()
        return result

    @api.depends('taken_seats', 'attendee_ids')
    def _compute_taken_seats(self):
        for rec in self:
            rec.taken_seats = len(rec.attendee_ids)    
        # if rec.taken_seats > 5:
        #     self.write({'state': 'confirmed'})        

    # @api.onchange('taken_seats')
    # def check_seats(self):
    #     if self.taken_seats > 5:
    #         return {'warning': {
    #             'title':   'Room full',
    #             'message': 'Too many attendees'
    #         }}

    # @api.constrains('max_student', 'attendee_ids')
    # def _check_seats(self):
    #     for record in self:
    #         if record.taken_seats > 5:
    #             raise exceptions.ValidationError('Too many attendees')
    @api.multi
    def create_invoice(self):
        self.AccountInvoice = self.env['account.invoice']

        self.invoice = self.AccountInvoice.search([
            ('partner_id', '=', self.instructor_id.id)
        ], limit=1)

        if not self.invoice:
            self.invoice = self.AccountInvoice.create({
                'partner_id': self.instructor_id.id,
            })  

        expense_account = self.env['account.account'].search([('user_type_id', '=', self.env.ref('account.data_account_type_expenses').id)], limit=1)
        self.env['account.invoice.line'].create({
            'invoice_id': self.invoice.id,
            'product_id': self.product_id.id,
            'price_unit': self.product_id.lst_price,
            'account_id': expense_account.id,
            'name':       'Session',
            'quantity':   1,
        })

        self.write({'is_paid': True})

    



