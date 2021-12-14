# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class time_off_website(models.Model):
#     _name = 'time_off_website.time_off_website'
#     _description = 'time_off_website.time_off_website'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
