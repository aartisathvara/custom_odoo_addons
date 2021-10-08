# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProfessorInfo(models.Model):
    _name = "professor.info"
    _description = "professor.info"


    p_name = fields.Char(string="Professor Name")
    email = fields.Char(string="Professor Email")