# -*- coding: utf-8 -*-
# Part of Odoo. See ICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_round
import json

class ReturnPickingLineDetail(models.TransientModel):
    _name = "return_picking_line_detail"
    _description = 'Return Picking Line detail'

    location = fields.Many2one(comodel_name='location_warehouse', string='Locación',
                               help='Muestra la ciudad/locación del almacén')
    warehouse_id = fields.Many2one(comodel_name='stock.warehouse', string='De almacen', help='Almacen de origen')
    location_id = fields.Many2one(comodel_name='stock.location', string='Location')
    location_dest_id = fields.Many2one(comodel_name='stock.location', string='Return Location')
    product_id = fields.Many2one('product.product', string="Product")
    lot_id = fields.Many2one(comodel_name='stock.production.lot', string='Lot/Serial Number')
    plaque_id = fields.Many2one(comodel_name='stock_production_plaque', string='Placa')
    quantity = fields.Float("Quantity", digits='Product Unit of Measure')
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', related='product_id.uom_id')
    wizard_id = fields.Many2one('stock.return.picking', string="Wizard")
    fee_unit = fields.Float(string='Tarifa unitaria')
    contract_date = fields.Date(string='Inicio de contrato',
                                help='Indica la fecha que se realiza el contrato asociada a dicha transferencia')
    contract_date_end = fields.Date(string='Finalización de contrato',
                                help='Indica la fecha que se realiza el contrato asociada a dicha transferencia')

class ReturnPickingLine(models.TransientModel):
    _inherit = 'stock.return.picking.line'

    return_location_id = fields.Many2one(comodel_name='stock.location',
                                          string='Ubicaciones de devolución',
                                          help='Ubicacioón para devolcución seleciona por el sistema')
    location = fields.Many2one(comodel_name='location_warehouse', string='Locación', related='wizard_id.location',
                               help='Muestra la ciudad/locación del almacén')
    warehouse_id = fields.Many2one(comodel_name='stock.warehouse', string='De almacen', help='Almacen de origen')
    location_origin_id = fields.Many2one(comodel_name='stock.location', string='Return Location',
                                         domain="location_domain")
    stock_quant_ids = fields.Many2many(comodel_name='stock.quant',
                                      string='Detail Operation')
    return_detail = fields.Many2many(comodel_name='return_picking_line_detail', string='Detail Operation')

class ReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    location = fields.Many2one(comodel_name='location_warehouse', string='Locación',
                               help='Muestra la ciudad/locación del almacén')
    warehouse_domain = fields.Char(string="domain warehouse", compute='_domain_warehouse_domain_id')
    warehouse_id = fields.Many2one(comodel_name='stock.warehouse', string='De almacen', help='Almacen de origen',
                                   domain='warehouse_domain')
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
    related_stock_picking = fields.Boolean(string="relation ticket")
    product_return_moves2 = fields.One2many('return_picking_line_detail', 'wizard_id', 'Moves')

    # realciona y crea registro product_return_moves con stock_quant_ids
    @api.onchange('stock_quant_ids')
    def _compute_stock_picking(self):
        return_id = 0
        return_dest = 0

        if self.product_return_moves and self.related_stock_picking == True:
            self.product_return_moves = False
            self.product_return_moves2 = False

        for rec1 in self.mapped('stock_quant_ids').product_id:
            qty = 0
            product = []
            quant = []
            for rec2 in self.stock_quant_ids:
                if rec1.id == rec2.product_id.id:
                    product.append(rec1.id)
                    quant.append(rec2.id)
                    qty = rec2.quantity + qty
                    if rec2.product_id.categ_id.return_location_id:
                        for rec3 in rec2.product_id.categ_id.return_location_id:
                            if rec3.location_id2 == self.location:
                                return_id = rec3.id
                    else:
                        return_id = False
            self.write({'product_return_moves': [(0, 0, {'product_id': rec1.id,
                                                         'quantity': qty,
                                                         'uom_id': rec1.uom_id.id,
                                                         'wizard_id': self.id,
                                                         'stock_quant_ids': quant,
                                                         # 'return_detail': quant,
                                                         'return_location_id': return_id,
                                                         })]})
        for rec3 in self.mapped('stock_quant_ids'):
            for rec4 in self.product_return_moves:
                if rec3.product_id == rec4.product_id:
                    return_dest = rec4.return_location_id
            self.write({'product_return_moves2': [(0, 0, {'location': rec3.location,
                                                          'warehouse_id': self.warehouse_id,
                                                          'location_id': self.location_id.id,
                                                          'location_dest_id': return_dest,
                                                          'product_id': rec3.product_id.id,
                                                          'lot_id': rec3.lot_id.id,
                                                          'plaque_id': rec3.plaque_id,
                                                          'quantity': rec3.quantity,
                                                          'uom_id': rec3.product_uom_id.id,
                                                          'fee_unit': rec3.fee_unit,
                                                          'contract_date': rec3.contract_date,
                                                          'contract_date_end': rec3.contract_date_end,
                                                          })]})

    # Seleciona ubicación de destino (no se usa, es campo obligatorio por defecto)
    @api.onchange('stock_quant_ids')
    def _compute_location_demo(self):
        if self.type_return == 'product':
            for rec in self:
                rec.location_id = rec.location_origin_id


    # Reestablece ubicaciones cuando se cambia el tipo de devolución
    @api.onchange('type_return')
    def _reset_stock_picking_ids(self):
        for rec in self:
            if rec.type_return == 'product' and rec.related_stock_picking == True:
                rec.stock_picking_ids = False
                rec.product_return_moves = False
                # rec.product_return_moves2 = False
            elif rec.type_return == 'picking' and rec.related_stock_picking == True:
                rec.stock_quant_ids = False
                rec.product_return_moves = False
                # rec.product_return_moves2 = False

    # Reestablece las transferecias o productos seleccionados al cambiar de ubicación
    @api.onchange('location_origin_id')
    def _reset_stock_picking(self):
        for rec in self:
            if rec.location_origin_id and rec.related_stock_picking == True:
                rec.stock_picking_ids = False
                rec.product_return_moves = False

    # Reestablece la ubicación de origin al seleccionar almacen
    @api.onchange('warehouse_id')
    def _reset_location_origin_id(self):
        self.location_origin_id = False

    # Reestablece la ubicación de origin al seleccionar almacen
    @api.onchange('location')
    def _reset_location_id(self):
        self.warehouse_id = False

    # warehouse domain
    @api.depends('location')
    def _domain_warehouse_domain_id(self):
        if self.location:
            for rec in self:
                rec.warehouse_domain = json.dumps(
                    [('location_id', "=", rec.location.ids),
                     ('partner_id', '=', rec.ticket_id.partner_id.ids)])
        else:
            self.warehouse_domain = json.dumps([])

    # Stock quant domain
    @api.depends('location_origin_id')
    def _domain_stock_quant_ids(self):
        if self.location_origin_id:
            for rec in self:
                rec.stock_quant_domain = json.dumps(
                    [('location_id', "=", rec.location_origin_id.ids), ('available_quantity', '>', 0.0)])
        else:
            self.stock_quant_domain = json.dumps([])

    # Origin location domain
    @api.depends('warehouse_id')
    def _domain_location_origin_id(self):
        if self.warehouse_id:
            for rec in self:
                # rec.location_domain = json.dumps([('id', "=", rec.mapped('suitable_picking_ids').location_dest_id.ids),
                #                                   ('warehouse_id', '=', rec.warehouse_id.ids), ('usage', 'in', ['supplier', 'internal', 'customer'])])
                rec.location_domain = json.dumps([('warehouse_id', '=', rec.warehouse_id.ids),
                                                  ('usage', 'in', ['supplier', 'internal', 'customer'])])
        else:
            self.location_domain = json.dumps([])

    # pickings domain
    @api.depends('location_origin_id')
    def _domain_pickings_id(self):
        if self.location_origin_id:
            for rec in self:
                # rec.picking_domain_ids = json.dumps([('id', 'in', self.mapped('suitable_picking_ids').filtered(lambda m: m.location_dest_id == rec.location_origin_id).ids)])
                rec.picking_domain_ids = json.dumps([('id', 'in', self.mapped('suitable_picking_ids').filtered(
                    lambda m: m.location_dest_id == rec.location_origin_id).ids), ('state', '=', 'done')])
        else:
            self.picking_domain_ids = json.dumps([])

    @api.onchange('stock_picking_ids')
    def _onchange_stock_picking_ids(self):
        move_dest_exists = False
        product_return_moves = [(5,)]
        for rec in self.stock_picking_ids:
            if rec and rec.state != 'done':
                raise UserError(_("You may only return Done pickings."))
        # In case we want to set specific default values (e.g. 'to_refund'), we must fetch the
        # default values for creation.
        line_fields = [f for f in self.env['stock.return.picking.line']._fields.keys()]
        product_return_moves_data_tmpl = self.env['stock.return.picking.line'].default_get(line_fields)
        for move in self.stock_picking_ids:
            for rec in move.move_lines:
                if rec.state == 'cancel':
                    continue
                if rec.scrapped:
                    continue
                if rec.move_dest_ids:
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

    # Prepara da lineas de devolución en modo devolución por tranferencias
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

    # Retorna los valores para generar el stock picking devolución en modo devolución por tranferencias
    def _prepare_picking_default_values(self):
        # Stock picking origin concatenate
        if self.picking_id:
            return {
                'move_lines': [],
                'picking_type_id': self.picking_id.picking_type_id.return_picking_type_id.id or self.picking_id.picking_type_id.id,
                'state': 'draft',
                'origin': _("Return of %s") % self.picking_id.name,
                'location_id': self.picking_id.location_dest_id.id,
                'location_dest_id': self.location_id.id,
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
                'currency_id': self.env.company.currency_id.id,
            }

    # Crea el stock picking de devolución en modo devolución por tranferencias
    def _create_returns(self):
        if self.type_return == 'product':
            pickings = []
            self.create_return_extend_product()
            return pickings
        elif self.type_return == 'picking':
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

    # Crea stock picking de devolución en modo devolución por productos
    def create_return_extend_product(self):
        l = []
        a = []
        picking = []
        operation = []
        for rec1 in self.mapped('product_return_moves'):
            if rec1.return_location_id:
                l.append(rec1.return_location_id.id)
                a = list(set(l))
            else:
                raise UserError('No se ha establecido una ubicación de devoluciones en la categoría del producto, %s.' % rec1.product_id.name)
        for rec2 in self.mapped('product_return_moves').return_location_id:
            picking_type = self.env['stock.location'].search([('id', '=', rec1.return_location_id.id)], limit=1)
            create_vals = {'partner_id': self.partner_id.id,
                           'origin': 'return' + ' [' + self.warehouse_id.name + ']',
                           'scheduled_date': fields.datetime.now(),
                           'picking_type_id': picking_type.warehouse_id.pick_type_id.id,
                           'location_id': self.location_origin_id.id,
                           'location_dest_id': rec2.id,
                           'ticket_return': self.ticket_id.id,
                           'currency_id': self.env.company.currency_id.id,
                           }
            stock_picking1 = self.env['stock.picking'].create(create_vals)
            # Guarda variables de retorno del stock picking y tipo de operación
            picking.append(stock_picking1.id)
            # operation.append(stock_picking1.picking_type_id)
            # return picking, operation
            # Código que crea una nueva actividad
            create_activity = {'activity_type_id': 4,
                               'summary': 'Devolución:',
                               'automated': True,
                               'note': 'Ha sido asignado para validar la devolución de inventario',
                               'date_deadline': fields.datetime.now(),
                               'res_model_id': self.env['ir.model']._get_id('stock.picking'),
                               'res_id': stock_picking1.id,
                               'user_id': stock_picking1.location_dest_id.warehouse_id.employee_id.user_id.id,
                               }
            new_activity1 = self.env['mail.activity'].sudo().create(create_activity)
            # Escribe el id de la actividad en un campo
            stock_picking1.write({'activity_id': new_activity1.id})
            # Crea linea de operaciones detalladas
            for rec3 in self.product_return_moves2:
                if rec3.location_dest_id == rec2:
                    create_vals3 = {
                                    'location_id': self.location_id.id,
                                    'location_dest_id': rec2.id,
                                    'picking_id': stock_picking1.id,
                                    'product_id': rec3.product_id.id,
                                    'lot_id': rec3.lot_id.id,
                                    'plaque_id': rec3.plaque_id.id,
                                    'product_uom_id': rec3.uom_id.id,
                                    'product_uom_qty': 0,
                                    'qty_done': rec3.quantity,
                                    'fee_unit': rec3.fee_unit,
                                    'contract_date': rec3.contract_date,
                                    'contract_date_end': rec3.contract_date_end,
                                    }
                    self.env['stock.move.line'].sudo().create(create_vals3)
            stock_picking1.action_confirm()
            # stock_picking1.action_assign()
        # Add tickets in helpdesk
        self.ticket_id.compute_picking_ids(picking)



