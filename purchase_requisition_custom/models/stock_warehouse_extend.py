from odoo import fields, models, api
from odoo.exceptions import UserError
import json

class stock_warehouse_extend(models.Model):
    _inherit = 'stock.warehouse'

    employee_id = fields.Many2many(comodel_name='hr.employee', relation='x_hr_employee_stock_warehouse_rel',
                     column1='stock_warehouse_id', column2='hr_employee_id', string='Empleado responsable',
                     help='Empleado que puede aprobar transferencias internas en el almacen')
    location_id = fields.Many2one(comodel_name="location_warehouse", string='Locación', help="Indica la locación/ciudad donde se encuentra el almacen")
    available_requisition = fields.Boolean(string='Puede usarse en requisiciones')
    code = fields.Char('Short Name', required=True, size=8, help="Short name used to identify your warehouse")
    transit_location_id_domain = fields.Char(compute='_domain_transit_location_id', readonly=True, store=False)
    transit_location_id = fields.Many2one(comodel_name='stock.location', string='Ubicación de transito',
                                          help='Solo se permite una ubicación de transito por almacen')
    transit_location = fields.Boolean(string='Ubicación de transito', compute='_compute_transit_location',
                                      help='Solo se permite una ubicación de transito por almacen', readonly=True)

    # Función que aplica filtro dinamico
    @api.depends('transit_location_id')
    def _domain_transit_location_id(self):
        for rec in self:
            rec.transit_location_id_domain = json.dumps(
                [('warehouse_id', '=', self.ids)])

    # validación limite para asociar almacen
    @api.depends('transit_location_id')
    def _compute_transit_location(self):
        if self.transit_location_id:
            self.transit_location = True
        else:
            self.transit_location = False

    # validación limite para asociar almacen
    @api.onchange('employee_id')
    def _compute_ticket_limit(self):
        c = 0
        for rec in self.employee_id:
            c = c + 1
            if c > 1:
                raise UserError('Solo puede asociar un usuario por almacen')

