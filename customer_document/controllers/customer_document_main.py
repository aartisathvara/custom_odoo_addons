# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request, route


class CustomerDocument(http.Controller):
    @http.route("/customer_document", type="http", website=True, auth="user")
    def customer_document(self):
        document_ids = request.env["customer.document"].search([])
        return request.render(
            "customer_document.customer_document_details_page",
            {"document_ids": document_ids},
        )

    @http.route("/customer_document_form", type="http", website=True, auth="user")
    def customer_document_form(self):
        partner_id = request.env["res.partner"].search([])
        return request.render(
            "customer_document.customer_document_form_page", {"partner_id": partner_id}
        )

    @http.route(
        "/insert_customer_document_record", type="http", website=True, auth="user"
    )
    def insert_customer_document_record(self, **post):
        if post:
            partner_id = request.env["res.partner"].search(
                [("name", "=like", post["partner_id"])]
            )
            vals = {
                "partner_id": partner_id.id,
                "age": post["age"] + " years",
            }
            request.env["customer.document"].sudo().create(vals)
        return request.render("customer_document.thank_you_template")
