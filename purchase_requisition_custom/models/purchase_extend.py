from odoo import fields, models, api, _
from odoo.exceptions import UserError


class ModelName(models.Model):
    _inherit = 'purchase.order'

    requisition_state = fields.Selection(string='Estado acuerdo de compra', related='requisition_id.state')
    related_requisition = fields.Boolean(string='relacion requicision', related='requisition_id.available')
    state_aprove = fields.Integer(string='nivel de aprobación')
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
                    'summary': 'Aprobación de solicitud de compra',
                    'automated': True,
                    'note': 'A sido asignado para aprovar la siguiente solicitud de compra',
                    'date_deadline': self.date_order.date(),
                    'res_model_id': model_id,
                    'res_id': self.id,
                    'user_id': self.requisition_id.manager_id.user_id.id
                }
                self.env['mail.activity'].create(create_vals)

                # jefe inmediato del jefe actual
                self.write({'aprove_manager': self.requisition_id.manager_id})

                # Contador de niveles de aprovación
                c = self.state_aprove + 1
                self.write({'state_aprove': c})

                # if order.partner_id not in order.message_partner_ids:
                #     order.message_subscribe([order.partner_id.id])
            return True
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
                        self.write({'state': 'purchase', 'date_approve': fields.Datetime.now()})
                    else:
                        # está condición evita que repita aprobación
                        if self.aprove_manager != self.env.user.employee_id.parent_id:
                            # Estado en aprovación si necesita otro nivel de aprovación
                            self.write({'state': 'to approve'})
                            # Código que crea una nueva actividad
                            model_id = self.env['ir.model']._get(self._name).id
                            create_vals = {
                                'activity_type_id': 4,
                                'summary': 'Aprovación adicional de solicitud de compra',
                                'automated': True,
                                'note': 'A sido asignado para aprovar la siguiente solicitud de compra, debido a que el montón supera la base del jefe a cargo',
                                'date_deadline': self.date_order.date(),
                                'res_model_id': model_id,
                                'res_id': self.id,
                                'user_id': self.aprove_manager.parent_id.user_id.id
                                }
                            self.env['mail.activity'].create(create_vals)

                            # Contador de niveles de aprovación
                            c = self.state_aprove + 1
                            self.write({'state_aprove': c})

                            # jefe inmediato del jefe actual
                            users = self.env.user.employee_id.parent_id
                            self.write({'aprove_manager': users})


                        elif self.env.user.employee_id.general_manager == '1':
                            self.write({'state': 'purchase', 'date_approve': fields.Datetime.now()})
                        else:
                            raise UserError('Ya aprovaste la solicitud de compra, debes esperar a que su jefe inmediato apruebe ya que supera su monto asigando.')

                elif self.state_aprove > 1 and self.requisition_id.manager_id == self.env.user.employee_id:
                    raise UserError('Ya aprovaste la solicitud de compra, debes esperar a que su jefe inmediato apruebe ya que supera su monto asigando.')
                else:
                    raise UserError('El gerente responsable debe aprobar la solicitud.')

            else:
                # Aprovación gerente general
                self.write({'state': 'purchase', 'date_approve': fields.Datetime.now()})

        else:
            raise UserError('No se puede validar, el acuerdo de compra está cerrado o ha sido desasociado')

    #    Función que marca como tarea hecha
    def action_done(self):
        messages, next_activities = self._action_done()
        return messages.ids and messages.ids[0] or False









