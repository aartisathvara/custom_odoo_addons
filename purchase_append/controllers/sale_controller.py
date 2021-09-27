# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, route

class SaleController(http.Controller):
    @http.route("/check_sale_order", type="http", website=True, auth="public")
    def check_sale_order(self):
        sale_orders = request.env["sale.order"].sudo().search([])
        return request.render(
            "purchase_append.sale_order_page", {"sale_orders": sale_orders}
        )

    @http.route("/view_sale_order", type="http", website=True, auth="public")
    def view_sale_order(self,**post):
        if post:
            sale_id = post["sale_orders"]
            invoice_add = request.env["sale.order"].browse(int(sale_id)).partner_invoice_id
            invoice_address = (invoice_add.street + " " + (invoice_add.street2 or "") + " "
                    + invoice_add.city + " " + (invoice_add.state_id and invoice_add.state_id.name or "")
                    + " " + (invoice_add.country_id and invoice_add.country_id.name or ""))

            delivery_add = request.env["sale.order"].browse(int(sale_id)).partner_shipping_id
            delivery_address = (delivery_add.street + " " + (delivery_add.street2 or "")
                    + " " + delivery_add.city + " " + (delivery_add.state_id and delivery_add.state_id.name or "")
                    + " " + (delivery_add.country_id and delivery_add.country_id.name or ""))

            vals = {
                "sale_data": request.env["sale.order"].browse(sale_id),
                "partner_invoice_address": invoice_address,
                "partner_delivery_address": delivery_address,
            }

            tracking_order_vals = {"sales_order_ref": sale_id, "user_name": request._uid}
            request.env["tracking.order"].create(tracking_order_vals)

            return request.render("purchase_append.view_sale_order_page", vals)
