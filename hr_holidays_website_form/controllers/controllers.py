from odoo import http
from odoo.http import request

class Ausencias(http.Controller):
    @http.route(['/time-off'], type='http', auth="public", website=True)
    def time_off_form(self, **kw):
        return http.request.render('hr_holidays_website_form.website_time_off', {})

    @http.route(['/time-off-submited'], type='http', auth="public", website=True)
    def time_off_submited(self, **kw):
        request.env['hr.leave'].sudo().create(kw)
        return http.request.render('hr_holidays_website_form.time_off_submited', {})



