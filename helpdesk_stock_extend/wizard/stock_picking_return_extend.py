# -*- coding: utf-8 -*-
# Part of Odoo. See ICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_round
import json

class ReturnPickingLine(models.TransientModel):
    _inherit = "stock.return.picking.line"

    wizard_ids = fields.Many2one('stock.return.picking', string="Wizard2")

class ReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    location_domain = fields.Char(string="domain location", compute='_domain_location_origin_id')
    location_origin_id = fields.Many2one(comodel_name='stock.location', string='Return Location')
    # picking_domain_ids = fields.Char(string="domain pickings", compute='_domain_pickings_id')
    picking_ids = fields.Many2many(comodel_name='stock.picking', string='Envio para devolver 2',
                                   domain="[('id', 'in', suitable_picking_ids)")
    product_return_moves_ids = fields.One2many('stock.return.picking.line', 'wizard_ids', 'Moves2')

    # Origin location domain
    @api.depends('suitable_picking_ids')
    def _domain_location_origin_id(self):
        a = []
        if self.suitable_picking_ids:
            for rec in self.suitable_picking_ids:
                a.append(rec.location_dest_id.id)
                self.location_domain = json.dumps([('id', "=", a)])
        else:
            self.location_domain = json.dumps([])

    # # pickings domain
    # @api.depends('location_origin_id')
    # def _domain_pickings_id(self):
    #     a = []
    #     if self.location_origin_id:
    #         for rec in self:
    #             rec.picking_domain_ids = json.dumps([('location_dest_id', '=', rec.location_origin_id.ids)])
    #     else:
    #         self.picking_domain_ids = json.dumps([])

    @api.onchange('picking_ids')
    def _onchange_picking_ids(self):
        move_dest_exists = False
        product_return_moves_ids = [(5,)]
        for rec in self.picking_ids:
            if rec and rec.state == 'done':
                raise UserError(_("You may only return Done pickings."))
        # In case we want to set specific default values (e.g. 'to_refund'), we must fetch the
        # default values for creation.
        line_fields = [f for f in self.env['stock.return.picking.line']._fields.keys()]
        product_return_moves_data_tmpl = self.env['stock.return.picking.line'].default_get(line_fields)
        for move in self.picking_ids:
            if move.move_lines.state == 'cancel':
                continue
            if move.move_lines.scrapped:
                continue
            if move.move_lines.move_dest_ids:
                move_dest_exists = True
            product_return_moves_data = dict(product_return_moves_data_tmpl)
            product_return_moves_data.update(self._prepare_stock_return_picking_line_vals_from_move_ids(move.move_lines))
            product_return_moves_ids.append((0, 0, product_return_moves_data))  # Se añade registro en la variable flotante
        if self.picking_ids and not product_return_moves_ids:
            raise UserError(
                _("No products to return (only lines in Done state and not fully returned yet can be returned)."))
        if self.picking_ids:
            self.product_return_moves_ids = product_return_moves_ids
            self.product_return_moves = product_return_moves_ids
            self.move_dest_exists = move_dest_exists
            self.parent_location_id = self.picking_ids.picking_type_id.warehouse_id and self.picking_ids.picking_type_id.warehouse_id.view_location_id.id or self.picking_ids.location_id.location_id.id
            self.original_location_id = self.picking_ids.location_id.id
            location_id = self.picking_ids.location_id.id
            if self.picking_ids.picking_type_id.return_picking_type_id.default_location_dest_id.return_location:
                location_id = self.picking_ids.picking_type_id.return_picking_type_id.default_location_dest_id.id
            self.location_id = location_id

    @api.model
    def _prepare_stock_return_picking_line_vals_from_move_ids(self, stock_move):
        quantity = stock_move.product_qty
        for move in stock_move.move_dest_ids:
            if move.origin_returned_move_id and move.origin_returned_move_id == stock_move:
                continue
            if move.state in ('partially_available', 'assigned'):
                quantity -= sum(move.move_line_ids.mapped('product_qty'))
            elif move.state in ('done'):
                quantity -= move.product_qty
        quantity = float_round(quantity, precision_rounding=stock_move.product_id.uom_id.rounding)
        a = self.env['stock.move'].search([('id', '=', stock_move.ids)])
        return {
            'product_id': stock_move.product_id.id,
            'quantity': quantity,
            'move_id': a,
            'uom_id': stock_move.product_id.uom_id.id,
        }

    def _prepare_picking_default_values(self):
        string = ''
        if self.picking_ids:
            for rec in self.picking_ids:
                string += ' [ ' + rec.name + ']'
        else:
            string = self.picking_id.name
        return {
            'move_lines': [],
            'picking_type_id': self.picking_id.picking_type_id.return_picking_type_id.id or self.picking_id.picking_type_id.id,
            'state': 'draft',
            'origin': _("Return of %s") % string,
            'location_id': self.picking_id.location_dest_id.id,
            'location_dest_id': self.location_id.id
        }


