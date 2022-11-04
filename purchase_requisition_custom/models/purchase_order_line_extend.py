from datetime import datetime, time
from odoo import fields, models, api
import json

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    image_product = fields.Binary(string='Imagen', related='product_id.image_1920')
    warehouse_id = fields.Many2one(comodel_name='stock.warehouse', string='A almacen',
                                   help='Almacen a mover')
    location_id = fields.Many2one(comodel_name='stock.location', string='De ubicación', compute='_compute_location_virtual_partner',
                                  help='Ubicación a mover, con filtro de almacane y ubicación interna, cliente')
    transit_location_id = fields.Many2one(comodel_name='stock.location', string='Ubicación de transito', store=True,
                                          help='Solo se permite una ubicación de transito por almacen')
    location_dest_id = fields.Many2one(comodel_name='stock.location', string='A ubicación',
                                               help='Ubicación a mover, con filtro de almacane y ubicación interna, cliente')
    location_dest_id_domain = fields.Char(compute="_compute_location_dest_id", readonly=True, store=False)
    requisition_id = fields.Many2one('purchase.requisition', string='Purchase Agreement', related='order_id.requisition_id')
    qty_received = fields.Float("Received Qty", compute='_compute_qty_received', inverse='_inverse_qty_received',
                                compute_sudo=True, store=True, digits='Product Unit of Measure')

    # Seleciona la ubicación origin la ubicación de proveedor
    def _compute_location_virtual_partner(self):
        virtual_partner_location = self.env['stock.location'].search([('usage', '=', 'supplier')], limit=1)
        self.location_id = virtual_partner_location

    # Seleciona la cuenta analitica
    @api.onchange('location_dest_id')
    def _compute_account_analytic_id(self):
        for rec in self:
            if rec.location_dest_id:
                rec.write({'account_analytic_id': rec.location_dest_id.account_analytic_id})
            else:
                rec.write({'account_analytic_id': False})

    # Dominio dinamico de ubicación de destino
    @api.depends('warehouse_id')
    def _compute_location_dest_id(self):
        for rec in self:
            rec.location_dest_id_domain = json.dumps(
                [('warehouse_id', '=', rec.warehouse_id.ids),
                 ('usage', '=', ['internal'])]
            )

    # Función que optiene la cantidad e productos en stock picking
    def _get_po_line_moves(self):
        self.ensure_one()
        moves = self.move_ids.filtered(lambda m: m.product_id == self.product_id and m.stage == 1)
        if self._context.get('accrual_entry_date'):
            moves = moves.filtered(lambda r: fields.Date.context_today(r, r.date) <= self._context['accrual_entry_date'])
        return moves








