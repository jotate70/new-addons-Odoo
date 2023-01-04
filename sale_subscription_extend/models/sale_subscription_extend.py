# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError

class SaleSubscription(models.Model):
    _inherit = 'sale.subscription'
    _description = "Subscription"

    approve_manager_origin = fields.Many2one(comodel_name='hr.employee', string='Responsable de aprobación original',
                                             related='user_id.employee_id.department_id.manager_id',
                                             help='Jefe responsable de la orden de compra o requisición')
    manager_id = fields.Many2one(comodel_name='hr.employee', related='user_id.employee_id.department_id.manager_id',
                                 string='Representante de aprobación',
                                 help='Jefe inmediato respondable de su aprobación')
    time_off = fields.Char(string='Disponibilidad', compute='_compute_number_of_days')
    time_off_related = fields.Boolean(string='Ausencia', related='manager_id.is_absent')
    recurring_invoice_line_2_ids = fields.One2many('sale_subscription_line_2', 'analytic_account_id',
                                                 string='Subscription Lines', copy=True)
    state_aprove = fields.Integer(string='nivel de aprobación', help='Indica el nivel de aprobación actual')
    activity_id = fields.Integer(string='id actividad')

    # Crea el estado si no existe
    def _create_onchange_state_approve(self):
        state_approve = self.env['sale.subscription.stage'].search([('name', '=', 'approve')])
        if state_approve:
            return
        else:
            for rec in self:
                create_state = {'name': 'approve',
                                'sequence': '30',
                                'fold': False,
                                'category': 'progress',
                                'description': 'Approval manager',
                               }
                self.env['sale.subscription.stage'].sudo().create(create_state)

    # Crea el estado si no existe
    def _create_onchange_state_invoiced(self):
        state_invoiced = self.env['sale.subscription.stage'].search([('name', '=', 'invoiced')])
        if state_invoiced:
            return
        else:
            for rec in self:
                create_state = {'name': 'invoiced',
                                'sequence': '35',
                                'fold': False,
                                'category': 'progress',
                                'description': 'invoiced',
                                }
                self.env['sale.subscription.stage'].sudo().create(create_state)

    # Indica si el jefe inmediato está o no está ausente
    @api.depends('time_off_related')
    def _compute_number_of_days(self):
        if self.time_off_related == False:
            self.time_off = 'Disponible'
        else:
            self.time_off = 'Ausente'
            # Para el caso de cuando no es un gerente general o una persona con limite de presupuesto
            if self.manager_id.general_manager == False:
                self.write({'manager2_id': self.manager_id.parent_id})
            # Para el caso de cuando es un gerente general o una persona sin tope de presupuesto
            else:
                self.write({'manager2_id': self.manager_id.parent_optional_id})
        return self.time_off

    # Update state approve
    def action_approve_subscription(self):
        # Verifica que exista los estados, y si no los crea
        if self.manager_id:
            self._create_onchange_state_approve()
            self._create_onchange_state_invoiced()
            state = self.env['sale.subscription.stage'].search([('name', '=', 'approve')])
            self.write({'stage_id': state.id})
            # Código que crea una nueva actividad
            model_id = self.env['ir.model']._get(self._name).id
            create_vals = {
                'activity_type_id': 4,
                'summary': 'Facturación recurrente:',
                'automated': True,
                'note': 'Ha sido asignado para aprobar la siguiente suscripción',
                'date_deadline': fields.Datetime.now(),
                'res_model_id': model_id,
                'res_id': self.id,
                'user_id': self.manager_id.user_id.id
            }
            new_activity = self.env['mail.activity'].create(create_vals)
            # Escribe el id de la actividad en un campo
            self.write({'activity_id': new_activity})
        else:
            raise UserError('No existe un responsable para aprobar la suscripción, por favor comunicarse con el administrador.')

    # Función del boton aprobación extend
    def button_approve(self, force=False):
        if self.manager_id:
            # aprobación para el manager
            if self.manager_id.user_id == self.env.user:
                if self.state_aprove == 0:
                    #  Marca actividad como hecha de forma automatica
                    new_activity = self.env['mail.activity'].search([('id', '=', self.activity_id)], limit=1)
                    new_activity.action_feedback(feedback='Es aprobado')
                    # Contador de niveles de aprovación
                    c = self.state_aprove + 1
                    self.write({'state_aprove': c})
                    # jefe inmediato del jefe actual
                    users = self.env.user.employee_id.parent_id
                    # Actualiza el jefe inmediato
                    self.write({'manager_id': users})
                    # Código que crea una nueva actividad
                    model_id = self.env['ir.model']._get(self._name).id
                    create_vals = {
                        'activity_type_id': 4,
                        'summary': 'Segunda aprobación, facturación recurrente:',
                        'automated': True,
                        'note': 'Ha sido asignado para aprobar la siguiente facturación recurrente.',
                        'date_deadline': fields.Datetime.now(),
                        'res_model_id': model_id,
                        'res_id': self.id,
                        'user_id': self.manager_id.user_id.id
                    }
                    new_activity = self.env['mail.activity'].create(create_vals)
                    # Escribe el id de la nueva actividad para el siguiente nivel de aprobación
                    self.write({'activity_id': new_activity})
                if self.state_aprove == 1:
                    #  Marca actividad como hecha de forma automatica
                    new_activity = self.env['mail.activity'].search([('id', '=', self.activity_id)], limit=1)
                    new_activity.action_feedback(feedback='Es aprobado')
                    # Contador de niveles de aprovación
                    c = self.state_aprove + 1
                    self.write({'state_aprove': c})
                    # jefe inmediato del jefe actual
                    users = self.env.user.employee_id.parent_id
                    # Actualiza el jefe inmediato
                    self.write({'manager_id': users})
                    # Código que crea una nueva actividad
                    model_id = self.env['ir.model']._get(self._name).id
                    create_vals = {
                        'activity_type_id': 4,
                        'summary': 'Confirmación de estado facturación de la suscripción:',
                        'automated': True,
                        'note': 'Ha sido asignado para indicar el estado de la redicación de la factura de la suscripción',
                        'date_deadline': fields.Datetime.now(),
                        'res_model_id': model_id,
                        'res_id': self.id,
                        'user_id': self.manager_id.user_id.id
                    }
                    new_activity = self.env['mail.activity'].create(create_vals)
                    # Escribe el id de la nueva actividad para el siguiente nivel de aprobación
                    self.write({'activity_id': new_activity})
            else:
                raise UserError('La persona responsable debe aprobar la solicitud.')
        # Función de aprobación por defecto
        else:
            raise UserError('No existe un responsable para aprobar la suscripción, por favor comunicarse con el administrador.')

class SaleSubscriptionLine2(models.Model):
    _name = "sale_subscription_line_2"
    _description = "Subscription Line 2"
    _check_company_auto = True

    product_id = fields.Many2one(
        'product.product', string='Product', check_company=True,
        domain="[('recurring_invoice','=',True)]", required=True)
    analytic_account_id = fields.Many2one('sale.subscription', string='Subscription', ondelete='cascade')
    company_id = fields.Many2one('res.company', related='analytic_account_id.company_id', store=True, index=True)
    name = fields.Text(string='Description', required=True)
    quantity = fields.Float(string='Quantity', help="Quantity that will be invoiced.", default=1.0, digits='Product Unit of Measure')
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', required=True, domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', readonly=True)
    price_unit = fields.Float(string='Unit Price', required=True, digits='Product Price')
    discount = fields.Float(string='Discount (%)', digits='Discount')
    price_subtotal = fields.Float(compute='_compute_amount', string='Subtotal', digits='Account', store=True)
    currency_id = fields.Many2one('res.currency', 'Currency', related='analytic_account_id.currency_id', store=True)

