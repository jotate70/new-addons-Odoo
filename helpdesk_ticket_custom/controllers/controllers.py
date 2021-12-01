# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import content_disposition, Controller, request, route

class user_ticket(http.Controller):
    @route(['/helpdesk'], type='http', auth='user', website=True)
    def account(self, redirect=None, **post):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values.update({
            'error': {},
            'error_message': [],
        })

        if post and request.httprequest.method == 'POST':
            error, error_message = self.details_form_validate(post)
            values.update({'error': error, 'error_message': error_message})
            values.update(post)
            if not error:
                values = {key: post[key] for key in self.MANDATORY_BILLING_FIELDS}
                values.update({key: post[key] for key in self.OPTIONAL_BILLING_FIELDS if key in post})
                for field in set(['country_id', 'state_id']) & set(values.keys()):
                    try:
                        values[field] = int(values[field])
                    except:
                        values[field] = False
                values.update({'zip': values.pop('zipcode', '')})
                partner.sudo().write(values)
                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/home')

        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])

        values.update({
            'partner': partner,
            'countries': countries,
            'states': states,
            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'redirect': redirect,
            'page_name': 'my_details',
        })

# class OdooControllers(http.Controller):
#
#     @http.route(['/ticket'], type='json', auth='public', website=True)
#     def get_helpdesk_tickets(self, **kw):
#         # Se guarda en un str, sudo es para dar permisos todos los campos y search [] nos trae todos los datos
#         sub_group = http.request.env['product.template'].sudo().search([])
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


