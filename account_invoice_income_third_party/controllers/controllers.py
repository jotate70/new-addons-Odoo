# -*- coding: utf-8 -*-
from odoo import http

# class /odoo/odoo-server/addons/accountInvoiceIngresoParaTerceros(http.Controller):
#     @http.route('//odoo/odoo-server/addons/account_invoice_income_third_party//odoo/odoo-server/addons/account_invoice_income_third_party/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//odoo/odoo-server/addons/account_invoice_income_third_party//odoo/odoo-server/addons/account_invoice_income_third_party/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('/odoo/odoo-server/addons/account_invoice_income_third_party.listing', {
#             'root': '//odoo/odoo-server/addons/account_invoice_income_third_party//odoo/odoo-server/addons/account_invoice_income_third_party',
#             'objects': http.request.env['/odoo/odoo-server/addons/account_invoice_income_third_party./odoo/odoo-server/addons/account_invoice_income_third_party'].search([]),
#         })

#     @http.route('//odoo/odoo-server/addons/account_invoice_income_third_party//odoo/odoo-server/addons/account_invoice_income_third_party/objects/<model("/odoo/odoo-server/addons/account_invoice_income_third_party./odoo/odoo-server/addons/account_invoice_income_third_party"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/odoo/odoo-server/addons/account_invoice_income_third_party.object', {
#             'object': obj
#         })