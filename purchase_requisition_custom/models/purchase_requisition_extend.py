# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError


class purchase_requisition_extend(models.Model):
    _inherit = 'purchase.requisition'

    manager_id = fields.Many2one(comodel_name='hr.employee', related='user_id.employee_id.parent_id', string='Jefe inmediato',
                             help='Jefe inmediato respondable de su aprobación')
    available = fields.Boolean(string='habilitado', compute='_domain_ochange_x_partner')
    activity_id = fields.Integer(string='id actividad')

    @api.model
    def _domain_ochange_x_partner(self):
        if self.state == 'ongoing' or self.state == 'open':
            self.write({'available': True})
        else:
            self.write({'available': False})

    # función botón cancelar
    def action_cancel_extend(self):
        #  Marca actividad como hecha de forma automatica
        new_activity = self.env['mail.activity'].search([('id', '=', self.activity_id)], limit=1)
        new_activity.action_feedback(feedback='Es rechazado')
        # try to set all associated quotations to cancel state
        if self.manager_id.user_id == self.env.user:
            for requisition in self:
                for requisition_line in requisition.line_ids:
                    requisition_line.supplier_info_ids.unlink()
                requisition.purchase_ids.button_cancel()
                for po in requisition.purchase_ids:
                    po.message_post(body=_('Cancelled by the agreement associated to this quotation.'))
            self.write({'state': 'cancel'})
        else:
            raise UserError(_('No cuenta con el permiso para rechazar acuerdos de compra, por favor comunicarse con su jefe inmediato para aprobar este acuerdo de compra.'))

    # función del boton validar
    def action_in_progress_extend(self):
        self.ensure_one()
        if not self.line_ids:
            raise UserError(_("You cannot confirm agreement '%s' because there is no product line.", self.name))
        if self.type_id.quantity_copy == 'none' and self.vendor_id:
            for requisition_line in self.line_ids:
                if requisition_line.price_unit <= 0.0:
                    raise UserError(_('You cannot confirm the blanket order without price.'))
                if requisition_line.product_qty <= 0.0:
                    raise UserError(_('You cannot confirm the blanket order without quantity.'))
                requisition_line.create_supplier_info()
            self.write({'state': 'ongoing'})
        else:
            self.write({'state': 'in_progress'})
            # suscribe el contacto que es gerente del representante del proveedor en acuerdos de compra
            self.message_subscribe(self.manager_id.user_id.partner_id.ids)

            # Código que crea una nueva actividad
            model_id = self.env['ir.model']._get(self._name).id
            create_vals = {
                'activity_type_id': 4,
                'summary': 'Acuerdo de compra:',
                'automated': True,
                'note': 'A sido asignado para aprovar el siguiente acuerdo de compra',
                'date_deadline': self.date_end.date(),
                'res_model_id': model_id,
                'res_id': self.id,
                'user_id': self.manager_id.user_id.id
            }
            new_activity = self.env['mail.activity'].create(create_vals)
            # Escribe el id de la actividad en un campo
            self.write({'activity_id': new_activity})

    # Función del boton aprovación
    def action_approve(self):
        if self.manager_id.user_id == self.env.user:
            # Cambio de etapa
            self.write({'state': 'open'})
            #  Marca actividad como hecha de forma automatica
            new_activity = self.env['mail.activity'].search([('id', '=', self.activity_id)], limit=1)
            new_activity.action_feedback(feedback='Es aprobado')
        else:
            raise UserError(_('No cuenta con el permiso para aprobar acuerdos de compra, por favor comunicarse con su jefe inmediato para aprobar este acuerdo de compra.'))















