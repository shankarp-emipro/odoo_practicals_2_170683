from odoo import fields, models


class CrmTeam(models.Model):
    _name = "crm.team.ept"
    _description = "To store crm team data"

    name = fields.Char(string="Team Name", help="Enter crm team name", required=True)
    team_leader = fields.Many2one(string="Team leader", help="Team leader",
                                  comodel_name="res.users")
