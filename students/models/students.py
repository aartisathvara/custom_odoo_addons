# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"

    new_field = fields.Char(string="new field")
    em_age = fields.Integer(string="Employee Age")

    def get_vehicles(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Vehicles",
            "view_mode": "tree,form",
            "res_model": "purchase.order",
            # 'domain': [('driver_id', '=', self.id)],
            # 'context': "{'create': False}"
        }

    def _compute_access_url(self):
        for res in self:    
            return '/contact/data/%s' % (res.id)

    # def get_portal_url(self):
    #     # return {
    #     #     "url": "contact/page/self.id"
    #     #     "type": "ir.actions.act_url"
    #     # }
    #     url = "s%"% contact/page/self.id
    #     return url    

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_address = fields.Char(string="Address")

class SaleOrder(models.Model):
    _inherit = "sale.order"

    abc = fields.Char(string="Abc")


class StudentsProfile(models.Model):
    _name = "students.profile"
    _description = "students.profile"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    # _rec_name = "phone"


    def _compute_access_url(self):
        super(StudentsProfile, self)._compute_access_url()
        for stu in self:
            stu.access_url = '/student/data/%s' % (stu.id)

    name = fields.Char(string="Student Name", required=True, tracking=True)
    phone = fields.Char(string="Student Phone Number")
    email = fields.Char(string="Student Email ID")
    age = fields.Integer(string="Student Age", compute="_cal_age", store=True, readonly=True)
    result = fields.Float(string="Student Result")
    classes = fields.Boolean(string="Class Will be Online")
    address = fields.Text(string="Student Address")
    birthday = fields.Date(string="Student Birthday")
    joiningdate = fields.Datetime(string="Student School Joining date")
    gender = fields.Selection(
        [("girl", "Girl"), ("boy", "Boy"),("other","Other")], string="Student Gender"
    )
    marksheet = fields.Binary(string="Student Marksheet")
    photo = fields.Image(string="Student Photo", max_width=100, max_hight=100)
    description = fields.Html(string="Student Description")
    student_school = fields.Many2one("school.info", string="Student School Name")
    student_teacher = fields.Many2one(
        "teachers.profile", string="Students Teacher Details"
    )
    sc_type = fields.Char(string="Type Of School")
    user_id = fields.Many2one('res.users', string='user_id', default=lambda self: self.env.user)
    school_details = fields.One2many(
        "school.info", "stu_imforamtion", string="School Details"
    )
    students_datetime = fields.Many2many("datatime.info", string="Datetime")
    color = fields.Integer(string="Color Index")
    total_entry = fields.Integer(compute="compute_count")
    vedor_select = fields.Many2one("res.partner", string="Vendor")
    partner_id = fields.Many2one(
        'res.partner', string='Customer')
    company_id = fields.Many2one('res.company', store=True,
                                 default=lambda self: self.env.company)

    
    def _get_portal_return_action(self):
        """ Return the action used to display orders when returning from customer portal. """
        self.ensure_one()
        return self.env.ref('students.students_action_window')

    # state bar --------------------------------------------------------------------------
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("done", "Done"),
            ("confirmed", "Confirmed"),
            ("cancelled", "Cancelled"),
            ("method", "Method"),
        ],
        string="Status",
        default="draft",
    )


    def action_confirm(self):
        self.state = "confirmed"

    def action_cancel(self):
        self.state = "cancelled"

    def action_draft(self):
        self.state = "draft"

    def action_done(self):
        self.state = "done"

    #Send By Mail-----------------------------------------------------------------------------    
    
    def action_send_card(self):
        mail_template = self.env.ref('students.student_card_emil_template')
        mail_template.send_mail(self.id, force_send=True)
        # try:
        #     template_id = self.env.ref('students.student_card_emil_template').id
        # except ValueError:
        #     template_id = False
        # ctx = {
        #     'default_model' : 'students.profile',
        #     'default_res_id' : self.id,
        #     'default_use_template' : bool(template_id),
        #     'default_template_id' : template_id,
        #     'default_composition_mode' : 'comment',
        #     'mark_so_as_sent' : True,
        #     'force_email' : True,
        #     'custom_layout' : 'mail.mail_notification_light'
        # }    

        # return {
        #     'type' : 'ir.actions.act_window',
        #     'view_mode' : 'form',
        #     'res_model' : 'mail.compose.message',
        #     'views' : [(False, 'form')],
        #     'view_id' : False,
        #     'target' : 'new',
        #     'context' : ctx,
        # }

    # SMART BUtton-------------------------------------------------------------------------------
    def datetime(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Time",
            "view_mode": "tree,form",
            "res_model": "datatime.info",
            # 'domain': [('driver_id', '=', self.id)],
            "context": {"stu_name": self.id},
        }

    def _get_report_base_filename(self):
        self.ensure_one()
        return '%s' % (self.name)


    def compute_count(self):
        for record in self:
            record.total_entry = self.env["datatime.info"].search_count(
                [("id", "=", self.ids)]
            )

    @api.depends('birthday')
    def _cal_age(self):
        for rec in self:
            if rec.birthday:
                dt = rec.birthday
                d1 = datetime.strptime(str(dt), "%Y-%m-%d").date()
                d2 = date.today()
                rd = relativedelta(d2, d1)
                rec.age = str(rd.years)
    # @api.depends('birthday')
    # def _cal_age(self):
    #     if self.birthday is not False:
    #         self.age = (datetime.today().date() - datetime.strptime(str(self.birthday), '%Y-%m-%d').date()) // timedelta(days=365)
    # ORM METHOD-------------------------------------------------------------------------
    def action_method(self):

        # # Special methods----------------------------------------------------------------

        # # 1. (0,0,vals)
        # self.write(
        #     {
        #         "name": "Rutvik Raval",
        #         "school_details": [
        #             (0, 0, {"school_name": "JK School", "school_fees": 6000}),
        #             (0, 0, {"school_name": "KP School", "school_fees": 6000}),
        #         ],
        #     }
        # )


        # # 2. (1,0,vals)
        # vals = {"school_details":[]}
        # for school in self.school_details:
        #     vals["school_details"].append([1,school.ids,{"school_name":"Sp jain"}])
        # self.write(vals)  

        # # # 3.(2,ID)
        # self.write({"school_details":[(2,2,0)]})

        # # 4.(3,ID)
        # self.write({"school_details":[(3,1,0)]})

        # 5.(4,ID)
        # self.write({"school_details":[(4,1,0)]})

        # # 6.(5,ID)
        # self.write({"school_details":[(5,0,0)]})

        # 7.(6,ID)
        ids = [1,2]
        self.write({"students_datetime":[(6,0,ids)]})




        # #---->SERCH ORM METHOD
        # students = self.env['students.profile'].search([('id', '=', 1)])
        # print("Students",students.name)
        # students = self.env['students.profile'].search([('id', '=', 1)])
        # print("Students",students.display_name)
        # students_gender = self.env['students.profile'].search([('gender','=','girl')])
        # print("Girl students",students_gender )
        # students_gender = self.env['students.profile'].search([('gender','=','boy'),('age','>=','20')])
        # print("Boy students age Grater Than 20",students_gender )

        # stud_obj = self.env['students.profile']
        # stud_name = []
        # for stud in stud_obj.search([]):
        #     stud_name.append(stud.name)
        # print(stud_name)

        # #---->SERCH COUNT ORM METHOD
        # total_student = self.env['students.profile'].search_count([])
        # print("Total Student....",total_student)
        # total_girls_students = self.env['students.profile'].search_count([('gender','=','girl')])
        # print("Total Girl Students",total_girls_students )

        # #---->ref ORM METHOD
        # #---->browse ORM METHOD
        # browse_reslt = self.env['students.profile'].browse(1)
        # print("browse_reslt...",browse_reslt)
        # browse_reslt = self.env['students.profile'].browse([3,2])
        # print("browse_reslt...",browse_reslt)

        # #---->exists ORM METHOD
        # browse_reslt = self.env['students.profile'].browse(200)
        # if browse_reslt.exists():
        #     print("Existsing")
        # else:
        #     print("Not Existsing")

        # browse_reslt = self.env['students.profile'].browse(3)
        # if browse_reslt.exists():
        #     print("Existsing")
        # else:
        #     print("Not Existsing")

        # #---->create ORM METHOD
        # vals = {"name" : "Keyur Patel",
        #         "phone" : "3434556363",
        #         "age" : 24}
        # self.env["students.profile"].create(vals)

        # vals = {"name" : "Keyur Patel",
        #         "phone" : "3434556363",
        #         "age" : 24}
        # create_record = self.env["students.profile"].create(vals)
        # print("create_record", create_record, create_record.id)

        # #---->write ORM METHOD
        # record_to_update = self.env["students.profile"].browse(11)
        # if record_to_update.exists():
        #     vals = {"name":"Kurvesh Patel", "result": 9.88}
        #     record_to_update.write(vals)

        # #---->copy ORM METHOD
        # record_to_copy = self.env["students.profile"].browse(9)
        # record_to_copy.copy()

        # #---->unlike ORM METHOD
        # record_to_copy = self.env["students.profile"].browse(13)
        # record_to_copy.unlink()

    def name_get(self):
        # name get function for the model execute automatically
        stu = []
        for rec in self:
            stu.append((rec.id, "%s - %s" % (rec.name, rec.id)))
        return stu

    # onchange ---------------------------------------------------------------------------
    @api.onchange("student_school")
    def schoo_type(self):
        for rec in self:
            if rec.student_school:
                rec.sc_type = rec.student_school.school_type


#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
