# -*- coding: utf-8 -*-

from odoo import models, fields, api


class employee_extend(models.Model):
    _inherit = 'hr.employee'

    budget = fields.Float(string='Presupuesto mensual', help='Presupuesto mensual que se le asigna a los gerentes y directores')
    active_budget = fields.Boolean(string='Es responsable de presupuesto')
    general_manager = fields.Boolean(string='Es gerente general')



