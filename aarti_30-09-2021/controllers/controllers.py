# -*- coding: utf-8 -*-
# from odoo import http


# class Aarti30-09-2021(http.Controller):
#     @http.route('/aarti_30-09-2021/aarti_30-09-2021/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/aarti_30-09-2021/aarti_30-09-2021/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('aarti_30-09-2021.listing', {
#             'root': '/aarti_30-09-2021/aarti_30-09-2021',
#             'objects': http.request.env['aarti_30-09-2021.aarti_30-09-2021'].search([]),
#         })

#     @http.route('/aarti_30-09-2021/aarti_30-09-2021/objects/<model("aarti_30-09-2021.aarti_30-09-2021"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('aarti_30-09-2021.object', {
#             'object': obj
#         })
