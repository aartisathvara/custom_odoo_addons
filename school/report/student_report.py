from odoo import api, fields, models


class StudentInherit(models.AbstractModel):
    _name = 'report.school.school_report_page'
    _description = 'student get value inherit report'

    @api.model
    def _get_report_values(self, docids, data=None):
    	print("\n\n\n yes entered here in the function")
        model = self.env[student.student].browse(self.env.context.get('teacher_ids'))
        print("model",model)
        docs = self.env['student.student'].browse(docids)
        print("docs", docs)
        return {
            'doc_ids': student.student,
            'doc_model': model,
            'data': data,
            'docs': docs,
            'proforma': True
        }
