# -*- coding: utf-8 -*-
# from odoo import http


# class Cabinet(http.Controller):
#     @http.route('/cabinet/cabinet', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cabinet/cabinet/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('cabinet.listing', {
#             'root': '/cabinet/cabinet',
#             'objects': http.request.env['cabinet.cabinet'].search([]),
#         })

#     @http.route('/cabinet/cabinet/objects/<model("cabinet.cabinet"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cabinet.object', {
#             'object': obj
#         })
