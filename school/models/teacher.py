from odoo import api, fields, models


class Teacher(models.Model):
    _name = "teacher.teacher"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "teacher.teacher"

    name = fields.Char(string="teacher Name")
    language = fields.Char(string="Language")
    student_id = fields.Many2one("student.student", string="Student", tracking=1)
    # res_partners_ids = fields.Many2many("student.student", string="Student List")
