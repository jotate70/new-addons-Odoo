# -*- coding: utf-8 -*-
# from odoo import http


# class HelpdeskStockCustom(http.Controller):
#     @http.route('/helpdesk_stock_custom/helpdesk_stock_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/helpdesk_stock_custom/helpdesk_stock_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('helpdesk_stock_custom.listing', {
#             'root': '/helpdesk_stock_custom/helpdesk_stock_custom',
#             'objects': http.request.env['helpdesk_stock_custom.helpdesk_stock_custom'].search([]),
#         })

#     @http.route('/helpdesk_stock_custom/helpdesk_stock_custom/objects/<model("helpdesk_stock_custom.helpdesk_stock_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('helpdesk_stock_custom.object', {
#             'object': obj
#         })
