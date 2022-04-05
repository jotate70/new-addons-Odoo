# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions

# heredamos del modelo de tickets de mesa ayuda
class helpdesk_ticket_requisition(models.Model):
    _inherit = 'helpdesk.ticket'

    requisition_id = fields.Many2one(comodel_name='purchase.requisition', string='Acuerdo de compra')














