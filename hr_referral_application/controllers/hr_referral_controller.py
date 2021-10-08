# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, route

class ReferralProgram(http.Controller):
    @http.route("/referral_program", type="http", website=True, auth="user")
    def referral_program(self):
        referral_id = request.env["hr.employee"].sudo().search([])
        degree_id = request.env["hr.recruitment.degree"].sudo().search([])
        department_id = request.env["hr.job"].sudo().search([])
        vals = {
            'referral_id':referral_id,
            'degree_id':degree_id,
            'department_id':department_id,
        }
        return request.render("hr_referral_application.referral_program_template",vals)

    @http.route("/submit_referral_program", type="http", website=True, auth="public")
    def submit_referral_program(self, **post):
        if post:
            referral_id = request.env['hr.employee'].search([('name','=like',post['referral_id'])])
            degree_id = request.env['hr.recruitment.degree'].search([('name','=like',post['degree_id'])])
            department_id = request.env['hr.job'].search([('name','=like',post['department_id'])])
            vals = {
                'name':post['name'],
                'email':post['email'],
                'referral_id':referral_id.id,
                'degree_id':degree_id.id,
                'department_id':department_id.id,
                'expected_salary':post['expected_salary'],
                'joining_date':post['expected_joinning_date'],
                'summary':post['summary'],
                'state':'draft',
            }
            request.env["hr.referral.application"].sudo().create(vals)
            return request.render("hr_referral_application.thank_you_template")