# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions

class purchase_requisition_extend(models.Model):
    _inherit = 'purchase.requisition.line'

    qty_available = fields.Float(related='product_id.qty_available', string='Stock',
                             help='Muestra el stock del producto')

    inventory_product_qty = fields.Float(string='Cantidad inventario', help='Cantidad de pruductos que deseas sacar o mover de inventario')
    product_qty2 = fields.Float(string='Cantidad', help='Cantidad de pruductos a comprar')

    property_stock_inventory = fields.Many2one(comodel_name='stock.location', related='product_id.property_stock_inventory', string='Ubicación en inventario',
                                 help='Muestra la ubicación del producto en el inventario')

    picking_type_id = fields.Many2one(comodel_name='stock.picking.type', string='Tipo de operación', help='Ubicación a mover')

    default_location_dest_id = fields.Many2one(comodel_name='stock.location', string='Ubicación a mover',
                                               related='picking_type_id.default_location_dest_id', help='Ubicación a mover')

    show_picking = fields.Boolean(string='show',
                                  help='Mostrar/ocultar el button y smart button de solicitud de compra')

    name_picking = fields.Char(comodel_name='stock.location', related='product_id.name')


    @api.onchange('product_qty2', 'inventory_product_qty', 'product_qty')
    def _compute_product_qty(self):
        if self.product_qty2 <= self.qty_available:
            self.inventory_product_qty = self.product_qty2
            self.product_qty = 0
            self.show_picking = False
        else:
            self.inventory_product_qty = self.qty_available
            c = self.qty_available - self.product_qty2
            self.product_qty = abs(c)
            self.show_picking = True




































