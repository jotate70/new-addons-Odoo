# -*- coding: utf-8 -*-

from odoo import models, fields, api
import json

class employee_extend(models.Model):
    _inherit = 'hr.employee'

    approve_manager_budget_settings = fields.Boolean(string='Activar presupuesto', compute='get_requisition')
    parent_optional_id = fields.Many2one(comodel_name='hr.employee', string='Aprobador opcional', help='Permite tener una alternativa para un aprobador sin tope en caso de ausencia.')
    active_budget = fields.Boolean(string='Es responsable de presupuesto.',
                                   help='Está check activa la opción de asignar presupiesto al empleado.')
    general_manager = fields.Boolean(string='Sin tope de presupuesto.',
                                     help='Es la persona que no tiene limite para aprobar presupuesto.')
    budget = fields.Float(string='Presupuesto', help='Monto maximo que puede aprobar por el periodo establecido.')
    person_budget = fields.Float(string='Tope de aprobación', help='Monto maximo que puede aprobar por solicitud de compra.')
    budget_discount = fields.Float(string='Suma requisiciones',
                                   help='Esté campo se utiliza para guardar la suma de las requisiciones.')
    budget_available = fields.Float(string='Saldo actual', compute='_compute_available_budget',
                                    help='Indica el saldo del presupuesto a la fecha.')
    budget_available_total = fields.Float(string='Saldo', compute='compute_budget_available_total',
                                     help='Indica el saldo del presupuesto a la fecha computado.')
    collaborators_sum = fields.Float(string='Suma presupuestos subordinados', compute='compute_collaborators_sum',
                                          help='Indica el saldo del presupuesto a la fecha computado.')
    budget_len = fields.Selection([('monthly', 'Mensual'),
                                   ('quasrtely', 'Trimestral'),
                                   ('biannual', 'Semestral'),
                                   ('annual', 'Anual'),
                                   ],
                                  string='Locación', help='Indica la ciudad donde se ejecuta el proyecto',
                                  default='monthly', store=True)
    manager_warehouse = fields.Many2many(comodel_name='stock.warehouse', relation='x_hr_employee_stock_warehouse_rel',
                                         column1='hr_employee_id', column2='stock_warehouse_id', string='Almacenes',
                                         help='Almacenes que puedes aprobar transferencia internas inmeditas.')
    stock_warehouse_domain = fields.Char(compute="_compute_stock_warehouse", readonly=True, store=False)
    currency_id = fields.Many2one(comodel_name='res.currency', string='Moneda')

    # Función que llaman los valores en modelo settings
    def get_requisition(self):
        self.approve_manager_budget_settings = self.env['ir.config_parameter'].sudo().get_param(
            'purchase_requisition_custom_constraint.approve_manager_budget_settings')

    # Función que aplica filtro dinamico de almacen
    @api.depends('manager_warehouse')
    def _compute_stock_warehouse(self):
        warehouse = self.env['stock.warehouse'].sudo().search([('employee_id', "=", False)])
        for rec in self:
            rec.stock_warehouse_domain = json.dumps(
                [('id', "=", warehouse.ids)]
            )

    # Función que suma gasto de presupuesto de las perosnas a cargo
    def compute_collaborators_sum(self):
        a = self.env['hr.employee'].search([('id', '=', self.ids), ('active_budget', '=', True),
                                            ('budget', '>', 0), ('budget_available', '>', 0)], limit=1)
        if a.child_ids:
            for rec2 in a.child_ids:
                self.collaborators_sum += (rec2.budget - rec2.budget_available)
        else:
            self.collaborators_sum = 0

    # Función que suma gasto de presupuesto de las perosnas a cargo + el gasto propio
    def compute_budget_available_total(self):
        self.budget_available_total = self.budget - (self.collaborators_sum + (self.budget - self.budget_available))

    # Restablece el presupuesto
    @api.onchange('budget')
    def _apply_manager_budget(self):
        self.budget_available = self.budget
        self.budget_discount = 0

    # Suma el gasto de presupuesto asignado
    def compute_manager_budget(self, amount_untaxed):
        self.budget_discount += amount_untaxed

    # Resta el gasto de presupuesto asignado cuando se cancela el movimiento
    def compute_manager_budget_subtration(self, amount_untaxed):
        self.budget_discount -= amount_untaxed

    # descuenta el gasto del presupuesto de los subordinados al presupuesto asignado
    def _compute_available_budget(self):
        for rec in self:
            rec.budget_available = rec.budget - rec.budget_discount












