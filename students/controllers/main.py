from odoo import http
from odoo.http import request
from odoo import api, fields, models, _
from datetime import datetime
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.exceptions import AccessError, MissingError
from collections import OrderedDict
import dateutil.parser
from dateutil.relativedelta import relativedelta

class CustomerPortal(CustomerPortal):

    MANDATORY_BILLING_FIELDS = ["name", "phone", "email", "street","new_field", "city", "country_id"]

    # @http.route('/students', auth='public', type='http', website=True)
    # def students_homepage(self):
    #     values = {
    #         'orders': request.env["students.profile"].search([])
    #     }
    #     return request.render("students.students_homepage_template", values)

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        print('\n\n\n', values)
        if 'students_count' in counters:
            values['students_count'] = request.env['students.profile'].search_count([])
        if 'teachers_count' in counters:
            values['teachers_count'] = request.env['teachers.profile'].search_count([])
        return values


    @http.route('/teachers', auth='public', type='http', website=True)
    def teachers_homepage(self):
        values = {
            'teachers': request.env["teachers.profile"].search([])
        }
        return request.render("students.teachers_homepage_template", values)    

    @http.route('/teachers/data/<int:teacher_id>', type='http', auth='public', website=True)
    def sale_details(self , teacher_id,**kwargs):
        values = request.env["teachers.profile"].sudo().browse(teacher_id)
        return request.render('students.teachers_detail_view', {'teachers': values})
    

    def _order_get_page_view_values(self, record, access_token, **kwargs):
        values = {
            'students_profile': record,
            'teachers_profile': record,
            'token': access_token,
            # 'return_url': '/students',
            'bootstrap_formatting': True,
            'partner_id': record.partner_id.id,
            'report_type': 'html',
            'action': record._get_portal_return_action(),
        }
        print("\n\n\n\n...........values student\n\n\n\n", values)
        return values  

    @http.route(['/student/data/<int:student_id>'], type='http', auth="public", website=True)
    def portal_student_data(self, student_id, report_type=None,  access_token=None,  download=False, **kw):
        print ("???????????", student_id)
        try:
            order_sudo = self._document_check_access('students.profile', student_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/students')
 
        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=order_sudo, report_type=report_type, report_ref='students.report_student_card',download=download)

        # use sudo to allow accessing/viewing orders for public user
        # only if he knows the private token
        # Log only once a day
        if order_sudo:
            # store the date as a string in the session to allow serialization
            now = fields.Date.today().isoformat()
            session_obj_date = request.session.get('view_quote_%s' % order_sudo.id)
            if session_obj_date != now and request.env.user.share and access_token:
                request.session['view_quote_%s' % order_sudo.id] = now
                body = _('Quotation viewed by customer %s', order_sudo.partner_id.name)
                _message_post_helper(
                    "students.profile",
                    order_sudo.id,
                    body,
                    token=order_sudo.access_token,
                    message_type="notification",
                    subtype_xmlid="mail.mt_note",
                    partner_ids=order_sudo.user_id.sudo().partner_id.ids,
                )

        values = self._order_get_page_view_values(order_sudo, access_token, **kw)
        print("\n\n\n\n...........values student1\n\n\n\n", values)
        # values['message'] = message

        return request.render("students.student_portal_content", values)

    #sort BY AND filter By
    @http.route('/students', auth='public', type='http', website=True)
    def portal_student_detail(self, sortby=None, filterby=None, **kw):
        # partner = request.env.user.partner_id
        StudertDetails = request.env['students.profile']

        print("\n\nvhjvhjvhjvv......", kw)

        domain = []
        if kw.get("state") != "all" and kw.get("student_teacher"):
            domain += [("state", "=", kw.get("state")),("student_teacher","=",kw.get("student_teacher"))]
        if kw.get("state") == "all" and kw.get("student_teacher"):
            domain += [("student_teacher","=",kw.get("student_teacher"))]

        searchbar_sortings = {
            'name': {'label': _('Name'), 'students': 'name desc'},
            'phone': {'label': _('Phone'),'students': 'phone'}
        }        

        if not sortby:
            sortby = 'name'
        sort_students = searchbar_sortings[sortby]['students']


        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
            'stage': {'label': _('Stage'), 'domain': [('state', 'in', ['draft'])]},
        }

        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']

      
        values = {
            'page_name': 'student',
            'orders': StudertDetails.sudo().search(domain, order=sort_students),
            # 'pager': pager,
            'default_url': '/students',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby':filterby,
        }

        print("/n/n/n/n",values)

        return request.render("students.students_homepage_template", values)

    # @http.route('/students', auth='public', type='http', website=True)
    # def portal_my_students(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):

    #     searchbar_sortings = {
    #         'date': {'label': _('Date'), 'order': 'invoice_date desc'},
    #         'duedate': {'label': _('Due Date'), 'order': 'invoice_date_due desc'},
    #         'name': {'label': _('Reference'), 'order': 'name desc'},
    #         'state': {'label': _('Status'), 'order': 'state'},
    #     }
    #     # default sort by order
    #     if not sortby:
    #         sortby = 'date'
    #     order = searchbar_sortings[sortby]['order']

    #     searchbar_filters = {
    #         'all': {'label': _('All'), 'domain': [('move_type', 'in', ['in_invoice', 'out_invoice'])]},
    #         'invoices': {'label': _('Invoices'), 'domain': [('move_type', '=', 'out_invoice')]},
    #         'bills': {'label': _('Bills'), 'domain': [('move_type', '=', 'in_invoice')]},
    #     }
    #     # default filter by value
    #     if not filterby:
    #         filterby = 'all'
    #     domain += searchbar_filters[filterby]['domain']

    #     if date_begin and date_end:
    #         domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

    #     # count for pager
    #     invoice_count = AccountInvoice.search_count(domain)
    #     # pager
    #     pager = portal_pager(
    #         url="/my/invoices",
    #         url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
    #         total=invoice_count,
    #         page=page,
    #         step=self._items_per_page
    #     )
    #     # content according to pager and archive selected
    #     invoices = AccountInvoice.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
    #     request.session['my_invoices_history'] = invoices.ids[:100]

    #     values.update({
    #         'date': date_begin,
    #         'invoices': invoices,
    #         'page_name': 'invoice',
    #         'pager': pager,
    #         'default_url': '/my/invoices',
    #         'searchbar_sortings': searchbar_sortings,
    #         'sortby': sortby,
    #         'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
    #         'filterby':filterby,
    #     })
    #     return request.render("account.portal_my_invoices", values)   

    @http.route('/random', auth='public', type='http', website=True)
    def portal_random_detail(self): 

        student_teacher = request.env['teachers.profile'].search([])
        print("\n\n\n\n\n\n++++++++++++++++++++++++++",student_teacher)

        var = dict(request.env['students.profile']._fields['state'].selection)

        values = { 'state' : var,
                    'student_teacher' : student_teacher}


        redirect = request.render("students.student_record_form",values)
        return redirect


    @http.route('/order_info', auth='public', type='http', website=True)
    def portal_get_existing_order_detail(self, **kw):
        values = { 'state' : dict(request.env['sale.order']._fields['state'].selection),
                    }
        if kw:
            print("\n\n\nkw\n\n\n", kw)
            start_date = datetime.strptime(kw.get('start_date'), "%Y-%m-%d")
            end_date = datetime.strptime(kw.get('end_date'), "%Y-%m-%d")
            start_date_time = datetime.combine(start_date, datetime.strptime('000000','%H%M%S').time())
            end_date_time = datetime.combine(end_date, datetime.strptime('235959','%H%M%S').time())
            domain = [("date_order", '>=', start_date_time), 
                ("date_order", '<=', end_date_time),("state", "=", kw.get("state")),]
            if kw.get('state') == "all":
                print ("innnnnnnnnnnnnnnnnnn")
                domain += [("date_order", '>=', start_date_time), 
                ("date_order", '<=', end_date_time),]
            sale_data = request.env["sale.order"].search(domain)
            values.update({
                'sale_order': sale_data,
                'get_kw': True,
                'st' : kw.get('start_date'),
                'en' : kw.get('end_date'),
                'sta' : kw.get("state"),
            })
            sale_order_data = request.env["sale.order"].sudo().search(domain)
            values.update({"sale_order_data": sale_order_data})
        return request.render("students.order_record_form",values)

    # @http.route('/filter_sale', auth='public', type='http', website=True)
    # def sale_filter_detail(self, **kw):
    #     print("\n\n\nkw\n\n\n", kw)
    #     stt = request.env["sale.order"].search([])
    #     print("kkkkkkkkkkkkkkkkkkkkkkkkkkk........",stt)
    #     start_date = datetime.strptime(kw.get('start_date'), "%Y-%m-%d")
    #     end_date = datetime.strptime(kw.get('end_date'), "%Y-%m-%d")
    #     start_date_time = datetime.combine(start_date, datetime.strptime('000000','%H%M%S').time())
    #     end_date_time = datetime.combine(end_date, datetime.strptime('000000','%H%M%S').time())
    #     print ("??????", type(start_date_time), end_date_time)
    #     # {'start_date': '2021-09-10', 'end_date': '2021-09-24', 'state': 'sent'}
    #     # dat_order = dateutil.parser.parse(date_order).date()
    #     # sale_sr = sale_br.search([('date_order', '=',   self.from_date)])
    #     sale_data = request.env["sale.order"].search([("date_order", '>=', start_date_time), 
    #         ("date_order", '<=', end_date_time), ('state', '=', kw.get('state'))])
    #     vals = {
    #         'sale_order': sale_data
    #     }
    #     return request.render("students.sale_order_detail_view", vals)
        

class MyCustomWeb(http.Controller):

    @http.route(
        ["/contact","/contact/page/<int:page>"], type="http", auth="user", website=True
    )
    def res_kanban(self, page=0, search="", **post):
        domain = []
        if search:
            domain.append(("name", "ilike", search))
        post["search"] = search
        contact_obj = request.env["res.partner"].sudo().search(domain)
        print("\n\nkkkkkkkkkk......",contact_obj )
        total = contact_obj.sudo().search_count([])
        pager = request.website.pager(
            url="/contact",
            total=total,
            page=page,
            step=12,
        )
        offset = pager["offset"]
        contact_obj = contact_obj[offset : offset + 12]
        return request.render(
            "students.contact_form",
            {
                "search": search,
                "contact_details": contact_obj,
                "pager": pager,
            },
        )

    # def _order_get_page_view_values(self, record, access_token, **kwargs):
    #     values = {
    #         'res_partner': record,
    #         'token': access_token,
    #         'return_url': '/contact',
    #         'partner_id': record.partner_id.id,
    #     }
    #     return values

    # @http.route(['/contact/data/<int:partner_id>'], type='http', auth="public", website=True)
    # def portal_contact_data(self, partner_id, report_type=None,  access_token=None,  download=False, **kw):
    #     print ("???????????", partner_id)
    #     res_reslt = request.env["res.partner"].sudo().search()
    #     values = self._order_get_page_view_values(order_sudo, access_token, **kw)
    #     return request.render("students.res_portal_contact", values)        

    # @http.route(['/contact/data/<int:page>'], type='http', auth="public", website=True)
    # def portal_res_data(self, page=0, search="", **post):
    #     domain = []
    #     contact_obj = request.env["res.partner"].sudo().search(domain)
    #     print("\n\nkkkkkkkkkk......",contact_obj )
    #     total = contact_obj.sudo().search_count([])
    #     return request.render(
    #         "students.res_portal_contact",
    #         {
    #             "contact_details": contact_obj,
    #         },
    #     )

    @http.route('/contact/data/<int:partner_id>', type='http', auth='public', website=True)
    def sale_details(self , partner_id,**kwargs):
        contact = request.env["res.partner"].sudo().browse(partner_id)
        return request.render('students.partner_detail_view', {'contact': contact})
