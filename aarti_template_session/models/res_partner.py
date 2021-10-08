from odoo import api, models,fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    enable_team_lead = fields.Boolean(string='Team Lead')
    team_member_ids = fields.One2many('team.members','partner_id')

class TeamMembers(models.Model):
    _name = 'team.members'
    _description = 'Team Members'

    name = fields.Char('Name')
    partner_id = fields.Many2one('res.partner')
