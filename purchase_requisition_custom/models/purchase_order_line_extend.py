from odoo import fields, models, api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    image_product = fields.Binary(string='Imagen', related='product_id.image_1920')
    warehouse_id = fields.Many2one(comodel_name='stock.warehouse', string='A almacen',
                                   domain="[('usage', '=', 'supplier'), ('available_requisition', '=', 'True')]",
                                   help='Almacen a mover')
    location_id = fields.Many2one(comodel_name='stock.location', string='De ubicación', compute='_compute_location_virtual_partner',
                                  help='Ubicación a mover, con filtro de almacane y ubicación interna, cliente')
    transit_location_id = fields.Many2one(comodel_name='stock.location', domain="[('usage', '=', 'transit')]",
                                          string='Ubicación de transito',
                                          help='Solo se permite una ubicación de transito por almacen')
    location_dest_id = fields.Many2one(comodel_name='stock.location', string='A ubicación',
                                               help='Ubicación a mover, con filtro de almacane y ubicación interna, cliente')

    def _compute_location_virtual_partner(self):
        virtual_partner_location = self.env['stock.location'].search([('usage', '=', 'supplier')], limit=1)
        self.location_id = virtual_partner_location




