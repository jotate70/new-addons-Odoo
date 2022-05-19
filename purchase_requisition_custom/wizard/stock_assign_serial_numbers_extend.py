# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class StockAssignSerialNumbers_extend(models.TransientModel):
    _inherit = 'stock.assign.serial'

    fee_unit = fields.Float(string='Tarifa unitaria', digits='Product Price')
    observation = fields.Char(string='Observación')


