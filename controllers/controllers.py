# -*- coding: utf-8 -*-
# from odoo import http


# class TrainTransportation(http.Controller):
#     @http.route('/train_transportation/train_transportation', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/train_transportation/train_transportation/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('train_transportation.listing', {
#             'root': '/train_transportation/train_transportation',
#             'objects': http.request.env['train_transportation.train_transportation'].search([]),
#         })

#     @http.route('/train_transportation/train_transportation/objects/<model("train_transportation.train_transportation"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('train_transportation.object', {
#             'object': obj
#         })

