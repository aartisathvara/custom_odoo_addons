from odoo import api, models, fields

class StudentsEmailsUpdateWizard(models.TransientModel):
    _name = "students.emails.update.wizard"
    _description = "students.emails.update.wizard"

    email = fields.Char(string="email")
