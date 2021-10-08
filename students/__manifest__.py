# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Students",
    "version": "14.0.1.0.0",
    'author': "kush",
    'summary': "Students Management System", 
    'description': "This is Students Management System",
    'depends': ['base', 'mail','contacts','sale','account','website',],
    "category": "Students",
    "data": [
        "security/student_security.xml",
        "security/ir.model.access.csv",
        "data/professor.info.csv",
        "data/website_menus.xml",
        "data/contant_template.xml",
        "report/report.xml",
        "report/student_card.xml",
        "report/sale_report_inherit.xml",
        "views/students_view.xml",
        "data/mail_template.xml",
        "views/school_view.xml",
        "views/teachers_view.xml",
        "views/datatime_view.xml",
        "views/professor_view.xml",
        "views/template.xml",
        "views/teacher_template.xml",
    ],
    "demo": [
        # "demo/students_demo_data.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}
