# -*- coding: utf-8 -*-
import json
from odoo import http
from odoo.http import request, route
from odoo.addons.website.controllers.main import Website

class Controller(http.Controller):
    @http.route("/contacts", type="http", website=True, auth="public")
    def demo_page(self):
        contacts = request.env['res.partner'].sudo().search([], order='name asc')
        return request.render("frontend_session.contacts_list", {'contacts': contacts})

class portal(Website):
    @http.route(['/', '/..'], type='http', auth="public", website=True, sitemap=True)
    def index(self, **kw):

        # test =  super().index()
        print("called-------------------------------")
        # return test
        return request.redirect("/contacts")
