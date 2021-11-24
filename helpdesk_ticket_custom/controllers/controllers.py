# -*- coding: utf-8 -*-
from odoo import http


class helpdesk_ticket_website_form(http.Controller):

    @http.route('/academy/<model("teachers"):teacher>/', auth='public', website=True)
    def teacher(self, teacher):
        return http.request.render('helpdesk_ticket_custom.teachers', {
            'person': teacher
        })

