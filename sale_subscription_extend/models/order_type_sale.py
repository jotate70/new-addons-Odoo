# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class SaleOrderType(models.Model):
    _name = "sale_order_type"
    _description = "Subscription"

    name = fields.Char(string='Nombre del acuerdo')
    allow_stock_picking = fields.Boolean(string='Permitir movimiento de inventario', help='Stock picking movement')
    allow_approve = fields.Boolean(string='Requiere aprobación', help='Ask for approval on the sales order')
    order_type = fields.Selection([
        ('contract', 'Contract'),
        ('unit_rental', 'Unit rental'),
        ('sale', 'Sale'),
        ('quote', 'Quote'),],
        string='Tipo de orden', index=True, default='contract',
        help="\n- Contract: Subscription items with the recurring option."
             "\n- Unit rental: Storable subscription items with recurring option."
             "\n- Sale: for sale items. "
             "\n- Quote, allows you to make sales quotes.")







