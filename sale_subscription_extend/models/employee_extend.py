# -*- coding: utf-8 -*-

from odoo import models, fields, api
import json

class employee_extend(models.Model):
    _inherit = 'hr.employee'

    invoicing_manager = fields.Boolean(string='Responsable de facturación recurrente.',
                                       help='Está check activa la opción de asignar presupiesto al empleado.')
    subscription_manager = fields.Boolean(string='Responsable de suscripción',
                                            help='Es la persona que no tiene limite para aprobar presupuesto.')













