from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import ValidationError

class BakkerKoeken(models.Model):
    _name = "bakker_koeken"
    _description = "Bakker zijn lekkere koeken"
    _order = "name_koek asc"

    name_koek = fields.Char(string="Naam van de koek", required=True, help="Vul hier de naam van de koek in")
    prijs_koek = fields.Float(string="Prijs van de koek", required=True, help="Vul hier de prijs van de koek in")
    voorraad_koek = fields.Integer(string="Voorraad van de koek", required=True , default=10)
    vervaldatum_koek = fields.Date(string="Vervaldatum van de koek", required=True, help="Vul hier de vervaldatum van de koek in", default=lambda self: fields.Date.today() + timedelta(days=30), readonly=True)
    aankoopdatum_koek = fields.Date(string="Aankoopdatum van de koek", default=fields.Date.today, help="Vul hier de aankoopdatum van de koek in", readonly=True)
    categorie_koek_id = fields.Many2one('bakker_koeken_categorie', string="Categorie van de koek", required=True, help="Selecteer hier de categorie van de koek")
    pudding_koek = fields.Boolean(string="Bevat pudding", default=False, help="Vink dit aan als de koek pudding bevat")
    totaal_inventarisatie = fields.Float(string="Totale inventarisatie waarde", compute="_compute_totaal_inventarisatie", store=True, inverse="_inverse_totaal_inventarisatie", help="Totale waarde van de koek in inventarisatie (prijs * voorraad)")
    tags_ids = fields.Many2many('bakker_koeken_tags', string="Tags", help="Selecteer hier de tags voor de koek")
    
    # Nieuwe verkoop gerelateerde velden
    verkoop_ids = fields.One2many('bakker_verkoop', 'koek_id', string='Verkopen')
    totaal_verkocht = fields.Integer(string='Totaal Verkocht', compute='_compute_verkoop_stats', store=True)
    totaal_omzet = fields.Float(string='Totaal Omzet', compute='_compute_verkoop_stats', store=True)
    verkoop_count = fields.Integer(string='Aantal Verkopen', compute='_compute_verkoop_count')
    
    @api.depends('verkoop_ids.aantal', 'verkoop_ids.totaal_bedrag', 'verkoop_ids.status')
    def _compute_verkoop_stats(self):
        for record in self:
            betaalde_verkopen = record.verkoop_ids.filtered(lambda v: v.status == 'betaald')
            record.totaal_verkocht = sum(betaalde_verkopen.mapped('aantal'))
            record.totaal_omzet = sum(betaalde_verkopen.mapped('totaal_bedrag'))
    
    @api.depends('verkoop_ids')
    def _compute_verkoop_count(self):
        for record in self:
            record.verkoop_count = len(record.verkoop_ids)
    
    @api.onchange('prijs_koek', 'voorraad_koek')
    def _onchange_prijs_koek(self):
        self._compute_totaal_inventarisatie()
    
    @api.onchange('totaal_inventarisatie')
    def _onchange_totaal_inventarisatie(self):
        self._inverse_totaal_inventarisatie()
    
    @api.depends('prijs_koek', 'voorraad_koek')
    def _compute_totaal_inventarisatie(self):
        for record in self:
            record.totaal_inventarisatie = record.prijs_koek * record.voorraad_koek
    
    def _inverse_totaal_inventarisatie(self):
        for record in self:
            if record.prijs_koek != 0:
                record.voorraad_koek = record.totaal_inventarisatie / record.prijs_koek
            else:
                record.voorraad_koek = 0
            
    @api.constrains('voorraad_koek', 'prijs_koek')
    def _check_non_negative(self):
        for record in self:
            if record.voorraad_koek < 0:
                raise ValidationError("Voorraad van de koek kan niet negatief zijn.")
            if record.prijs_koek < 0:
                raise ValidationError("Prijs van de koek kan niet negatief zijn.")
        
    def action_voorraad_bijvullen(self):
        """Vul voorraad bij met standaard hoeveelheid"""
        for record in self:
            record.voorraad_koek += 20
            record.aankoopdatum_koek = fields.Date.today()
            
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
            'params': {
                'title': 'Voorraad Bijgevuld!',
                'message': f'Voorraad van {self.name_koek} is bijgevuld met 20 stuks',
                'type': 'success',
            }
        }
    
    def action_uitverkocht(self):
        """Markeer als uitverkocht"""
        for record in self:
            record.voorraad_koek = 0
        return True
    
    def action_verse_batch(self):
        """Maak nieuwe verse batch - duplicate record"""
        for record in self:
            # Maak een kopie van het huidige record
            new_batch = record.copy({
                'voorraad_koek': 30,
                'aankoopdatum_koek': fields.Date.today(),
                'vervaldatum_koek': fields.Date.today() + timedelta(days=30),
                'name_koek': f"{record.name_koek} - Verse Batch",
            })
            
            vers_tag = self.env['bakker_koeken_tags'].search([('name', '=', 'Vers')], limit=1)
            if vers_tag:
                new_batch.tags_ids = [(4, vers_tag.id)]
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Nieuwe Verse Batch',
            'res_model': 'bakker_koeken',
            'res_id': new_batch.id,
            'view_mode': 'form',
            'target': 'current',
            'effect': {
                'fadeout': 'slow',
                'message': '🍪 Verse batch aangemaakt!',
                'type': 'rainbow_man',
            }
        }
    
    def action_mark_populair(self):
        """Markeer als populair"""
        populair_tag = self.env['bakker_koeken_tags'].search([('name', '=', 'Populair')], limit=1)
        for record in self:
            if populair_tag:
                record.tags_ids = [(4, populair_tag.id)]
        return True
    
    def action_seizoen_special(self):
        """Markeer als seizoensspecial"""
        seizoen_tag = self.env['bakker_koeken_tags'].search([('name', '=', 'Seizoen')], limit=1)
        for record in self:
            if seizoen_tag:
                record.tags_ids = [(4, seizoen_tag.id)]
            record.prijs_koek = record.prijs_koek * 1.15  # 15% prijsverhoging
        return True
    
    def action_kwaliteitscontrole(self):
        """Doe kwaliteitscontrole"""
        import random
        for record in self:
            if random.choice([True, False]):  # 50% kans
                
                vers_tag = self.env['bakker_koeken_tags'].search([('name', '=', 'Vers')], limit=1)
                if vers_tag:
                    record.tags_ids = [(4, vers_tag.id)]
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': '✅ Kwaliteitscontrole Voltooid',
                'message': 'Kwaliteit gecontroleerd en goedgekeurd!',
                'type': 'info',
            }
        }
    
    def action_view_low_stock(self):
        """Toon koeken met lage voorraad"""
        action = self.env.ref('Bakker.bakker_koeken_action').read()[0]
        action['domain'] = [('voorraad_koek', '<=', 10)]
        action['context'] = {'search_default_filter_voorraad_laag': 1}
        return action
    
    def action_verkoop_rapport(self):
        """Genereer verkoop rapport"""
        return {
            'name': 'Verkoop Rapport',
            'type': 'ir.actions.act_window',
            'res_model': 'bakker_koeken',
            'view_mode': 'pivot,graph',
            'context': {
                'group_by': ['categorie_koek_id'],
            }
        }
    
    def action_verkoop_koek(self):
        """Open wizard om koeken te verkopen"""
        return {
            'name': 'Koek Verkopen',
            'type': 'ir.actions.act_window',
            'res_model': 'bakker.verkoop.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_koek_id': self.id,
                'default_prijs_per_stuk': self.prijs_koek,
            }
        }
    
    def action_view_verkopen(self):
        """Toon alle verkopen voor deze koek"""
        return {
            'name': f'Verkopen voor {self.name_koek}',
            'type': 'ir.actions.act_window',
            'res_model': 'bakker_verkoop',
            'view_mode': 'list,form',
            'domain': [('koek_id', '=', self.id)],
            'context': {'default_koek_id': self.id}
        }
    
    def action_snelle_verkoop(self):
        """Snelle verkoop - direct 1 koek verkopen"""
        if self.voorraad_koek <= 0:
            raise ValidationError("Geen voorraad beschikbaar!")
        
        # Zoek of maak een standaard walk-in klant
        walk_in_klant = self.env['res.partner'].search([('name', '=', 'Walk-in klant')], limit=1)
        if not walk_in_klant:
            walk_in_klant = self.env['res.partner'].create({
                'name': 'Walk-in klant',
                'is_company': False,
                'customer_rank': 1,
                'street': 'Bakkerij',
                'email': 'walkin@bakkerij.local'
            })
        
        verkoop = self.env['bakker_verkoop'].create({
            'koek_id': self.id,
            'partner_id': walk_in_klant.id,
            'aantal': 1,
            'prijs_per_stuk': self.prijs_koek,
            'betaal_methode': 'cash',
        })
        
        verkoop.action_bevestig_verkoop()
        verkoop.action_markeer_betaald()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': '💰 Verkoop Voltooid!',
                'message': f'1x {self.name_koek} verkocht voor €{self.prijs_koek}',
                'type': 'success',
            }
        }

