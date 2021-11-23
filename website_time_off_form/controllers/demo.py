from odoo import http
from odoo.http import request

class demo(http.Controller):
    @http.route('/demo_time-off', type="http", auth="public", website=True)
    def demo_time_off_form(self, **kw):
        return http.request.render('website_time_off_form.demo_create_website_time_off_form', {})

    @http.route('/create/demo_time-off', type="http", auth="public", website=True)
    def demo_web_time_off(self, **kw):
        request.env['hr.leave'].sudo().create(kw)
        return request.render("website_time_off_form.demo_time-off-thanks", {})




