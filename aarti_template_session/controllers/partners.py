# -*- coding: utf-8 -*-/partners
from odoo import http
from odoo.http import request, route


class Controller(http.Controller):
    @http.route("/partners", type="http", website=True, auth="user")
    def demo_page(self):
        partners = request.env["res.partner"].sudo().search([])
        return request.render(
            "aarti_template_session.partner_page", {"partners": partners}
        )
