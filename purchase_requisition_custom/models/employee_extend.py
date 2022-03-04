# -*- coding: utf-8 -*-

from odoo import models, fields, api


class employee_extend(models.Model):
    _inherit = 'hr.employee'

    budget = fields.Float(string='Presupuesto', help='Monto maximo que puede aprobar por solicitud de compra')
    active_budget = fields.Boolean(string='Es responsable de presupuesto', help='Está check activa la opción de asignar presupiesto al empleado')
    general_manager = fields.Boolean(string='Sin tope de presupuesto', help='Es la persona que no tiene limite para aprobar presupuesto')



