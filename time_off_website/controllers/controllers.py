# -*- coding: utf-8 -*-
# from odoo import http


# class TimeOffWebsite(http.Controller):
#     @http.route('/time_off_website/time_off_website/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/time_off_website/time_off_website/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('time_off_website.listing', {
#             'root': '/time_off_website/time_off_website',
#             'objects': http.request.env['time_off_website.time_off_website'].search([]),
#         })

#     @http.route('/time_off_website/time_off_website/objects/<model("time_off_website.time_off_website"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('time_off_website.object', {
#             'object': obj
#         })
