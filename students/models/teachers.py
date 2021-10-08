# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models
from odoo.exceptions import ValidationError


class TeachersPorfile(models.Model):
    _name = "teachers.profile"
    _description = "teachers.profile"
    _inherit = "portal.mixin"

    def _compute_access_url(self):
        super(TeachersPorfile, self)._compute_access_url()
        for tea in self:
            tea.access_url = '/teachers/data/%s' % (tea.id)

    # def _compute_access_url(self):
    #     for tea in self:    
    #         return '/teachers/data/%s' % (tea.id)


    t_name = fields.Char(string="Teacher Name", required=True)
    photo = fields.Binary(string="Teacher Image")
    # t_id = fields.Integer(string="Teacher School Id")
    t_email = fields.Char(string="Teacher Email")
    t_subject = fields.Char(string="Teacher Subject")
    t_experience = fields.Float(string="Teacher Experience")
    t_gender = fields.Selection(
        [("girl", "Girl"), ("boy", "Boy")], string="Teacher Gender"
    )

    _sql_constraints = [
        ("email_unique", "Unique(t_email)", "Teacher Email will be alrady exists"),
        # ("id_unique", "Unique(t_id)", "Teacher Id will be same"),
    ]
    t_availabe = fields.Boolean(string="Teacher Availabe", default=True)
    t_address = fields.Char(string="Teacher Address")
    total_t = fields.Integer(string="Total Teachers")
    stu_info = fields.One2many(
        "students.profile", "student_teacher", string="Student Info"
    )

    def name_get(self):
        teachers_list = []
        for teacher in self:
            teachers_list.append(
                (
                    teacher.id,
                    "{}".format(
                        teacher.t_name,

                    ),
                )
            )
        return teachers_list

    @api.model
    def name_search(
        self, name="", args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        if name and not self.env.context.get("import_file"):
            args = args if args else []
            args.extend(["|", ["t_name", "ilike", name], ["t_subject", "ilike", name]])
            name = ""
        return super(TeachersPorfile, self).name_search(
            name=name, args=args, operator=operator, limit=limit
        )

    def special_command(self):
        self.write({"t_name": "RK Rathod", "stu_info": [(0, 0, {"name": "kp patel"})]})
