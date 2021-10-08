from odoo import api, fields, models,_
import datetime

class HrReferralApplication(models.Model):
    _name = "hr.referral.application"
    _description = "Hr Referral Application"

    name = fields.Char(string="Name", required="True",copy=False, readonly=True,states={'draft': [('readonly', False)]},
                       default=lambda self: _('New'))
    email = fields.Char(string="Email")
    state = fields.Selection(
        string="Status",
        default="draft",
        readonly=True,
        copy=False,
        selection=[("draft", "Draft"), ("approved", "Approved"), ("cancel", "Cancel")],
    )
    currency_id = fields.Many2one("res.currency", string="Currency", copy=False)
    referral_id = fields.Many2one("hr.employee", string="Referral Name", copy=False)
    degree_id = fields.Many2one("hr.recruitment.degree", string="Degree", copy=False)
    department_id = fields.Many2one("hr.job", string="Department", copy=False)
    expected_salary = fields.Monetary(string="Expected Salary", store=True, copy=False)
    summary = fields.Text(string="Summary", copy=False,default='Summary..')
    joining_date = fields.Date(string="Expected joining Date", copy=False,default=fields.Datetime.now )

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hr.referral.application') or _('New')
        return super(HrReferralApplication, self).create(vals)

    def action_approved(self):
        for rec in self:
            rec.write({"state": "approved"})

    def action_draft(self):
        for rec in self:
            rec.write({"state": "draft"})

    def action_cancel(self):
        for rec in self:
            rec.write({"state": "cancel"})
