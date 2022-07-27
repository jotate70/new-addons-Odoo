# -*- coding: utf-8 -*-

from odoo import models, fields, api
import json

class employee_extend(models.Model):
    _inherit = 'hr.employee'

    parent_optional_id = fields.Many2one(string='Aprobador optional', help='Permite tener una alternativa para un aprobador sin tope en caso de ausencia.')
    active_budget = fields.Boolean(string='Es responsable de presupuesto.',
                                   help='Está check activa la opción de asignar presupiesto al empleado.')
    general_manager = fields.Boolean(string='Sin tope de presupuesto.',
                                     help='Es la persona que no tiene limite para aprobar presupuesto.')
    budget = fields.Float(string='Presupuesto', help='Monto maximo que puede aprobar por solicitud de compra.')
    budget_discount = fields.Float(string='Ultimo monto',
                                   help='Esté campo se utiliza para guardar el valor del ultimo monto aprobado en una requisición.')
    budget_transit = fields.Date(string='Saldo de presupuesto', help='Indica el saldo del presupuesto a la fecha.')
    budget_date_start = fields.Date(string='Fecha de incio',
                                    help='Indica la fecha de incio del presupuesto.')
    budget_date_end = fields.Date(string='Fecha de incio',
                                    help='Indica la fecha final del presupuesto.')
    manager_warehouse = fields.Many2many(comodel_name='stock.warehouse', relation='x_hr_employee_stock_warehouse_rel',
                                         column1='hr_employee_id', column2='stock_warehouse_id', string='Almacenes',
                                         help='Almacenes que puedes aprobar transferencia internas inmeditas.')
    stock_warehouse_domain = fields.Char(compute="_compute_stock_warehouse", readonly=True, store=False)

    # Función que aplica filtro dinamico de almacen
    @api.depends('manager_warehouse')
    def _compute_stock_warehouse(self):
        warehouse = self.env['stock.warehouse'].sudo().search([('employee_id', "=", False)])
        for rec in self:
            rec.stock_warehouse_domain = json.dumps(
                [('id', "=", warehouse.ids)]
            )

    def _compute_manager_budget(self):
        if self.budget_transit >= 0:
            self.budget_transit = self.budget_transit - self.budget_discount
        else:
            # notificación
            self.action_notification()

    def _reset_manager_budget_transit(self):
        employee_budget = self.env['hr.employee'].search([('active_budget', '=', True)])
        for rec in employee_budget:
            rec.budget_transit = rec.budget

    # Notificación
    def action_notification(self):
        notification_title = 'Atención'
        notification_message = 'Ya supero en monto mensual'
        notification_type = 'success'
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': notification_title,
                'message': notification_message,
                'type': notification_type,
            }
        }










