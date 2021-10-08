# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models


class DatatimeInfo(models.Model):
    _name = "datatime.info"
    _description = "datatime.info"
    # _rec_name = "s_name"

    s_name = fields.Many2one(
        "students.profile", default=lambda self: self._context.get("stu_name")
    )
    e_time = fields.Datetime(string="Student Enter Time", required=True)
    ex_time = fields.Datetime(string="Student Exit Time", require=True)
    color = fields.Integer(string="Color Index")

    def name_get(self):
        datatime_list = []
        for datatime in self:
            datatime_list.append(
                (
                    datatime.id,
                    "[EN]{} [EX]{}".format(
                        datatime.e_time,
                        datatime.id,
                    ),
                )
            )
        return datatime_list
