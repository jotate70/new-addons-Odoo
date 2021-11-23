from odoo import http
from odoo.http import request

class time_off_from(http.Controller):
    @http.route('/time-off', type="http", auth="public", website=True)
    def patient_web_time_off_form(self, **kw):
        return http.request.render('website_time_off_form.create_website_time_off_form', {})

    @http.route('/create/time-off', type="http", auth="public", website=True)
    def create_web_time_off(self, **kw):
        request.env['hr.leave'].sudo().create(kw)
        return request.render("website_time_off_form.time-off-thanks", {})