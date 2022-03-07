from odoo import fields, models, api, _
from odoo.exceptions import UserError


class ModelName(models.Model):
    _inherit = 'purchase.order'

    requisition_state = fields.Selection(string='Estado acuerdo de compra', related='requisition_id.state')
    related_requisition = fields.Boolean(string='relacion requicision', related='requisition_id.available')
    state_aprove = fields.Integer(string='nivel de aprobación')
    manager_before = fields.Many2one(comodel_name='hr.employee', string='Responsable de anterior')
    aprove_manager = fields.Many2one(comodel_name='hr.employee', string='Responsable de aprobación')
    activity_id = fields.Integer(string='id actividad')

    # Función del boton confirmar
    def button_confirm_extend(self):
        # código nuevo con condición
        if self.related_requisition == True:
            for order in self:
                if order.state not in ['draft', 'sent']:
                    continue
                order._add_supplier_to_product()
                order.write({'state': 'to approve'})

                # Código que crea una nueva actividad
                model_id = self.env['ir.model']._get(self._name).id
                create_vals = {
                    'activity_type_id': 4,
                    'summary': 'Solicitud de compra:',
                    'automated': True,
                    'note': 'A sido asignado para aprovar la siguiente solicitud de compra',
                    'date_deadline': self.date_order.date(),
                    'res_model_id': model_id,
                    'res_id': self.id,
                    'user_id': self.requisition_id.manager_id.user_id.id
                }
                new_activity = self.env['mail.activity'].create(create_vals)

                # Escribe el id de la actividad en un campo
                self.write({'activity_id': new_activity})

                # jefe inmediato del jefe actual
                self.write({'aprove_manager': self.requisition_id.manager_id})

                # Contador de niveles de aprovación
                c = self.state_aprove + 1
                self.write({'state_aprove': c})

                # if order.partner_id not in order.message_partner_ids:
                #     order.message_subscribe([order.partner_id.id])
            return True
        elif self.requisition_id.state == 'cancel':
            raise UserError('El acuerdo de compra asociado está en estado cancelado.')
        elif self.requisition_id.state == 'draft' or self.requisition_id.state == 'in_progress':
            raise UserError('EL acuerdo de compra primero debe ser aprovado.')
        else:
            # código por defecto
            for order in self:
                if order.state not in ['draft', 'sent']:
                    continue
                order._add_supplier_to_product()
                # Deal with double validation process
                if order._approval_allowed():
                    order.button_approve()
                else:
                    order.write({'state': 'to approve'})
                if order.partner_id not in order.message_partner_ids:
                    order.message_subscribe([order.partner_id.id])
            return True

    # Función del boton aprovación
    def action_approve_extend(self):
        if self.related_requisition == True:
            if self.env.user.employee_id.general_manager == False:
                # Aprovación para el manager
                if self.aprove_manager.user_id == self.env.user:
                    # niveles de aprobación dependiendo el monto asignado al jefe inmediato
                    # si cumple la condición aprueba la orden, si no pide un nivel más
                    if self.amount_total <= self.aprove_manager.budget:
                        # Aprueba la orden
                        self.write({'state': 'purchase', 'date_approve': fields.Datetime.now()})
                        #  Marca actividad como hecha de forma automatica
                        new_activity = self.env['mail.activity'].search([('id', '=', self.activity_id)], limit=1)
                        new_activity.action_feedback(feedback='Es aprobado')
                    else:
                        # está condición evita que repita aprobación
                        if self.aprove_manager != self.env.user.employee_id.parent_id:

                            #  Marca actividad anterior como hecha de forma automatica
                            new_activity = self.env['mail.activity'].search([('id', '=', self.activity_id)], limit=1)
                            new_activity.action_feedback(feedback='Requiere otra aprobación')

                            # Estado en aprovación si necesita otro nivel de aprovación
                            self.write({'state': 'to approve'})
                            # Contador de niveles de aprovación
                            c = self.state_aprove + 1
                            self.write({'state_aprove': c})

                            # jefe inmediato del jefe actual
                            users = self.env.user.employee_id.parent_id
                            self.write({'aprove_manager': users})

                            # se usa para avisar al usuario que ya aprobo la solictud
                            users_before = self.env.user.employee_id
                            self.write({'manager_before': users_before})

                            # Código que crea una nueva actividad y valida que no sea un genre general
                            model_id = self.env['ir.model']._get(self._name).id
                            create_vals = {
                                'activity_type_id': 4,
                                'summary': 'Aprovación adicional, solicitud de compra:',
                                'automated': True,
                                'note': 'A sido asignado para aprovar la siguiente solicitud de compra, debido a que el montón supera la base del jefe a cargo',
                                'date_deadline': self.date_order.date(),
                                'res_model_id': model_id,
                                'res_id': self.id,
                                'user_id': self.aprove_manager.user_id.id
                                }
                            new_activity = self.env['mail.activity'].create(create_vals)
                            # Escribe el id de la nueva actividad para el siguiente nivel de aprovación
                            self.write({'activity_id': new_activity})
                        else:
                            raise UserError('Ya aprovaste la solicitud de compra, debes esperar a que su jefe inmediato apruebe ya que supera su monto asigando.')

                elif self.requisition_id.manager_id == self.env.user.employee_id:
                    raise UserError('Ya aprovaste la solicitud, Su jefe inmediato debe aprobar ya que supera su presupuesto asignado.')
                elif self.manager_before == self.env.user.employee_id:
                    raise UserError('Ya aprovaste la solicitud, Su jefe inmediato debe aprobar ya que supera su presupuesto asignado.')
                else:
                    raise UserError('El gerente responsable debe aprobar la solicitud.')

            else:
                # Aprovación gerente general
                self.write({'state': 'purchase', 'date_approve': fields.Datetime.now()})
                #  Marca actividad anterior como hecha de forma automatica
                new_activity = self.env['mail.activity'].search([('id', '=', self.activity_id)], limit=1)
                new_activity.action_feedback(feedback='Es aprobado')

        else:
            raise UserError('No se puede validar, el acuerdo de compra está cerrado o ha sido desasociado')

    # Botón reestableercer a borrador
    def button_draft_extend(self):
        self.write({'state': 'draft'})
        # se reestablece el jefe actual
        self.write({'aprove_manager': self.requisition_id.manager_id})
        # se reestablece el jefe actual
        self.write({'manager_before': False})
        # se reestablece el nivel de aprovación
        self.write({'state_aprove': 0})
        return {}

    # Boton cancelar
    def button_cancel_extend(self):
        #  Marca actividad como hecha de forma automatica
        new_activity = self.env['mail.activity'].search([('id', '=', self.activity_id)], limit=1)
        new_activity.action_feedback(feedback='Es Rechazado')
        for order in self:
            for inv in order.invoice_ids:
                if inv and inv.state not in ('cancel', 'draft'):
                    raise UserError(_("Unable to cancel this purchase order. You must first cancel the related vendor bills."))

        self.write({'state': 'cancel', 'mail_reminder_confirmed': False})







