# -*- coding: utf-8 -*-

from odoo import api, fields, models
import json

class purchase_requisition_line_extend(models.Model):
    _inherit = 'purchase.requisition.line'

    product_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', compute='_compute_product_qty')

    qty_available = fields.Float(related='product_id.qty_available', string='A mano',
                             help='Muestra la  cantidad a mano del producto en inventario')

    qty_available_location = fields.Float(string='Disponible',
                                 help='Muestra la cantidad disponible en la ubicación selecionada del producto')

    location_id_domain = fields.Char(compute="_compute_location_stock_picking", readonly=True, store=False)

    property_stock_inventory = fields.Many2one(comodel_name='stock.location',
                                               string='Ubicación en inventario',
                                               help='Muestra la ubicación del producto en el inventario',
                                               )
    inventory_product_qty = fields.Float(string='Cantidad inventario', compute='_compute_inventory_product_qty',
                                         help='Cantidad de pruductos que deseas sacar o mover de inventario')
    product_qty2 = fields.Float(string='Cantidad', help='Cantidad de pruductos a comprar')

    picking_type_id = fields.Many2one(comodel_name='stock.picking.type', string='Tipo de operación',
                                      domain="[('code', '=', 'internal')]")

    default_location_dest_id = fields.Many2one(comodel_name='stock.location', string='Ubicación a mover',
                                               related='picking_type_id.default_location_dest_id', help='Ubicación a mover')

    show_picking = fields.Boolean(string='show', related='requisition_id.show_picking',
                                  help='Mostrar/ocultar el button y smart button de solicitud de compra')

    name_picking = fields.Char(comodel_name='stock.location', related='product_id.name')

    # Función que aplica filtro dinamico de localización del producto en inventario
    @api.depends('product_id')
    def _compute_location_stock_picking(self):
        for rec in self:
            rec.location_id_domain = json.dumps(
                [('usage', '=', 'internal'), ('id', "=", rec.product_id.stock_quant.location_id.ids)]
            )

    #   Función que restablece ubicación y cantidad
    @api.onchange('product_id')
    def _compute_property_stock_inventory(self):
        self.property_stock_inventory = False
        self.qty_available_location = 0

    #   Función que calcula la cantidad de stock por ubicación
    @api.onchange('property_stock_inventory', 'show_picking')
    def _compute_qty_available_location(self):
        c = 0
        for rec in self.product_id.stock_quant:
            if rec.product_id == self.product_id and rec.location_id == self.property_stock_inventory:
                c = c + rec.available_quantity
            self.qty_available_location = c

    # Función que calcula la cantidad de inventario a mover
    @api.onchange('product_qty2')
    @api.depends('qty_available_location')
    def _compute_inventory_product_qty(self):
        for rec in self:
            if rec.product_qty2 <= rec.qty_available_location:
                rec.inventory_product_qty = rec.product_qty2
            else:
                rec.inventory_product_qty = rec.qty_available_location

    # Función que calcula la cantidad a comprar
    @api.onchange('product_qty2')
    @api.depends('qty_available_location')
    def _compute_product_qty(self):
        for rec2 in self:
            if rec2.product_qty2 > rec2.qty_available_location:
                rec2.product_qty = rec2.product_qty2 - rec2.qty_available_location
            else:
                rec2.product_qty = 0














































