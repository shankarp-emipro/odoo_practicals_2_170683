from odoo import models, fields, _
from odoo.exceptions import ValidationError


class SalesInfoUpdate(models.TransientModel):
    _name = "sales.info.update"
    _description = "Wizard to update sles info"

    user_id = fields.Many2one(string="User", help="User id", comodel_name="res.users",
                              readonly=True)
    team_id = fields.Many2one(string="Team", help="Team id", comodel_name="crm.team", readonly=True)
    user_new_id = fields.Many2one(string="New User", help="New user id", comodel_name="res.users")
    team_new_id = fields.Many2one(string="New Team", help="New team id", comodel_name="crm.team")

    def update_sales_info(self):
        if self.user_new_id.sale_team_id.id == self.team_new_id.id:
            self.env['sale.order'].browse(self._context['active_ids']).write(
                {'user_id': self.user_new_id.id, 'team_id': self.team_new_id.id})
        else:
            raise ValidationError(
                _(
                    self.user_new_id.name + " does not belong to " + self.team_new_id.name + " team."))
