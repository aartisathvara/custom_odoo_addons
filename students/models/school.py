# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SchoolProfile(models.Model):
    _name = "school.info"
    _description = "school.profile"

    school_name = fields.Char(string="SchoolName")
    school_type = fields.Selection(
        [("public", "Public"), ("private", "Private")], string="School Type"
    )
    school_rank = fields.Integer(string="School Rank")
    school_fees = fields.Integer(string="School Fees", required=True)
    stu_imforamtion = fields.Many2one("students.profile", string="SD")

    # compute fields
    school_id = fields.Integer(
        compute="_auto_school_id_populate",
        string="School Id",
        store=True,
        help="This is auto populate data based on school type change",
    )  # store will be use to store tha school id data in module database

    @api.depends("school_type")  # depends will be use to direct live chane in from view
    def _auto_school_id_populate(self):
        for rec in self:
            if rec.school_type == "private":
                rec.school_id = 222
            elif rec.school_type == "public":
                rec.school_id = 333
            else:
                rec.school_id = 000

    # constrains
    @api.constrains("school_fees")
    def _check_fee(self):
        for record in self:
            if record.school_fees < 5000:
                raise ValidationError("Schoo fees will be greater than 5000")

    def name_get(self):
        school_list = []
        for school in self:
            school_list.append(
                (
                    school.id,
                    "School Name {} is {}".format(
                        school.school_name, school.school_type
                    ),
                )
            )
        return school_list
