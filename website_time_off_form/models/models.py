# -*- coding: utf-8 -*-

from odoo import models, fields, api


class hr_holidays_time_off_form_custom(models.Model):
    _inherit = "hr.leave"

    demo = fields.Char(string='demo')
