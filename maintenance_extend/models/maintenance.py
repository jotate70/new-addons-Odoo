# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _
import json

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'
    _description = 'Maintenance Equipment'
    _check_company_auto = True

    equipment_assign_to = fields.Selection(
        [('department', 'Department'), ('employee', 'Employee'), ('customer', 'Cliente'), ('other', 'Other')],
        string='Used By',
        required=True,
        default='employee')
    product_domain = fields.Char(compute="_compute_product_domain", readonly=True, store=False, domain='_compute_product_domain')
    product_name = fields.Many2one(comodel_name='product.product', string='Producto', domain='product_domain')
    lot_id = fields.Many2one(comodel_name='stock.production.lot', string='Lot/Serial Number', index=True, check_company=True)
    lot_id_domain = fields.Char(string='Lot/Serial Number domain', compute='_domain_lot_id')
    plaque_id = fields.Many2one(comodel_name='stock_production_plaque', string='Placa')
    tracking = fields.Selection([
        ('serial', 'By Unique Serial Number'),
        ('lot', 'By Lots'),
        ('none', 'No Tracking')], string="Tracking",
        help="Ensure the traceability of a storable product in your warehouse.", default='none', related='product_name.product_tmpl_id.tracking')
    location_origin = fields.Many2one(comodel_name='location_warehouse', string='Locación',
                               help='Muestra la ubicación de la ciudad/locación del producto')
    warehouse_domain = fields.Char(compute="_compute_warehouse_domain", readonly=True, store=False)
    warehouse_id = fields.Many2one(comodel_name='stock.warehouse', string='Almacen', domain='warehouse_domain',
                                   help='Almacen a mover')
    location_domain = fields.Char(compute="_compute_location_domain", readonly=True, store=False)
    location_id = fields.Many2one(comodel_name='stock.location', string='Ubicación', domain='location_domain',
                                  help='Ubicación donde se encuentra el producto')

    # Función que aplica filtro dinamico serial
    @api.depends('product_name')
    def _domain_lot_id(self):
        product = self.env['stock.production.lot'].search(
            [('product_id', "=", self.product_name.ids), ('product_qty', '>', 0)])
        for rec in self:
            if rec.product_name:
                rec.lot_id_domain = json.dumps([('id', "=", product.ids)])
            else:
                rec.lot_id_domain = json.dumps([])

    # Filtro dinamico de producto
    @api.depends('location_id')
    def _compute_product_domain(self):
        stock_quant = self.env['stock.quant'].search([('location_id', "=", self.location_id.ids), ('quantity', '>', 0)])
        for rec in self:
            rec.product_domain = json.dumps(
                [('id', '=', stock_quant.product_id.ids)]
            )

    # Filtro dinamico de almacen
    @api.depends('location_origin')
    def _compute_warehouse_domain(self):
        for rec in self:
            rec.warehouse_domain = json.dumps(
                [('location_id', '=', rec.location_origin.id)]
            )

    # Filtro dinamico de ubicación
    @api.depends('warehouse_id')
    def _compute_location_domain(self):
        for rec in self:
            rec.location_domain = json.dumps(
                [('warehouse_id', '=', rec.warehouse_id.id), ('usage', '=', ['internal', 'customer'])]
            )

    # product reset
    @api.onchange('location_id')
    def _reset_compute_product_name(self):
        if self.location_id and self.product_name:
            return
        else:
            self.product_name = False
            self.name = False
            self.lot_id = False
            self.plaque_id = False
            self.serial_no = False
            self.location = False

    @api.onchange('product_name')
    def _reset_lot_id(self):
        if self.tracking == 'none':
            self.lot_id = False
            self.plaque_id = False
            self.serial_no = False

    @api.onchange('product_name')
    def _update_display_name(self):
        self.write({'name': self.product_name.display_name})

    @api.onchange('lot_id')
    def _select_product_name(self):
        self.write({'plaque_id': False})
        self.write({'plaque_id': self.lot_id.plaque_id})
        self.write({'product_name': self.lot_id.product_id})
        if self.lot_id:
            self.write({'serial_no': False})
            self.write({'serial_no': self.lot_id.name})
            self.location_id = self.lot_id.quant_ids.filtered(
                lambda p: p.lot_id == self.lot_id and p.usage in ['internal', 'supplier', 'customer']).mapped('location_id')
            self.warehouse_id = self.lot_id.quant_ids.filtered(
                lambda p: p.lot_id == self.lot_id and p.usage in ['internal', 'supplier', 'customer']).mapped('warehouse_id')
            self.location_origin = self.lot_id.quant_ids.filtered(
                lambda p: p.lot_id == self.lot_id and p.usage in ['internal', 'supplier', 'customer']).mapped('location')










