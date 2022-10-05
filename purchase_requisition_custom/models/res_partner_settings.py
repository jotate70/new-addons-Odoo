# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    approve_manager_budget_settings = fields.Boolean(string='Activar presupuesto')
    account_analityc_requisition_settings = fields.Boolean(string='Activar cuentas analíticas')

    # Permite guardar valor en modelo transitorio
    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param(
            'purchase_requisition_custom_constraint.approve_manager_budget_settings',
            self.approve_manager_budget_settings)
        self.env['ir.config_parameter'].set_param(
            'purchase_requisition_custom_constraint.account_analityc_requisition_settings',
            self.account_analityc_requisition_settings)
        return res

    # permite obtener valores en modelo transitorio
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        requisition_parameter_approve_manager_budget_settings = ICPSudo.get_param(
            'purchase_requisition_custom_constraint.approve_manager_budget_settings')
        requisition_parameter_account_analityc_requisition_settings = ICPSudo.get_param(
            'purchase_requisition_custom_constraint.account_analityc_requisition_settings')


        res.update(
            approve_manager_budget_settings=requisition_parameter_approve_manager_budget_settings,
            account_analityc_requisition_settings=requisition_parameter_account_analityc_requisition_settings,
        )
        return res








