# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class SaleOrderType(models.Model):
    _name = "sale_order_type"
    _description = "Subscription"

    name = fields.Char(string='Tipo de acuerdo')
    allow_stock_picking = fields.Boolean(string='Permitir movimiento de inventario')
    allow_suscription = fields.Boolean(string='Es recurrente')
    allow_aprrove = fields.Boolean(string='Requiere aprobación')





