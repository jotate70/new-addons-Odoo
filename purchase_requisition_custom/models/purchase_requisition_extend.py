# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError

class purchase_requisition_extend(models.Model):
    _inherit = 'purchase.requisition'

    manager_id = fields.Many2one(comodel_name='hr.employee', related='user_id.department_id.manager_id', string='Jefe del área',
                             help='Jefe inmediato respondable de su aprobación')
    manager2_id = fields.Many2one(comodel_name='hr.employee', related='manager_id.parent_id', string='Aprobación alternativa',
                             help='Cuando el jefe inmediato se encuentra ausente, debe aprobar el siguiente respondable')
    available = fields.Boolean(string='habilitado', compute='_domain_ochange_x_partner')
    activity_id = fields.Integer(string='id actividad')
    # Obtiene la fecha y hora actual
    current_date = fields.Datetime('Fecha actual', required=False, readonly=False, select=True,
                                   default=lambda self: fields.datetime.now())
    time_off = fields.Char(string='Disponibilidad', compute='_compute_number_of_days')
    time_off_related = fields.Boolean(string='Ausencia', related='manager_id.is_absent')
    purchase_ids2 = fields.One2many(comodel_name='stock.picking', inverse_name='requisition_id',
                                    string='Purchase Orders',
                                    states={'done': [('readonly', True)]})
    stock_picking_count = fields.Integer(compute='_compute_stock_picking_number', string='Numero de transferencias')
    show_picking = fields.Boolean(string='Picking',
                                  help='Mostrar/ocultar el campo cantidad de producto en stock')
    stock_picking_action = fields.Boolean(string='Tranferencia inmediata')
    c = fields.Integer(string='c')
    cc = fields.Integer(string='cc')
    No_rep = fields.Char(string='line_ids')
    array_rep = fields.Char(string='Ubicaciones repetidas')
    len_id = fields.Integer(string='longitud')

    def action_button(self):
        if self.stock_picking_action == True:
            self.stock_picking_action = False
        else:
            self.stock_picking_action = True

    # Función que genera las tranferencias dependiedo las ubicaciones a mover
    @api.onchange('stock_picking_action')
    def stock_picking_action_function(self):
        if self.line_ids:
            self.c = 0  # Reinicio de contador array 1
            location_dest = []  # Guarda id de las ubicaciones repetidas
            r = []
            picking_dest = []
            No_rep = []
            for rec in self.line_ids:
                self.cc = 0  # Reinicio de contador array 2
                self.c = self.c + 1  # Contador de aray 1
                for rec2 in self.line_ids:
                    self.cc = self.cc + 1  # Contador de aray 2
                    # optener lineas con ubicaciones repetidas
                    if rec.default_location_dest_id.id == rec2.default_location_dest_id.id and self.c != self.cc:  # posiciones con el mismo valor y valores de contador diferentes
                        location_dest.append(rec2.default_location_dest_id.id)
                        line = list(location_dest)
                        # self.No_rep = line
                        self.array_rep = list(set(location_dest))  # set solo deja un solo valor de los repetidos
                        r = list(set(location_dest))
                        self.len_id = len(list(set(location_dest)))  # len muestra el tamaño de la lista

                    # # optener lineas con ubicaciones no repetidas
                    elif rec.default_location_dest_id.id == rec2.default_location_dest_id.id and self.c == self.cc:  # posiciones con el mismo valor y valores de contador diferentes
                        location_dest.append(rec2.default_location_dest_id.id)
                        line = list(location_dest)
                        # self.No_rep = line
                        self.array_rep = list(set(location_dest))  # set solo deja un solo valor de los repetidos
                        r = list(set(location_dest))
                        self.len_id = len(list(set(location_dest)))  # len muestra el tamaño de la lista

            for rec3 in self.line_ids:
                if rec3.inventory_product_qty > 0:
                    picking_dest.append(rec3.default_location_dest_id.id)
                    picking = list(picking_dest)
                    move_li = list(set(picking_dest))
                    # self.No_rep = picking

            count_stock1 = 0
            count1 = []
            count2 = []
            w = 0
            for count1 in self.line_ids:
                count_stock2 = 0
                count_stock1 = count_stock1 + 1  # para usar en condición de cantidades de tranferencia inmediata
                for count2 in self.line_ids:
                    count_stock2 = count_stock2 + 1  # para usar en condición de cantidades de tranferencia inmediata

                    # Cración de registros tranferecia inmediata no repetidas
                    if self.len_id == self.c and count_stock1 < 2 and count2.inventory_product_qty > 0:  # Casos ubicaciones no repetidos
                        create_vals = {
                            'scheduled_date': self.date_end,
                            'location_id': count2.property_stock_inventory.id,
                            'picking_type_id': count2.picking_type_id.id,
                            'location_dest_id': count2.default_location_dest_id.id,
                        }
                        stock_picking_id = self.env['stock.picking'].sudo().create(create_vals)
                        # Cración de registros linea de productos de tranferecia inmediata
                        create_vals2 = {
                            'name': count2.name_picking,
                            'picking_id': stock_picking_id.id,
                            'product_id': count2.product_id.id,
                            'product_uom': 1,
                            'product_uom_qty': count2.inventory_product_qty,
                            'quantity_done': 0,
                            'description_picking': count2.name_picking,
                            'location_id': count2.picking_type_id.id,
                            'location_dest_id': count2.default_location_dest_id.id,
                            'date_deadline': self.date_end,
                        }
                        self.env['stock.move'].sudo().create(create_vals2)


                    # Para casos donde lienas repetidas sean la misma ubicación
                    elif self.len_id == 1 and count_stock1 <= 1 and count2.inventory_product_qty > 0:
                        if count_stock2 <= 1:
                            create_vals = {
                                'scheduled_date': self.date_end,
                                'location_id': count2.property_stock_inventory.id,
                                'picking_type_id': count2.picking_type_id.id,
                                'location_dest_id': count2.default_location_dest_id.id,
                            }
                            stock_picking_id = self.env['stock.picking'].sudo().create(create_vals)
                        # Cración de registros linea de productos de tranferecia inmediata
                        create_vals2 = {
                            'name': count2.name_picking,
                            'picking_id': stock_picking_id.id,
                            'product_id': count2.product_id.id,
                            'product_uom': 1,
                            'product_uom_qty': count2.inventory_product_qty,
                            'quantity_done': 0,
                            'description_picking': count2.name_picking,
                            'location_id': count2.picking_type_id.id,
                            'location_dest_id': count2.default_location_dest_id.id,
                            'date_deadline': self.date_end
                            }
                        self.env['stock.move'].sudo().create(create_vals2)

                w = 0
                # Para casos donde exista lienas repetidas
                if self.len_id > 1 and self.len_id < self.c and count1.inventory_product_qty > 0:
                    for lacation in r:
                        w = w + 1
                        # if lacation == count1.default_location_dest_id.id:
                        if count_stock1 < 2:
                            create_vals = {
                                'scheduled_date': self.date_end,
                                'location_id': count1.property_stock_inventory.id,
                                'picking_type_id': count1.picking_type_id.id,
                                'location_dest_id': lacation,
                               }
                            stock_picking_id = self.env['stock.picking'].sudo().create(create_vals)
                        create_vals2 = {
                            'name': count1.name_picking,
                            'picking_id': stock_picking_id.id,
                            'product_id': count1.product_id.id,
                            'product_uom': 1,
                            'product_uom_qty': count1.inventory_product_qty,
                            'quantity_done': 0,
                            'description_picking': count1.name_picking,
                            'location_id': count1.picking_type_id.id,
                            'location_dest_id': count1.default_location_dest_id.id,
                            'date_deadline': self.date_end,
                            }
                        self.env['stock.move'].sudo().create(create_vals2)


    # Cuenta las trasnferencias inmediatas asociadas a la acuerdo de compra
    @api.depends('purchase_ids2')
    def _compute_stock_picking_number(self):
        for requisition in self:
            requisition.stock_picking_count = len(requisition.purchase_ids2)

    # Indica si el jefe inmediato está o no está ausente
    @api.depends('time_off_related')
    def _compute_number_of_days(self):
        if self.time_off_related == False:
            self.time_off = 'Disponible'
        else:
           self.time_off = 'Ausente'
           self.write({'manager2_id': self.manager_id.parent_id})
        return self.time_off

    # Sirve para indicar si está habilitado para aprobar solicitudes de compra
    @api.model
    def _domain_ochange_x_partner(self):
        if self.state == 'ongoing' or self.state == 'open':
            self.write({'available': True})
        else:
            self.write({'available': False})

    # función botón cancelar
    def action_cancel_extend(self):
        if self.manager_id.user_id == self.env.user or (self.manager2_id.user_id == self.env.user and self.time_off_related == True):
            #  Marca actividad como hecha de forma automatica
            new_activity = self.env['mail.activity'].search([('id', '=', self.activity_id)], limit=1)
            new_activity.action_feedback(feedback='Es rechazado')
            # try to set all associated quotations to cancel state
            for requisition in self:
                for requisition_line in requisition.line_ids:
                    requisition_line.supplier_info_ids.unlink()
                requisition.purchase_ids.button_cancel()
                for po in requisition.purchase_ids:
                    po.message_post(body=_('Cancelled by the agreement associated to this quotation.'))
            self.write({'state': 'cancel'})
        else:
            raise UserError('No cuenta con el permiso para rechazar acuerdos de compra, por favor comunicarse con su jefe inmediato para aprobar este acuerdo de compra.')

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
        #     Crear actividad al jefe inmediato si esta disponible
        elif self.manager_id and self.time_off_related == False:
            self.write({'state': 'in_progress'})
            # suscribe el contacto que es gerente del representante del proveedor en acuerdos de compra
            self.message_subscribe(self.manager_id.user_id.partner_id.ids)
            # Código que crea una nueva actividad
            model_id = self.env['ir.model']._get(self._name).id
            create_vals = {
                'activity_type_id': 4,
                'summary': 'Acuerdo de compra:',
                'automated': True,
                'note': 'A sido asignado para aprobar el siguiente acuerdo de compra',
                'date_deadline': self.current_date.date(),
                'res_model_id': model_id,
                'res_id': self.id,
                'user_id': self.manager_id.user_id.id
            }
            new_activity = self.env['mail.activity'].create(create_vals)
            # Escribe el id de la actividad en un campo
            self.write({'activity_id': new_activity})
        #     Crear actividad al jefe del jefe inmediato si esta ausente
        elif self.manager_id and self.time_off_related == True:
            self.write({'state': 'in_progress'})
            # suscribe el contacto que es gerente del representante del proveedor en acuerdos de compra
            self.message_subscribe(self.manager2_id.user_id.partner_id.ids)
            # Código que crea una nueva actividad
            model_id = self.env['ir.model']._get(self._name).id
            create_vals = {
                'activity_type_id': 4,
                'summary': 'Acuerdo de compra:',
                'automated': True,
                'note': 'A sido asignado para aprobar el siguiente acuerdo de compra, el jefe responsable se encuentra ausente',
                'date_deadline': self.current_date.date(),
                'res_model_id': model_id,
                'res_id': self.id,
                'user_id': self.manager2_id.user_id.id
            }
            new_activity = self.env['mail.activity'].create(create_vals)
            # Escribe el id de la actividad en un campo
            self.write({'activity_id': new_activity})
        # Set the sequence number regarding the requisition type / Agrega la secuencia de acuerdo de compra
        if self.name == 'New':
            if self.is_quantity_copy != 'none':
                self.name = self.env['ir.sequence'].next_by_code('purchase.requisition.purchase.tender')
            else:
                self.name = self.env['ir.sequence'].next_by_code('purchase.requisition.blanket.order')

    # Función del boton aprobación, y tambien puede aprobar el jefe inmediato si no se encuentra el responsable de aprobación
    def action_approve(self):
        if self.manager_id.user_id == self.env.user or (self.manager2_id.user_id == self.env.user and self.time_off_related == True):
            # Cambio de etapa
            self.write({'state': 'open'})
            #  Marca actividad como hecha de forma automatica
            new_activity = self.env['mail.activity'].search([('id', '=', self.activity_id)], limit=1)
            new_activity.action_feedback(feedback='Es aprobado')
        else:
            raise UserError('No cuenta con el permiso para aprobar acuerdos de compra, por favor comunicarse con su jefe inmediato para aprobar este acuerdo de compra.')























