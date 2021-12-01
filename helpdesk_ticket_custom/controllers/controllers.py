# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import content_disposition, Controller, request, route

# class OdooControllers(http.Controller):
#
#     @http.route(['/ticket'], type='json', auth='public', website=True)
#     def get_helpdesk_tickets(self, **kw):
#         # Se guarda en un str, sudo es para dar permisos todos los campos y search [] nos trae todos los datos
#         sub_group = http.request.env['helpdesk_project'].sudo().search([])
#         # Se crea una variable tipo lista
#         sg = []
#         # Se recorre los id y llamamos los otros campos para no enviar solo id
#         for sub_group in sub_group:
#             n = {
#                 "name": sub_group.name,
#                 "id": sub_group.id,
#             }
#             # append permite guarda en el array sg en cada recorrido del for
#             sg.append(n)
#         # retornamos el array sg
#         return sg


