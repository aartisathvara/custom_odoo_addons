from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def sale_order_cron(self):
        sale_orders = self.search([("state", "not in", ["sale", "done"])])
        print("sale_orders===========", sale_orders)
