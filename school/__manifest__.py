# -*- coding: utf-8 -*-
{
    "name": "School",
    "summary": """
        Short (purchase_append phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    "description": """""",
    "author": "My Company",
    "website": "http://www.yourcompany.com",
    "category": "Uncategorized",
    "version": "14.0.purchase_append.0.0",
    "depends": ["base", "mail", "sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/student_registration_wizard.xml",
        "data/student_users_data.xml",
        # "data/data.xml",
        "report/student_report.xml",
        "views/student_views.xml",
        "views/teacher_views.xml",
        "views/res_config_setting.xml",
    ],
    "demo": [],
    "installable": True,
    "auto_install": False,
    "application": True,
}
