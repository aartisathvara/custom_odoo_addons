# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request,route
import datetime
from odoo.addons.portal.controllers.portal import CustomerPortal

class ExistingOrderController(http.Controller):
    # @http.route('/order_info', auth='public', type='http', website=True)
    # def portal_get_existing_order_detail(self, **kw):
    #     values = {'state': dict(request.env['sale.order']._fields['state'].selection),
    #               }
    #     if kw:
    #         print("\n\n\nkw\n\n\n", kw)
    #         start_date = datetime.strptime(kw.get('start_date'), "%Y-%m-%d")
    #         end_date = datetime.strptime(kw.get('end_date'), "%Y-%m-%d")
    #         start_date_time = datetime.combine(start_date, datetime.strptime('000000', '%H%M%S').time())
    #         end_date_time = datetime.combine(end_date, datetime.strptime('235959', '%H%M%S').time())
    #         domain = [("date_order", '>=', start_date_time),
    #                   ("date_order", '<=', end_date_time), ("state", "=", kw.get("state")), ]
    #         if kw.get('state') == "all":
    #             print("innnnnnnnnnnnnnnnnnn")
    #             domain += [("date_order", '>=', start_date_time),
    #                        ("date_order", '<=', end_date_time), ]
    #         sale_data = request.env["sale.order"].search(domain)
    #         # pager = request.website.pager(
    #         #         url='/order_info',
    #         #         total=total,
    #         #         page=page,
    #         #         step=4,
    #         #         )
    #         # offset = pager['offset']
    #         # print ("??????", domain, sale_data)
    #         values.update({
    #             'sale_order': sale_data,
    #             'get_kw': True,
    #             'st': kw.get('start_date'),
    #             'en': kw.get('end_date'),
    #             'sta': kw.get("state"),
    #         })
    #         sale_order_data = request.env["sale.order"].sudo().search(domain)
    #         values.update({"sale_order_data": sale_order_data})
    #     return request.render("students.order_record_form", values)


    @http.route('/check_existing_order', auth='public',website=True)
    def check_existing_order(self,**post):
        if post:
            print("===if post===",post)
            if post['start_date'] and post['end_date'] and post['status']:

                print("====post if===",post)

                start_date = datetime.datetime.strptime(post['start_date'], '%Y-%m-%d').date()
                print("===strat date==",start_date)

                end_date = datetime.datetime.strptime(post['end_date'], '%Y-%m-%d').date()
                print("===end= date===",end_date)
                print(type(start_date),"=====",type(end_date),"====post tstae===",post['status'])

                sale_orders = request.env['sale.order'].search([('date_order','>=',start_date),('date_order','<=',end_date),
                                                               ('state','=',post['status'])])
                print("=====saleorder===",sale_orders)


                return request.render("sale_customer_city.existing_order_page", {'sale_orders': sale_orders})

        states = dict(request.env['sale.order'].fields['state'].selection)
        print('=====states==',states)
        return request.render("sale_customer_city.existing_order_page",{'states':states})

    # @http.route("/search_sale_order", type="http", website=True, auth="public")
    # def search_sale_order(self, **post):
    #     print("====self===",self)
    #     if post:
    #         print("===if post===", post)
    #         if post['start_date'] and post['end_date'] and post['status']:
    #             print("====post if===", post)
    #
    #             start_date = datetime.datetime.strptime(post['start_date'], '%Y-%m-%d').date()
    #             print("===strat date==", start_date)
    #
    #             end_date = datetime.datetime.strptime(post['end_date'], '%Y-%m-%d').date()
    #             print("===end= date===", end_date)
    #             print(type(start_date), "=====", type(end_date), "====post tstae===", post['status'])
    #
    #             sale_orders = request.env['sale.order'].search(
    #                 [('date_order', '>=', start_date), ('date_order', '<=', end_date),
    #                  ('state', '=', post['status'])])
    #             print("=====saleorder===", sale_orders)
    #             return request.render('sale_customer_city.submit_sale_order',{'sale_orders':sale_orders})


class CustomCustomerPortal(CustomerPortal):
    OPTIONAL_BILLING_FIELDS = ["zipcode", "state_id", "vat", "company_name","my_name"]
    @route(['/my/account'], type='http', auth='user', website=True)
    def account(self, redirect=None, **post):
        print("===res===",self)
        return super(CustomCustomerPortal, self).account(**post)