# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class train_transportation(models.Model):
#     _name = 'train_transportation.train_transportation'
#     _description = 'train_transportation.train_transportation'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

