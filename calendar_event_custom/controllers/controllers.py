# -*- coding: utf-8 -*-
# from odoo import http


# class CalendarEventCustom(http.Controller):
#     @http.route('/calendar_event_custom/calendar_event_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/calendar_event_custom/calendar_event_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('calendar_event_custom.listing', {
#             'root': '/calendar_event_custom/calendar_event_custom',
#             'objects': http.request.env['calendar_event_custom.calendar_event_custom'].search([]),
#         })

#     @http.route('/calendar_event_custom/calendar_event_custom/objects/<model("calendar_event_custom.calendar_event_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('calendar_event_custom.object', {
#             'object': obj
#         })
