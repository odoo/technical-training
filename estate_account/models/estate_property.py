from odoo import models, Command, fields

class EstateProperty(models.Model):
    _inherit = "estate.property"

    existe = fields.Text()
    
    def action_sold_property(self):
        # Agregar un print para verificar la ejecución
        print("Ejecutando action_sold en estate_account")

        # Llamar al método original
        result = super(EstateProperty, self).action_sold_property()

        # Verificar que hay un comprador antes de crear la factura
        if not self.buyer_id:
            print("No hay comprador asignado. No se creará la factura.")
            return result

        # Crear la factura
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',

            'journal_id': self.env['account.journal'].search([('type', '=', 'sale')], limit=1).id,  # Diario de ventas
            'invoice_line_ids': [
                Command.create({
                    'name': 'Venta de propiedad - Comisión',
                    'quantity': 1.0,
                    'price_unit': self.selling_price * 0.06,  # 6% del precio de venta
                }),
                Command.create({
                    'name': 'Gastos administrativos',
                    'quantity': 1.0,
                    'price_unit': 100.00,  # 100.00 adicionales
                }),
            ],
        })

        print(f"Factura creada: {invoice.id}")

        return result
