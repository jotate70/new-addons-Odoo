# -*- coding: utf-8 -*-
# Part of Odoo. See ICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_round
import json

class ReturnPickingLine2(models.TransientModel):
    _name = "return_picking_line2"
    _rec_name = 'product_id'
    _description = 'Return Picking Line 2'

    product_id = fields.Many2one('product.product', string="Product", required=True)
    quantity = fields.Float("Quantity", digits='Product Unit of Measure', required=True)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', related='product_id.uom_id')
    wizard_id = fields.Many2one('stock.return.picking', string="Wizard")
    move_id = fields.Many2one('stock.move', "Move")
    warehouse_id = fields.Many2one(comodel_name='stock.warehouse', string='De almacen', help='Almacen de origen')
    location_origin_id = fields.Many2one(comodel_name='stock.location', string='Return Location',
                                         domain="location_domain")
    stock_quant_domain = fields.Char(string="domain stock quant", related='wizard_id.stock_quant_domain')
    stock_quant_ids = fields.Many2many(comodel_name='stock.quant', string='Stock Quant')

class ReturnPickingLine(models.TransientModel):
    _inherit = 'stock.return.picking.line'

    warehouse_id = fields.Many2one(comodel_name='stock.warehouse', string='De almacen', help='Almacen de origen')
    location_origin_id = fields.Many2one(comodel_name='stock.location', string='Return Location',
                                         domain="location_domain")
    stock_quant_ids = fields.Many2many(comodel_name='stock.quant', string='Stock Quant')

class ReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    warehouse_id = fields.Many2one(comodel_name='stock.warehouse', string='De almacen', help='Almacen de origen')
    type_return = fields.Selection([('picking', 'Por Transferencias'),
                                    ('product', 'Por producto')], store=True,
                                   string='Return Type', help='Indica el tipo de devolución', default="picking")
    location_domain = fields.Char(string="domain location", compute='_domain_location_origin_id')
    location_origin_id = fields.Many2one(comodel_name='stock.location', string='Return Location',
                                         domain="location_domain")
    picking_domain_ids = fields.Char(string="domain pickings", compute='_domain_pickings_id')
    stock_picking_ids = fields.Many2many(comodel_name='stock.picking', string='Envio para devolver 2',
                                         domain="picking_domain_ids")
    stock_quant_domain = fields.Char(string="domain stock quant", compute='_domain_stock_quant_ids')
    stock_quant_ids = fields.Many2many(comodel_name='stock.quant', string='Stock Quant', domain='stock_quant_domain')
    product_return_moves2 = fields.One2many('return_picking_line2', 'wizard_id', 'Moves')
    demo = fields.Char('demo')
    demo2 = fields.Char('demo2')
    demo3 = fields.Char('demo3')
    demo4 = fields.Char('demo4')

    @api.onchange('stock_quant_ids')
    def _compute_stock_picking(self):
        a = []
        b = []
        qty = 0
        if self.product_return_moves2:
            self.product_return_moves2 = False
        for rec in self.mapped('stock_quant_ids').product_id.ids:
            qty = 0
            product = self.env['stock.quant'].search([('product_id', '=', rec), ('usage', '=', 'internal'),
                                                      ('location_id.usage', '=', 'internal'),
                                                      ('available_quantity', '>', 0.0)])
            c = self.mapped('stock_quant_ids').filtered(lambda ml: ml.product_id == rec).product_id.ids
            for rec2 in product:
                qty = rec2.quantity + qty
            b.append({'product_id': rec,
                      'quantity': qty,
                      })
            self.write({'product_return_moves2': [(0, 0, {'product_id': rec,
                      'quantity': qty,
                      })]})
        self.demo = b
        self.demo2 = qty


    @api.onchange('location_origin_id', 'type_return')
    def _reset_stock_picking_ids(self):
        for rec in self:
            if rec.ticket_id != False:
                rec.stock_picking_ids = False
                rec.product_return_moves = False

    @api.onchange('warehouse_id')
    def _reset_location_origin_id(self):
        self.location_origin_id = False

    # Stock quant domain
    @api.depends('location_origin_id')
    def _domain_stock_quant_ids(self):
        if self.location_origin_id:
            for rec in self:
                rec.stock_quant_domain = json.dumps(
                    [('location_id', "=", rec.location_origin_id.ids), ('usage', '=', 'internal'),
                     ('location_id.usage', '=', 'internal'), ('available_quantity', '>', 0.0)])
        else:
            self.stock_quant_domain = json.dumps([])

    # Origin location domain
    @api.depends('warehouse_id')
    def _domain_location_origin_id(self):
        if self.suitable_picking_ids:
            for rec in self:
                rec.location_domain = json.dumps([('id', "=", rec.mapped('suitable_picking_ids').location_dest_id.ids),
                                                  ('warehouse_id', '=', self.warehouse_id.ids)])
        else:
            self.location_domain = json.dumps([])

    # pickings domain
    @api.depends('location_origin_id')
    def _domain_pickings_id(self):
        if self.location_origin_id:
            for rec in self:
                rec.picking_domain_ids = json.dumps([('id', 'in', self.mapped('suitable_picking_ids').filtered(lambda m: m.location_dest_id == rec.location_origin_id).ids)])
        else:
            self.picking_domain_ids = json.dumps([])

    @api.onchange('stock_picking_ids')
    def _onchange_stocok_picking_ids(self):
        move_dest_exists = False
        product_return_moves = [(5,)]
        for rec in self.stock_picking_ids:
            if rec and rec.state == 'done':
                raise UserError(_("You may only return Done pickings."))
        # In case we want to set specific default values (e.g. 'to_refund'), we must fetch the
        # default values for creation.
        line_fields = [f for f in self.env['stock.return.picking.line']._fields.keys()]
        product_return_moves_data_tmpl = self.env['stock.return.picking.line'].default_get(line_fields)
        for move in self.stock_picking_ids:
            if move.move_lines.state == 'cancel':
                continue
            if move.move_lines.scrapped:
                continue
            if move.move_lines.move_dest_ids:
                move_dest_exists = True
            product_return_moves_data = dict(product_return_moves_data_tmpl)
            product_return_moves_data.update(self._prepare_stock_return_picking_line_vals_from_move_ids(move.move_lines))
            product_return_moves.append((0, 0, product_return_moves_data))  # Se añade registro en la variable flotante
        if self.stock_picking_ids and not product_return_moves:
            raise UserError(
                _("No products to return (only lines in Done state and not fully returned yet can be returned)."))
        if self.stock_picking_ids:
            self.product_return_moves = product_return_moves
            self.product_return_moves = product_return_moves
            self.move_dest_exists = move_dest_exists
            self.parent_location_id = self.stock_picking_ids.picking_type_id.warehouse_id and self.stock_picking_ids.picking_type_id.warehouse_id.view_location_id.id or self.stock_picking_ids.location_id.location_id.id
            self.original_location_id = self.stock_picking_ids.location_id.id
            location_id = self.stock_picking_ids.location_id.id
            if self.stock_picking_ids.picking_type_id.return_picking_type_id.default_location_dest_id.return_location:
                location_id = self.stock_picking_ids.picking_type_id.return_picking_type_id.default_location_dest_id.id
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
        # Stock picking origin concatenate
        if self.picking_id:
            return {
                'move_lines': [],
                'picking_type_id': self.picking_id.picking_type_id.return_picking_type_id.id or self.picking_id.picking_type_id.id,
                'state': 'draft',
                'origin': _("Return of %s") % self.picking_id.name,
                'location_id': self.picking_id.location_dest_id.id,
                'location_dest_id': self.location_id.id
            }
        string = ''
        if self.stock_picking_ids:
            for rec in self.stock_picking_ids:
                string += ' [ ' + rec.name + ']'
                type_operation = rec.picking_type_id.return_picking_type_id.id or rec.picking_type_id.id
            return {
                'move_lines': [],
                'picking_type_id': type_operation,
                'state': 'draft',
                'origin': _("Return of %s") % string,
                'location_id': self.location_origin_id.id,
                'location_dest_id': self.location_id.id,
            }

    def _create_returns(self):
        # TODO sle: the unreserve of the next moves could be less brutal
        for return_move in self.product_return_moves.mapped('move_id'):
            return_move.move_dest_ids.filtered(lambda m: m.state not in ('done', 'cancel'))._do_unreserve()

        # create new picking for returned products
        if self.picking_id:
            new_picking = self.picking_id.copy(self._prepare_picking_default_values())
            picking_type_id = new_picking.picking_type_id.id
            new_picking.message_post_with_view('mail.message_origin_link',
                values={'self': new_picking, 'origin': self.picking_id},
                subtype_id=self.env.ref('mail.mt_note').id)
        else:
            for rec in self.stock_picking_ids:
                picking = rec
            new_picking = picking.copy(self._prepare_picking_default_values())
            picking_type_id = new_picking.picking_type_id.id
            new_picking.message_post_with_view('mail.message_origin_link',
                                               values={'self': new_picking, 'origin': self.stock_picking_ids},
                                               subtype_id=self.env.ref('mail.mt_note').id)
        returned_lines = 0
        for return_line in self.product_return_moves:
            if not return_line.move_id:
                raise UserError(_("You have manually created product lines, please delete them to proceed."))
            # TODO sle: float_is_zero?
            if return_line.quantity:
                returned_lines += 1
                vals = self._prepare_move_default_values(return_line, new_picking)
                r = return_line.move_id.copy(vals)
                vals = {}

                # +--------------------------------------------------------------------------------------------------------+
                # |       picking_pick     <--Move Orig--    picking_pack     --Move Dest-->   picking_ship
                # |              | returned_move_ids              ↑                                  | returned_move_ids
                # |              ↓                                | return_line.move_id              ↓
                # |       return pick(Add as dest)          return toLink                    return ship(Add as orig)
                # +--------------------------------------------------------------------------------------------------------+
                move_orig_to_link = return_line.move_id.move_dest_ids.mapped('returned_move_ids')
                # link to original move
                move_orig_to_link |= return_line.move_id
                # link to siblings of original move, if any
                move_orig_to_link |= return_line.move_id \
                    .mapped('move_dest_ids').filtered(lambda m: m.state not in ('cancel')) \
                    .mapped('move_orig_ids').filtered(lambda m: m.state not in ('cancel'))
                move_dest_to_link = return_line.move_id.move_orig_ids.mapped('returned_move_ids')
                # link to children of originally returned moves, if any. Note that the use of
                # 'return_line.move_id.move_orig_ids.returned_move_ids.move_orig_ids.move_dest_ids'
                # instead of 'return_line.move_id.move_orig_ids.move_dest_ids' prevents linking a
                # return directly to the destination moves of its parents. However, the return of
                # the return will be linked to the destination moves.
                move_dest_to_link |= return_line.move_id.move_orig_ids.mapped('returned_move_ids') \
                    .mapped('move_orig_ids').filtered(lambda m: m.state not in ('cancel')) \
                    .mapped('move_dest_ids').filtered(lambda m: m.state not in ('cancel'))
                vals['move_orig_ids'] = [(4, m.id) for m in move_orig_to_link]
                vals['move_dest_ids'] = [(4, m.id) for m in move_dest_to_link]
                r.write(vals)
        if not returned_lines:
            raise UserError(_("Please specify at least one non-zero quantity."))
        new_picking.action_confirm()
        new_picking.action_assign()
        return new_picking.id, picking_type_id
