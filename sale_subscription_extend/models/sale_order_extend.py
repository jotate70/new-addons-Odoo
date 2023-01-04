# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError

class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = "sale.order"

    sale_order_type = fields.Many2one(string='Tipo de orden', comodel_name='sale_order_type',
                                      help='Indicates the type of order, depending on the option allows you to activate '
                                           'subscription or inventory movement')
    approve_manager_origin = fields.Many2one(comodel_name='hr.employee', string='Responsable de aprobación original',
                                             related='user_id.employee_id.department_id.manager_id',
                                             help='Jefe responsable de la orden de compra o requisición')
    approve_manager = fields.Many2one(comodel_name='hr.employee', string='Responsable de aprobación',
                                      related='user_id.employee_id.department_id.manager_id',
                                      help='Jefe responsable de aprobar la solicitud de compra')
    activity_id = fields.Integer(string='id actividad')
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('approve', 'Aprobado'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),],
        string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    time_off = fields.Char(string='Disponibilidad', compute='_compute_number_of_days')
    time_off_related = fields.Boolean(string='Ausencia', related='approve_manager.is_absent')
    demo = fields.Char('demo')

    # Herencia del modelo cretae para crear tipo de ordenes si no existen
    @api.onchange('sale_order_type')
    def _create_sale_order_type(self):
        # Codigo adicional
        vat = []
        order = self.env['sale_order_type']
        for rec in order:
            vat.append(rec.id)
        count = len(vat)
        if count > 0:
            create_vals = {
                'id': 1,
                'name': 'example_1',
                'order_type': 'sale',
                'allow_stock_picking': False,
                'allow_approve': True,
            }
            self.env['sale_order_type'].create(create_vals)
        else:
            return

    # Indica si el jefe inmediato está o no está ausente
    @api.depends('time_off_related')
    def _compute_number_of_days(self):
        if self.time_off_related == False:
            self.time_off = 'Disponible'
        else:
            self.time_off = 'Ausente'
            # Para el caso de cuando no es un gerente general o una persona con limite de presupuesto
            if self.approve_manager.general_manager == False:
                self.write({'manager2_id': self.approve_manager.parent_id})
            # Para el caso de cuando es un gerente general o una persona sin tope de presupuesto
            else:
                self.write({'manager2_id': self.approve_manager.parent_optional_id})
        return self.time_off

    def action_demo(self):
        self.write({'state': 'draft'})

    # Update state approve
    def action_approve_sale(self):
        if self.approve_manager == self.env.user.employee_id:
            self.action_confirm()
        else:
            raise UserError('No cuenta con el permiso para aprobar la solicitud, por favor comunicarse con su jefe inmediato para aprobar esta solicitud.')

    def action_confirm(self):
        c = 0
        for rec in self.order_line:
            c += 1
        if c == 0:
            raise UserError('No se ha agregado productos en la cotización.')
        if self.sale_order_type:
            if self.sale_order_type.allow_approve == True and self.state != 'approve':
                self.write({'state': 'approve'})
                # Código que crea una nueva actividad
                model_id = self.env['ir.model']._get(self._name).id
                create_vals = {
                    'activity_type_id': 4,
                    'summary': 'Solicitud de compra:',
                    'automated': True,
                    'note': 'Ha sido asignado para aprobar la siguiente solicitud',
                    'date_deadline': fields.Datetime.now(),
                    'res_model_id': model_id,
                    'res_id': self.id,
                    'user_id': self.user_id.employee_id.department_id.manager_id.id,
                }
                new_activity = self.env['mail.activity'].create(create_vals)
                # Escribe el id de la actividad en un campo
                self.write({'activity_id': new_activity})

            elif self.state == 'approve' and self.approve_manager.user_id == self.env.user:
                #  Marca actividad como hecha de forma automatica
                new_activity = self.env['mail.activity'].search([('id', '=', self.activity_id)], limit=1)
                new_activity.action_feedback(feedback='Es aprobado')
                if self._get_forbidden_state_confirm() & set(self.mapped('state')):
                    raise UserError(_(
                        'It is not allowed to confirm an order in the following states: %s'
                        ) % (', '.join(self._get_forbidden_state_confirm())))
                for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
                    order.message_subscribe([order.partner_id.id])
                self.write(self._prepare_confirmation_values())
                # Context key 'default_name' is sometimes propagated up to here.
                # We don't need it and it creates issues in the creation of linked records.
                context = self._context.copy()
                context.pop('default_name', None)
                self.with_context(context)._action_confirm()
                if self.env.user.has_group('sale.group_auto_done_setting'):
                    self.action_done()
                return True
            else:
                raise UserError('No tienes un responsable asociado.')
        else:
            raise UserError('No tiene un tipo de orden seleccionada')

    # Action confirm stock picking
    def _action_confirm(self):
        if self.sale_order_type.allow_stock_picking == True and self.sale_order_type.allow_suscription == True:
            self.order_line._action_launch_stock_rule()
            return super(SaleOrder, self)._action_confirm()
        else:
            return

    def create_subscriptions(self):
        """
        Create subscriptions based on the products' subscription template.

        Create subscriptions based on the templates found on order lines' products. Note that only
        lines not already linked to a subscription are processed; one subscription is created per
        distinct subscription template found.

        :rtype: list(integer)
        :return: ids of newly create subscriptions
        """
        res = []
        for order in self:
            to_create = order._split_subscription_lines()
            # create a subscription for each template with all the necessary lines
            for template in to_create:
                values = order._prepare_subscription_data(template)
                values['recurring_invoice_line_ids'] = to_create[template]._prepare_subscription_line_data()
                values['recurring_invoice_line_2_ids'] = to_create[template]._prepare_subscription_line_data()
                subscription = self.env['sale.subscription'].sudo().create(values)
                subscription.onchange_date_start()
                res.append(subscription.id)
                to_create[template].write({'subscription_id': subscription.id})
                subscription.message_post_with_view(
                    'mail.message_origin_link', values={'self': subscription, 'origin': order},
                    subtype_id=self.env.ref('mail.mt_note').id, author_id=self.env.user.partner_id.id
                )
                self.env['sale.subscription.log'].sudo().create({
                    'subscription_id': subscription.id,
                    'event_date': fields.Date.context_today(self),
                    'event_type': '0_creation',
                    'amount_signed': subscription.recurring_monthly,
                    'recurring_monthly': subscription.recurring_monthly,
                    'currency_id': subscription.currency_id.id,
                    'category': subscription.stage_category,
                    'user_id': order.user_id.id,
                    'team_id': order.team_id.id,
                })
        return res

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    available_quantity_total = fields.Float(string='Stock', related='product_id.available_stock',
                                            help='Muestra la cantidad disponible que está sin reservar')

