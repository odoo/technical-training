from odoo import models, fields, api
from odoo.exceptions import ValidationError
import base64

class BakkerVerkoop(models.Model):
    _name = "bakker_verkoop"
    _description = "Verkoop van bakkerij koeken"
    _inherit = ['mail.thread', 'mail.activity.mixin'] 
    _order = "verkoop_datum desc"
    
    
    name = fields.Char(string="Verkoop Nummer", required=True, default="Nieuw", tracking=True)
    koek_id = fields.Many2one('bakker_koeken', string="Koek", required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string="Klant", required=True, tracking=True)
    klant_email = fields.Char(string="Email", related='partner_id.email', readonly=True)
    klant_telefoon = fields.Char(string="Telefoon", related='partner_id.phone', readonly=True)
    aantal = fields.Integer(string="Aantal", required=True, default=1, tracking=True)
    prijs_per_stuk = fields.Float(string="Prijs per stuk", required=True, tracking=True)
    korting_percentage = fields.Float(string="Korting (%)", default=0.0, tracking=True)
    subtotaal = fields.Float(string="Subtotaal", compute="_compute_totalen", store=True)
    korting_bedrag = fields.Float(string="Korting Bedrag", compute="_compute_totalen", store=True)
    totaal_bedrag = fields.Float(string="Totaal Bedrag", compute="_compute_totalen", store=True, tracking=True)
    verkoop_datum = fields.Datetime(string="Verkoop Datum", default=fields.Datetime.now, tracking=True)
    status = fields.Selection([
        ('concept', 'Concept'),
        ('bevestigd', 'Bevestigd'),
        ('betaald', 'Betaald'),
        ('geannuleerd', 'Geannuleerd')
    ], string="Status", default='concept', tracking=True)
    betaal_methode = fields.Selection([
        ('cash', 'Contant'),
        ('card', 'Bankkaart'),
        ('digital', 'Digitaal')
    ], string="Betaal Methode", tracking=True)
    opmerkingen = fields.Text(string="Opmerkingen")
    
    @api.model
    def create(self, vals):
        if vals.get('name', 'Nieuw') == 'Nieuw':
            vals['name'] = self.env['ir.sequence'].next_by_code('bakker.verkoop') or f"VK{fields.Date.today().strftime('%Y%m%d')}-{len(self.search([]))}"
        return super().create(vals)
    
    @api.depends('aantal', 'prijs_per_stuk', 'korting_percentage')
    def _compute_totalen(self):
        for record in self:
            record.subtotaal = record.aantal * record.prijs_per_stuk
            record.korting_bedrag = record.subtotaal * (record.korting_percentage / 100)
            record.totaal_bedrag = record.subtotaal - record.korting_bedrag
    
    @api.constrains('aantal')
    def _check_voorraad(self):
        for record in self:
            if record.status == 'concept' and record.aantal > record.koek_id.voorraad_koek:
                raise ValidationError(f"Niet genoeg voorraad! Beschikbaar: {record.koek_id.voorraad_koek}")
    
    def action_bevestig_verkoop(self):
        """Bevestig de verkoop en update voorraad"""
        for record in self:
            if record.status != 'concept':
                raise ValidationError("Alleen concept verkopen kunnen bevestigd worden.")
            
            # Check voorraad nogmaals
            if record.aantal > record.koek_id.voorraad_koek:
                raise ValidationError(f"Niet genoeg voorraad! Beschikbaar: {record.koek_id.voorraad_koek}")
            
            # Update voorraad
            record.koek_id.voorraad_koek -= record.aantal
            record.status = 'bevestigd'
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': '✅ Verkoop Bevestigd!',
                'message': f'Verkoop {self.name} is bevestigd en voorraad is bijgewerkt',
                'type': 'success',
            }
        }
    
    def action_markeer_betaald(self):
        """Markeer als betaald en verstuur factuur email"""
        for record in self:
            if record.status != 'bevestigd':
                raise ValidationError("Alleen bevestigde verkopen kunnen als betaald gemarkeerd worden.")
            record.status = 'betaald'
            
            # Verstuur factuur email als klant een email adres heeft
            if record.partner_id.email:
                try:
                    # Zoek email template
                    template = self.env.ref('Bakker.email_template_bakker_factuur', raise_if_not_found=False)
                    if template:
                        # Verstuur email
                        template.send_mail(record.id, force_send=True)
                        
                        # Log activiteit (nu werkt message_post)
                        record.message_post(
                            body=f"Factuur email verstuurd naar {record.partner_id.email}",
                            subject="Factuur Email Verstuurd"
                        )
                except Exception as e:
                    # Log fout maar stop proces niet
                    record.message_post(
                        body=f"Fout bij versturen email: {str(e)}",
                        subject="Email Fout"
                    )
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': '💰 Betaling Ontvangen!',
                'message': f'Verkoop {self.name} is gemarkeerd als betaald' + (f' en factuur is verstuurd naar {self.partner_id.email}' if self.partner_id.email else ''),
                'type': 'success',
            }
        }
    
    def action_annuleer(self):
        """Annuleer verkoop en herstel voorraad"""
        for record in self:
            if record.status == 'betaald':
                raise ValidationError("Betaalde verkopen kunnen niet geannuleerd worden.")
            
            # Herstel voorraad als verkoop bevestigd was
            if record.status == 'bevestigd':
                record.koek_id.voorraad_koek += record.aantal
            
            record.status = 'geannuleerd'
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': '❌ Verkoop Geannuleerd',
                'message': f'Verkoop {self.name} is geannuleerd en voorraad is hersteld',
                'type': 'warning',
            }
        }
    
    def action_print_factuur(self):
        """Print factuur PDF"""
        return self.env.ref('Bakker.report_bakker_factuur').report_action(self)
    
    def action_open_print_wizard(self):
        """Open standaard print wizard voor factuur"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Print Opties',
            'res_model': 'base.document.layout',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_report_template': 'web.external_layout_standard',
                'active_ids': self.ids,
                'active_model': 'bakker_verkoop',
                'report_action': self.env.ref('Bakker.report_bakker_factuur').id,
            }
        }
    
    def action_configure_print(self):
        """Open document layout configuratie voor factuur"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Configure Document Layout',
            'res_model': 'base.document.layout',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_report_layout': 'web.external_layout_standard',
                'default_logo': True,
                'default_company_details': True,
                'active_ids': self.ids,
                'active_model': 'bakker_verkoop',
                'report_action': self.env.ref('Bakker.report_bakker_factuur').id,
            }
        }
    
    def action_print_with_layout(self):
        """Print factuur met document layout opties"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Print Factuur',
            'res_model': 'base.document.layout',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_report_layout': 'web.external_layout_standard',
                'default_logo': True,
                'default_company_details': True,
                'active_ids': self.ids,
                'active_model': 'bakker_verkoop',
                'report_action': self.env.ref('Bakker.report_bakker_factuur').report_action(self),
                'close_on_report_download': True,
            }
        }
        
        
class BakkerVerkoopWizard(models.TransientModel):
    _name = 'bakker.verkoop.wizard'
    _description = 'Wizard voor het verkopen van koeken'
    
    koek_id = fields.Many2one('bakker_koeken', string='Koek', required=True)
    partner_id = fields.Many2one('res.partner', string='Klant', required=True)
    aantal = fields.Integer(string='Aantal', required=True, default=1)
    prijs_per_stuk = fields.Float(string='Prijs per stuk', required=True)
    korting_percentage = fields.Float(string='Korting (%)', default=0.0)
    finale_prijs = fields.Float(string='Finale Prijs per stuk', compute='_compute_finale_prijs')
    totaal_bedrag = fields.Float(string='Totaal Bedrag', compute='_compute_totaal_bedrag')
    beschikbare_voorraad = fields.Integer(related='koek_id.voorraad_koek', string='Beschikbare Voorraad')
    direct_betaald = fields.Boolean(string='Direct Betaald', default=True)
    betaal_methode = fields.Selection([
        ('cash', 'Contant'),
        ('card', 'Bankkaart'),
        ('digital', 'Digitaal')
    ], string="Betaal Methode", default='cash')
    
    # Gerelateerde velden van de klant
    klant_email = fields.Char(string="Email", related='partner_id.email', readonly=True)
    klant_telefoon = fields.Char(string="Telefoon", related='partner_id.phone', readonly=True)
    klant_adres = fields.Char(string="Adres", related='partner_id.street', readonly=True)
    klant_stad = fields.Char(string="Stad", related='partner_id.city', readonly=True)
    
    @api.depends('prijs_per_stuk', 'korting_percentage')
    def _compute_finale_prijs(self):
        for record in self:
            if record.korting_percentage:
                record.finale_prijs = record.prijs_per_stuk * (1 - record.korting_percentage / 100)
            else:
                record.finale_prijs = record.prijs_per_stuk
    
    @api.depends('aantal', 'finale_prijs')
    def _compute_totaal_bedrag(self):
        for record in self:
            record.totaal_bedrag = record.aantal * record.finale_prijs
    
    @api.constrains('aantal')
    def _check_voorraad(self):
        for record in self:
            if record.aantal > record.koek_id.voorraad_koek:
                raise ValidationError(f"Niet genoeg voorraad! Beschikbaar: {record.koek_id.voorraad_koek}")
    
    def action_verkoop(self):
        """Voer de verkoop uit"""
        verkoop = self.env['bakker_verkoop'].create({
            'koek_id': self.koek_id.id,
            'partner_id': self.partner_id.id,
            'aantal': self.aantal,
            'prijs_per_stuk': self.finale_prijs,
            'korting_percentage': self.korting_percentage,
            'betaal_methode': self.betaal_methode,
        })
        
        # Bevestig verkoop
        verkoop.action_bevestig_verkoop()
        
        # Markeer als betaald indien gewenst
        if self.direct_betaald:
            verkoop.action_markeer_betaald()
        
        return {
            'name': 'Nieuwe Verkoop',
            'type': 'ir.actions.act_window',
            'res_model': 'bakker_verkoop',
            'res_id': verkoop.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_create_new_customer(self):
        """Maak een nieuwe klant aan"""
        return {
            'name': 'Nieuwe Klant',
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_is_company': False, 'default_customer_rank': 1}
        }

class BakkerFactuurWizard(models.TransientModel):
    _name = 'bakker.factuur.wizard'
    _description = 'Factuur Preview Wizard'
    
    verkoop_id = fields.Many2one('bakker_verkoop', string='Verkoop', required=True)
    pdf_data = fields.Binary(string='PDF Data')
    pdf_filename = fields.Char(string='Filename')
    show_preview = fields.Boolean(string='Toon Preview', default=True)
    
    def action_preview_factuur(self):
        """Genereer PDF preview"""
        report = self.env.ref('Bakker.report_bakker_factuur')
        pdf_content, _ = report._render_qweb_pdf([self.verkoop_id.id])
        
        self.pdf_data = base64.b64encode(pdf_content)
        self.pdf_filename = f"Factuur_{self.verkoop_id.name}.pdf"
        self.show_preview = True
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Factuur Preview',
            'res_model': 'bakker.factuur.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
            'context': {'show_preview': True}
        }
    
    def action_download_factuur(self):
        """Download de PDF"""
        if not self.pdf_data:
            self.action_preview_factuur()
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content?model=bakker.factuur.wizard&id={self.id}&field=pdf_data&filename_field=pdf_filename&download=true',
            'target': 'self',
        }
    
    def action_print_factuur(self):
        """Print de PDF via browser"""
        if not self.pdf_data:
            self.action_preview_factuur()
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content?model=bakker.factuur.wizard&id={self.id}&field=pdf_data&filename_field=pdf_filename',
            'target': 'new',
        }