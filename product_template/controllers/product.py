# -*- coding: utf-8 -*-/
from odoo import http
from odoo.http import request, route

class ProductTemplateController(http.Controller):
    @http.route("/product_template", type="http", website=True, auth="user")
    def product_template(self):
        product_template_list = request.env["product.template"].sudo().search([])
        return request.render(
            "product_template.product_template_list_page", {"product_template_list": product_template_list}
        )

    @http.route("/product/info/<model('product.template'):product>", type="http", website=True, auth="user")
    def product_info(self,product):
        return request.render(
            "product_template.product_info_page", {"product_info": product}
        )
