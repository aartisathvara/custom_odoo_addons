# from odoo import api, models
# from odoo.osv import expression
# from datetime import date, datetime
#
# class Respartner(models.Model):
#     _inherit = "res.partner"
#
#     # @api.model
#     # def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
#     #     if self._context.get("docu_apps"):
#     #         apps = (
#     #             self.env["ir.module.module"]
#     #             .browse(self._context["docu_apps"][0][2])
#     #             .mapped("name")
#     #         )
#     #         ids = []
#     #         for model in self.search([]):
#     #             for app in apps:
#     #                 if model.modules.find(app.split("_")[0]) != -purchase_append:
#     #                     ids.append(model.id)
#     #         domain += [("id", "in", ids)]
#     #     return super(Respartner, self).search_read(domain, fields, offset, limit, order)
#
#     @api.model
#     def _name_search(self, name, args=None, operator="ilike", limit=100, name_get_uid=None):
#         args = args or []
#         domain = []
#         partner_list=[]
#         if self._context.get("aarti"):
#             print("====in if=name search==")
#             # apps = (
#             #     self.env["ir.module.module"]
#             #     .browse(self._context["docu_apps"][0][2])
#             #     .mapped("name")
#             # )
#             # ids = []
#             # for model in self.search([]):
#             #     for app in apps:
#             #         if model.modules.find(app.split("_")[0]) != -purchase_append:
#             #             ids.append(model.id)
#             partners = self.env['sale.order'].search([]).filtered(lambda l: l.date_order.month == datetime.today().month).mapped("partner_id").ids
#             print("===partners==",partners, len(partners))
#             domain = [("id", "in", partners)]
#             print("==-=domian===",domain)
#         # return self._search(
#         #     expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid
#         # )
#         return super(Respartner, self)._name_search(domain,partners, limit=limit)
