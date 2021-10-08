# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Student(models.Model):
    _name = "student.student"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Student Management"

    name = fields.Char(string="Student Name")
    sequence = fields.Integer(
        "Sequence",
        default=1,
        help="Gives the sequence order when displaying a product list",
    )
    student_gender = fields.Selection(
        [("Female", "female"), ("Male", "male"), ("Others", "others")], string="Gender"
    )
    is_agreed = fields.Boolean(string="Is Agreed?")
    state = fields.Selection(
        string="Status",
        default="draft",
        readonly=True,
        copy=False,
        selection=[("draft", "Draft"), ("confirm", "Validated"), ("done", "Done")],
    )
    roll_no = fields.Integer(string="Roll No")
    address = fields.Text(string="Address")
    color = fields.Integer()
    teacher_ids = fields.One2many(
        "teacher.teacher", "student_id", string="teacher", index=True, tracking=1
    )
    field_with_url = fields.Char("URL", default="www.odoo.com")
    school_result = fields.Integer(string="School Rank")

    def action_confirm(self):
        self.state = "confirm"

    def action_draft(self):
        self.state = "draft"

    def action_done(self):
        self.state = "done"

    _sql_constraints = [
        (
            "name_unique",
            "unique(name)",
            "Please enter unique school name, Given school name already exist",
        ),
        (
            "rollno_unique",
            "unique(roll_no)",
            "Please enter other RollNo, Given roll number already exist",
        ),
        ("roll_no", "CHECK(roll_no>purchase_append)", "please enter positive Roll No"),
    ]

    @api.constrains("school_result")
    def check_result(self):
        for record in self:
            if record.school_result < 4:
                raise ValidationError(
                    "you are not eligible to get this rank!!!!!......"
                )

    # @api.constrains('school_result')
    # def _check_something(self):
    #     for record in self:
    #         if record.school_result < 4:
    #             raise ValidationError("u r not able to get this rank!!!!")

    @api.model
    def name_create(self, name):
        print("Self", self)
        print("Student Name", name)
        rtn = self.create({"name": name})
        print("\n\nrtn", rtn)
        print("rtn.name_get()[0]", rtn.name_get()[0])
        return rtn.name_get()[0]

    @api.model
    def default_get(self, fields_list=[]):
        print("\n\n\n\nfields_list", fields_list)
        rtn = super(Student, self).default_get(fields_list)
        print("beforeeeeeeeeee", rtn)
        rtn.update({"address": "abcccccc......"})
        rtn.update({"roll_no": "12"})
        print("\n\n\nReturn statement", rtn)
        # rtn['is_agreed'] = True
        return rtn

    def unlink(self):
        rtn = super(Student, self).unlink()
        return rtn

    def clear_record_data(self):
        self.write(
            {
                "name": "",
                "student_gender": "",
                "is_agreed": "",
                "roll_no": "",
                "address": "",
            }
        )

    @api.returns("self", lambda value: value.id)
    def copy(self, default={}):
        # default['active'] = False
        default["name"] = "copy (" + self.name + ")"
        print("default values", default)
        # print("self recordset ",self)
        rtn = super(Student, self).copy(default=default)
        print("Return statement", rtn)
        return rtn

    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     print("view id",view_id)
    #     print("view Type ",view_type)
    #     print("toolbar",toolbar)
    #     print("submenu",submenu)
    #     res = super(Student, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
    #     print("Return Disc",res)
    #     return res
